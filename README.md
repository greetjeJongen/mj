# Mava Jini Tests - MJ

# Usage
Before setting up this webserver, make sure you have these modules installed:
* flask
* flask_mysqldb
* 
# Github
In the settings of the organisation, you have to add the "/hook" route to the webhooks, and make sure it gets called on every 'push' event.

In order to assign new questions to the repositories of students, a Github account is required with Owner privileges on the organisation. This account is used for pushing the new questions and will show up among the student's commits. 
The account should be set up be able to pull and push to the organisation without entering a password. (Either through SSH/GPG keys or by entering the credentials in the Git config)
The name of this account must also be specified in the configuration of app.py, in order to distinguish pushes from the students and from the system. (see bottom of this readme, 'Additional config')

# Database
You can edit the database configuration in lines 9 - 13 in app.py

This is the MySQL syntax to setup the tables needed:
```sql
TODO
```
# Routes
* **"/"** [GET] : Shows the words words 'Welcome to the Mava Jini Tests!'. Used only to verify server availability

* **"/question/-user-/next"** [GET] : Gives the specified user their next question.
The category of the new question depends on the result of the previous submission:
When a user pushes a correct submission, they should be given a new question of the next category.
Otherwise, when the answer of the user was incorrect, his next question will be of the same category.
(This endpoint should, normally, not be called manually. Instead, it is meant to be called automatically when a user submission was made)

* **"/hook"** [POST] : Don't manually use this route, this is intended for requests comming from Github.

* **"/test/add/-user-/-category-/-question-"** [POST] : Parses the test output given by the bash script and insert a new row into the database, specifying whether the user's submission was correct or not. Don't manually use this route, this is intended for requests comming from the bash script.

* **"/status/everyone"** [GET] : Returns a list of every answer from every user and if this answer was correct or not. (JSON)

* **"/status/-user-"** [GET] : Returns a list of every answer for a specific user and if this answer is correct or not. (JSON)

# Additional config
- On line 17, the path to the example questions is specified.
- On line 18, the path to the user repositories is specified.
- On line 19, the port number of the webserver is specified.
- On line 20, the Github name of the testing user is specified. (see 'IMPORTANT' above)
