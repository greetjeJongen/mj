import os

def list_cats():
    res = []
    for x in os.listdir(questions_path):
        if os.path.isdir(os.path.join(questions_path, x)) and not x.startswith("."):
            res.append(x)
    res.sort()
    return res

def first_cat():
    r = list_cats()
    return r[0]
