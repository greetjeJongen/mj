import os

def listCats():
    path="../MJQuestions/"
    res = []
    for x in os.listdir(path):
        if os.path.isdir(os.path.join(path, x)) and not x.startswith("."):
            res.append(x)
    res.sort()
    return res

def firstCat():
    r = listCats()
    return r[0]
