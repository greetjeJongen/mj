import os

def list():
    path="../MJQuestions/"
    res = []
    for x in os.listdir(path):
        if os.path.isdir(os.path.join(path, x)) and not x.startswith("."):
            res.append(x)
    return res.sort()
