import os, git
from datetime import datetime
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

# app config
questions_path = "../MJQuestions/"
repos_path = "../mj_repos/"


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
        return user+" already has a question"
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT category FROM answer WHERE repoName=%s ORDER BY datetimeOfAnswer DESC LIMIT 1;", [str(user)])
    res = cursor.fetchall()
    cursor.close()
    if len(res) == 0:
        print(user+ " hasn't made any exercises yet. Setting up for first question!")
        category = cl.first_cat()
        ques = rq.get_random_question(str(category))
        path_to_question = repos_path + user + "/" + category + "/" + ques
        print("Assigning " + path_to_question + " ...")

        # copy and push
        rq.copy_question(user, category, ques)

        # insert nieuwe vraag in db
        insert_question(category, ques, user)

        return "new question delivered"

    else:
        last_cat = res[0][0]
        print(user+" has made an exercise for all categories up to " + last_cat)
        cats = cl.list_cats()
        index = cats.index(last_cat)
        if index >= len(cats)-1:
            print("All exercises are made")
            return "all exercises made"
        else:
            next_cat = cats[index+1]
            ques = rq.get_random_question(str(next_cat))
            path_to_question = repos_path + user + "/" + next_cat + "/" + ques
            print("Assigning " + path_to_question + " ...")

            # copy and push
            rq.copy_question(user, next_cat, ques)

            # insert neiuwe vraag in db
            insert_question(next_cat, ques, user)

        return "new question delivered"


def insert_question(category, ques, user, datime=None):
    # datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO answer(repoName, category, pathToQuestion, dateTimeOfAnswer, passed) values (%s,%s,%s,%s,%s) ",
        (user, category, category + "/" + ques + "/", datime, 0))
    mysql.connection.commit()
    cursor.close()


@app.route("/hook", methods=['POST'])
def hook():
    # wordt opgeroepen bij elke push in de organisatie
    # runt script dat java code compileert en test (zie /root/eindwerk/mj_repos/run_tests)

    # code clonen
    data = request.data
    url = json.loads(data)["repository"]["url"]
    name = json.loads(data)["repository"]["name"]

    if os.path.exists(path + name):
        git.Git(repos_path + name).pull(url)
    else:
        git.Git(repos_path).clone(url)

    # tests runnen
    #rc = subprocess.call(["/root/eindwerk/mj_repos/run_tests", str(name)])
    return "success"

@app.route("/status/everyone")
def status_all():
    cursor = mysql.connection.cursor()
    cursor.execute("select repoName, passed from answer")
    res = cursor.fetchall()
    cursor.close()
    return jsonify(res)


@app.route("/status/<name>")
def status(name):
    return "success"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=83)
