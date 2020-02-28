import os, random, sys

category = "01-booleans"
path = "../MJQuestions/"+category+"/"

li = []
for x in os.listdir(path):
    if os.path.isdir(os.path.join(path, x)):
        li.append(x)
if len(li) < 1:
    sys.exit("No questions available for this category!")
rand = random.randint(0, len(li)-1)
print(li[rand])
