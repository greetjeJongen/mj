import os, random, sys, git, subprocess
import shutil

questions_path = "../MJQuestions/"
repos_path = "../mj_repos/"

def get_random_question(category):
    path = "../MJQuestions/"+category+"/"
    
    li = []
    for x in os.listdir(path):
        if os.path.isdir(os.path.join(path, x)):
            li.append(x)
    if len(li) < 1:
        sys.exit("No questions available for this category!")
    rand = random.randint(0, len(li)-1)
    return li[rand]

def copy_question(user, cat, q):
    user_path = repos_path + user
    user_cat_path = user_path + "/" + cat

    # remove previous question(s) from this category of verplaatsen naar foute opdrachten mapke
    res = subprocess.call(["rm", "-rf", user_cat_path])
    print(res)

    # copy new question
    if not os.path.exists(user_cat_path):
        os.mkdir(user_cat_path)

    src_path = questions_path + cat + "/" + q + "/Student.java"
    dest_path = user_cat_path + "/Student.java"
    shutil.copy(src_path, dest_path)
    # res = subprocess.call(["cp", "../MJQuestions/" + cat + "/" + q + "/*", user_cat_path + "/" + q])

    # push changes
    try:
        repo = git.Repo(user_path+"/.git")
        repo.git.add(A=True)
        repo.index.commit("New question from category " + cat)
        origin = repo.remote(name="origin")
        origin.push()
    except Exception as e:
        print("Something went wrong pushing the new question!")
        print(e)


def insert_question(user, category, path):

    return None