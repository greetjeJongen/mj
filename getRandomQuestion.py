import os, random, sys, git, subprocess


def getRandomQuestion(category):
    path = "../MJQuestions/"+category+"/"
    
    li = []
    for x in os.listdir(path):
        if os.path.isdir(os.path.join(path, x)):
            li.append(x)
    if len(li) < 1:
        sys.exit("No questions available for this category!")
    rand = random.randint(0, len(li)-1)
    return li[rand]

def copyQuestion(user, cat, q):
    user_path = "../mj_repos/" + user

    # remove previous question(s) from this category of verplaatsen naar foute opdrachten mapke
    res = subprocess.call(["rm", "-rf", user_path + "/" + cat])
    print(res)

    # copy new question
    res = subprocess.call(["cp", "../MjQuestions/" + cat + "/" + q, user_path + "/" + cat + "/" + q])
    print(res)

    # push changes
    try:
        repo = git.Repo(user_path+"/.git")
        repo.git.add(update=True)
        repo.index.commit("New question from category " + cat)
        origin = repo.remote(name="origin")
        origin.push()
    except:
        print("Something went wrong pushing the new question!")