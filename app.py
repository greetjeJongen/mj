import os, git, subprocess
from flask import Flask, request, json
from flask_mysqldb import MySQL

app = Flask(__name__)

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
    rc = subprocess.call(["/root/eindwerk/mj_repos/run_tests", str(name)])
    return "success"

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug = True, port=83)
