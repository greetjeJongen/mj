import os, git, subprocess
from flask import Flask, request, json, jsonify
from flask_mysqldb import MySQL


# MySQL config
app = Flask(__name__)
app.config['MYSQL_USER'] = 'dht'
app.config['MYSQL_PASSWORD'] = 'mvghetdhtmvghetdht'
app.config['MYSQL_DB'] = 'mj_testr'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)


@app.route("/")
def index():
    return "Welcome! zieke flask server hier gemaakt door the Didactical Aids Team"

@app.route("/question/<user>/current")
def current_question(user):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT pathToQuestion FROM answer WHERE repoName=%s and datetimeOfAnswer is null;", [str(user)])
    res = cursor.fetchall()
    cursor.close()

    if len(res) == 0:
        return False

    current = res[0][0]

    return True

@app.route("/question/<user>/next")
def next_question(user):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT pathToQuestion FROM answer WHERE repoName=%s and datetimeOfAnswer is null;", [str(user)])
    res = cursor.fetchall()
    cursor.close()



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
