import pandas as pd
import math
from src.describe import db
import  matplotlib.pyplot as plt


bookMarks = {}



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
    bookMarks[name] = {}
    for house, values in houses.items():
        bookMarks[name][house] = std(values[name])


def findBestCourse():
    best_course = None
    best_diff = float("inf")

    for course, house_dict in bookMarks.items():
        std_values = list(house_dict.values())
        diff = max(std_values) - min(std_values)

        if diff < best_diff:
            best_diff = diff
            best_course = course

    best_house_stats = bookMarks[best_course]
    tab = [(house, std_value) for house, std_value in best_house_stats.items()]

    return best_course, tab


def main():
    for name in db:
        if pd.api.types.is_numeric_dtype(db[name]) and name != "Index":
            calculateStd(name)

    tab = findBestCourse()
    team = [x[0] for x in tab[1]]
    values = [x[1] for x in tab[1]]
    colors = ['blue', 'red', 'yellow', 'green']

    for i, v in enumerate(values):
        plt.text(i, v, f"{v:.4f}", ha='center', va='bottom')

    plt.ylim(min(values) * 0.95, max(values) * 1.15)
    plt.bar(team, values, color=colors)
    plt.xlabel("Houses")
    plt.ylabel("Standard deviation")
    plt.title("Standard deviation for each houses")

    plt.show()

if (__name__ == "__main__"):
    main()