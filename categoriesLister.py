import os

def list_cats():
    path="../MJQuestions/"
    res = []
    for x in os.listdir(path):
        if os.path.isdir(os.path.join(path, x)) and not x.startswith("."):
            res.append(x)
    res.sort()
    return res

def first_cat():
    r = list_cats()
    return r[0]
