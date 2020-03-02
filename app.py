import os, git, subprocess
from flask import Flask, request, json, jsonify
from flask_mysqldb import MySQL
import categoriesLister as cl
import getRandomQuestion as rq

# MySQL config
app = Flask(__name__)
app.config['MYSQL_USER'] = 'dht'
app.config['MYSQL_PASSWORD'] = 'mvghetdhtmvghetdht'
app.config['MYSQL_DB'] = 'mj_testr'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)


@app.route("/")
def index():
    return "Welcome! Dit is de endpoint voor Mava Jini Testr"

def has_current_question(user):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT pathToQuestion FROM answer WHERE repoName=%s and datetimeOfAnswer is null;", [str(user)])
    res = cursor.fetchall()
    cursor.close()

    return len(res) != 0

@app.route("/question/<user>/next")
def next_question(user):
    if has_current_question(user):
        return user+" already has a question!"
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT category FROM answer WHERE repoName=%s ORDER BY datetimeOfAnswer DESC LIMIT 1;", [str(user)])
    res = cursor.fetchall()
    cursor.close()
    if len(res) == 0:
        print(user+ " hasn't made any exercises yet. Setting up for first question!")
        category = cl.firstCat()
        ques = rq.getRandomQuestion(str(category))
        pathToQuestion = "../mj_repos/"+user+"/"+category+"/"+ques
        print("Assigning " + pathToQuestion + " ...")

        # copy and push
        rq.copyQuestion(user, category, ques)

        # insert nieuwe vraag in db


        return "success"
    else:
        lastCat = res[0][0]
        print(user+" has made an exercise for all categories up to " + lastCat)
        cats = cl.listCats()
        index = cats.index(lastCat)
        if index >= len(cats):
            print("All exercises are made!?")
        else:
            nextCat = cats[index+1]
            ques = rq.getRandomQuestion(str(nextCat))
            pathToQuestion = "../mj_repos/"+user+"/"+nextCat+"/"+ques
            print("Assigning " + pathToQuestion+ " ...")

            # copy and push
            rq.copyQuestion(user, nextCat, ques)

            # insert neiuwe vraag in db

        return "success"

@app.route("/hook", methods=['POST'])
def hook():
    # wordt opgeroepen bij elke push in de organisatie
    # runt script dat c++ code compileert en test (zie /root/eindwerk/lb_repos/run_tests)

    # code clonen
    data = request.data
    url = json.loads(data)["repository"]["url"]
    name = json.loads(data)["repository"]["name"]
    path = "../mj_repos/"

    if os.path.exists(path + name):
        git.Git(path + name).pull(url)
    else:
        git.Git(path).clone(url)

    # tests rerunnen
    #rc = subprocess.call(["/root/eindwerk/mj_repos/run_tests", str(name)])
    return "success"

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug = True, port=83)
