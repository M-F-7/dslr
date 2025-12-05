import pandas as pd
from describe import db, std, min

bookMarks = {}
nbCourse = 0

def calculateStd(name):
    global nbCourse
    nbCourse += 1
    res = 0
    raven = db[db["Hogwarts House"] == "Ravenclaw"]
    griffin = db[db["Hogwarts House"] == "Gryffindor"]
    huffle = db[db["Hogwarts House"] == "Hufflepuff"]
    slyther = db[db["Hogwarts House"] == "Slytherin"]
    res += std(raven[name])
    res += std(griffin[name])
    res += std[huffle[name]]
    res += std(slyther[name])
    res / 4
    bookMarks[name] = (res)

def main():
    for name in db:
        if pd.api.types.is_numeric_dtype(db[name]) and name != "Index":
            calculateStd(name)
    print(bookMarks)



if (__name__ == "__main__"):
    main()