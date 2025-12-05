import pandas as pd
import math

ex = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
idx = 0

db = pd.read_csv("./data.csv")

flag = True

def printEx():
    global idx
    if idx < len(ex):
        print(ex[idx], end="      ")  
    idx += 1

def count(x):
    res = len(db[x])
    return res

def mean(x):
    res = sum(db[x]) / len(db[x])
    return res

def std(x):
    res = math.sqrt(sum(pow(v - mean(x), 2) for v in db[x]))
    return res / len(db) - 1

def min(x):
    try:
        res = float(db[x].name)
    except ValueError:
        print("Min: Error")
        exit(1)

    for value in db[x]:
        if res > value:
            res = value
    return res


def max(x):
    try:
        res = float(db[x].name)
    except ValueError:
        print("Max: Error")
        exit(1)

    for value in db[x]:
        if res < value:
            res = value
    return res


def median(tab):
    sorted_feature = tab.sort_values().values
    size = len(sorted_feature)
    tab = []
    if size % 2 == 0:
        res = (sorted_feature[(size // 2 - 1)] + sorted_feature[size // 2]) / 2 # // for int and / for float
    else:
        res = sorted_feature[size // 2]
    return res

def twentyFive(x):
    tab = []
    sorted_feature = db[x].sort_values().values
    res =   #calculer la size a la place de la value de la median et copie from ca et check paire impaire size
    tab.extend(sorted_feature[0:res])
    res = median(tab)
    return res

def fifty(x):
    return median(db[x])

def seventyFive(x):
    tab = []
    sorted_feature = db[x].sort_values().values
    res = median(db[x]) # // 
    tab.extend(sorted_feature[res::])
    res = median(tab)
    return res

def chooseMetric(name, metric):
    global flag
    if flag:
        printEx()
        flag = False
    match metric:
        case 0:
            print(f"{count(name):.6f} ", end="   ")
        case 1:
            print(f"{mean(name):.6f}", end="    ")
        case 2:
            print(f"{std(name):.6f}", end="    ")
        case 3:
            print(f"{min(name):.6f}", end="    ")
        case 4:
            print("4", end="    ")
        case 5:
            print(f"{fifty(name):.6f}", end="    ")
        case 6:
            print("6", end="    ")
        case 7:
            print(f"{max(name)}", end="    ")
        case _: # same as default in c
            print("Unkown", end="    ")



def main():
    metric = 0
    global flag
    while metric <= len(ex):
        for name in db:
            try:
                nb = float(name)
                chooseMetric(name, metric)
                if metric == 7 and idx == 8 and  name == db.iloc[:, -1].name:
                    exit()
                if name == db.iloc[:, -1].name:
                    flag = True
                    metric += 1
                    print()
            except ValueError:
                pass


if (__name__ == "__main__"):
    main()