import pandas as pd
import math
from describe import db
import  matplotlib.pyplot as plt


bookMarks = {}
nbCourse = 0



houses = {
    "Ravenclaw": db[db["Hogwarts House"] == "Ravenclaw"],
    "Gryffindor": db[db["Hogwarts House"] == "Gryffindor"],
    "Hufflepuff": db[db["Hogwarts House"] == "Hufflepuff"],
    "Slytherin": db[db["Hogwarts House"] == "Slytherin"],
}

def mean_series(series):
    values = [float(v) for v in series if pd.notna(v)]
    return sum(values) / len(values)


def std(filterColumns):
    values = [float(v) for v in filterColumns if pd.notna(v)]
    res = math.sqrt(sum((v - mean_series(filterColumns))**2 for v in values) / (len(values) - 1))
    return res


def calculateStd(name):
    global nbCourse
    nbCourse += 1
    res = 0
    for house in houses.values():
        res += std(house[name])
    res /= 4
    bookMarks[name] = (res)

def min_dict():
    items = list(bookMarks.items())
    key, value = items[0]

    for k, v in items:
        if v < value:
            key = k
            value = v

    return (key, value)


def main():
    for name in db:
        if pd.api.types.is_numeric_dtype(db[name]) and name != "Index":
            calculateStd(name)
    print(min_dict())
    plt.legend("test")
    plt.xlabel(bookMarks.keys)
    plt.ylabel(bookMarks.values)
    plt.show()

    #need to set up the histogram

if (__name__ == "__main__"):
    main()