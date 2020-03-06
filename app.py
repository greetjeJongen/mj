import os, git
import subprocess
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
port = 83
testing_user = "arnevandoorslaer"

@app.route("/")
def index():
    return "Welcome to the Mava Jini Tests!"

# gives the specified user their next qusetion
# the category of the new question depends on the result of the previous submission
# when a user pushes a correct submission, they should be given a new question of the next category
# otherwise, when the answer of the user was incorrect, his next question will be of the same category
@app.route("/question/<user>/next")
def next_question(user):
    if has_current_question(user):
        return user+" already has a question"

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT category, passed FROM answer WHERE repoName=%s ORDER BY datetimeOfAnswer DESC LIMIT 1;", [str(user)])
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
        passed = res[0][1]
        print(user+" has made an exercise for all categories up to " + last_cat)
        cats = cl.list_cats()
        index = cats.index(last_cat)
        if index >= len(cats)-1:
            print("All exercises are made")
            return "all exercises made"
        else:
            next_cat = cats[index+1]
            if passed is False:
                next_cat = cats[index]
            ques = rq.get_random_question(str(next_cat))
            path_to_question = repos_path + user + "/" + next_cat + "/" + ques
            print("Assigning " + path_to_question + " ...")

            # copy and push
            rq.copy_question(user, next_cat, ques)

            # insert neiuwe vraag in db
            insert_question(next_cat, ques, user)

        return "new question delivered"

# github webhook listening for updates in the repository
# this endpoint should not be called manually
@app.route("/hook", methods=['POST'])
def hook():
    # wordt opgeroepen bij elke push in de organisatie
    # runt script dat java code compileert en test (zie /root/eindwerk/mj_repos/run_tests)
    data = request.data

    # nakijken of pusher weldegelijk student is en niet de server die
    # een nieuwe vraag heeft toegewezen
    if json.loads(data)["pusher"]["name"] == testing_user:
        return "server pushed"

    # code clonen
    url = json.loads(data)["repository"]["url"]
    name = json.loads(data)["repository"]["name"]

    if os.path.exists(repos_path + name):
        git.Git(repos_path + name).pull(url)
    else:
        git.Git(repos_path).clone(url)
    
    pTemp = current_question(name)
    pTemp = pTemp.split("/")
    cat = pTemp[0]
    ques = pTemp[1]
    print(str(pTemp))
    # tests runnen
    rc = subprocess.call(["/root/eindwerk/mj_repos/run_tests", str(name), str(cat), str(ques)])
    return "success"

# parses the test output and inserts a new row in the database for this user
# specifying if their submission was correct or not
# this endpoint should not be called manually, but by the included bash script
@app.route("/test/add/<user>/<cat>/<ques>", methods=["POST"])
def add_test(user, cat, ques):
    # if request data is goed
    # insert passed 1 into db
    # else 0
    # also timedate of answer fixen:
    passed = not "FAILURES" in str(request.data)
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO answer(repoName, category, pathToQuestion, dateTimeOfAnswer, passed) values (%s,%s,%s,now(),%s) ",
        (user, cat, cat + "/" + ques + "/", passed))
    mysql.connection.commit()
    cursor.close()

    # geef volgende vraag
    next_question(user)


    return "success"

# TODO naar deze endpoint kijken want de output ervan is nie logisch
# returns a list of every answer and whether that answer was correct or not
@app.route("/status/everyone")
def status_all():
    cursor = mysql.connection.cursor()
    cursor.execute("select repoName, passed from answer")
    res = cursor.fetchall()
    cursor.close()
    return jsonify(status_parse(res))

# returns every answer of a specific user
@app.route("/status/<name>")
def status(name):
    cursor = mysql.connection.cursor()
    cursor.execute("select repoName, passed from answer where repoName=%s", [str(name)])
    res = cursor.fetchall()
    cursor.close()
    if len(res) == 0:
        return "no users found with repository " + name
    return jsonify(status_parse(res))



# below are helper functions designed in an effort to keep the endpoints tidy

# given a category, question and user
# inserts a row into the answer table
# used to give the user a new question (where passed is NULL)
def insert_question(category, ques, user, datime=None):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO answer(repoName, category, pathToQuestion, dateTimeOfAnswer, passed) values (%s,%s,%s,now(),%s) ",
        (user, category, category + "/" + ques + "/", None))
    mysql.connection.commit()
    cursor.close()

# returns the latest question a given user has not yet completed
# (the one they're currently working on)
def current_question(user):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT pathToQuestion FROM answer WHERE repoName=%s AND passed IS NULL ORDER BY datetimeOfAnswer DESC LIMIT 1;", [str(user)])
    res = cursor.fetchall()
    cursor.close()
    print(res[0][0])
    return res[0][0]

# checks if the user currently has a question
# for which they have not yet made any submissions
def has_current_question(user):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT passed FROM answer WHERE repoName=%s ORDER BY datetimeOfAnswer DESC LIMIT 1;", [str(user)])
    res = cursor.fetchall()
    cursor.close()

    print(len(res))

    if len(res) == 0:
        return False
    else:
        return res[0][0] is None

# given a list of tuples res (query result), this function converts this list to a dict with readable keys
# so that there is no need to rely on indexes. (it also looks better)
def status_parse(res):
    result = []
    for row in res:
        d = {}
        d["repoName"] = row[0]
        d["passed"] = row[1]
        result.append(d)

    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=port)
