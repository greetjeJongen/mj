# Mava Jini Tests - MJ
Daverend grenzeloos innovatief onstuimig code projectwerk omtrent het voorschotelen van "mini" tests aan studenten toegepaste informatica systemen richting (UCLL Leuven, Haasrode - campus Proximus)


# Usage

# Github

# Database

# Routes
* "/" [GET] : Shows the words words 'Welcome to the Mava Jini Tests!'. Used only to verify server availability
* "/question/<user>/next" [GET] : Gives the specified user their next question.
The category of the new question depends on the result of the previous submission:
When a user pushes a correct submission, they should be given a new question of the next category.
Otherwise, when the answer of the user was incorrect, his next question will be of the same category.
(This endpoint should, normally, not be called manually. Instead, it is meant to be called automatically when a user submission was made)
* "/hook" [POST] : Don't manually use this route, this is intended for requests comming from Github.
* "/test/add/<user>/<category>/<question>" [POST] : Parses the test output given by the bash script and insert a new row into the database, specifying whether the user's submission was correct or not. Don't manually use this route, this is intended for requests comming from the bash script.
* "/status/everyone" [GET] : Returns a list of every answer from every user and if this answer was correct or not. (JSON)
* "/status/<user>" [GET] : Returns a list of every answer for a specific user and if this answer is correct or not. (JSON)
# Additional config