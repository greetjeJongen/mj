import os, random, sys, git, subprocess
import shutil


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
    user_path = "../mj_repos/" + user
    user_cat_path = user_path + "/" + cat

    # remove previous question(s) from this category of verplaatsen naar foute opdrachten mapke
    res = subprocess.call(["rm", "-rf", user_cat_path])
    print(res)

    # copy new question
    if not os.path.exists(user_cat_path):
        os.mkdir(user_cat_path)

    src_path = "../MJQuestions/" + cat + "/" + q
    for file in os.listdir(src_path):
        full_path = os.path.join(src_path, file)
        if os.path.isfile(full_path):
            shutil.copy(full_path, user_cat_path + "/" + q)
    # res = subprocess.call(["cp", "../MJQuestions/" + cat + "/" + q + "/*", user_cat_path + "/" + q])
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