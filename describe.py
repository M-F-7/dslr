import pandas as pd
import math

ex = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
idx = 0

db = pd.read_csv("./datasets/dataset_train.csv")

flag = True

def printEx():
    global idx
    if idx < len(ex):
        print(f"{ex[idx]:<8}", end="      ")  
    idx += 1

def count(x):
    res = len(db[x])
    return res

def mean(x):
    values = [float(v) for v in db[x] if pd.notna(v)]
    res = sum(values) / len(values)
    return res

def std(x):
    values = [float(v) for v in db[x] if pd.notna(v)]
    res = math.sqrt(sum((v - mean(x))**2 for v in values) / (len(values) - 1))
    return res

def min(x):
    try:
        res = float(db[x].iloc[0])
    except ValueError:
        print("Min: Error")
        exit(1)

    for value in db[x]:
        if res > value:
            res = value
    return res


def max(x):
    try:
        res = float(db[x].iloc[0])
    except ValueError:
        print("Max: Error")
        exit(1)

    for value in db[x]:
        if res < value:
            res = value
    return res


def median(tab):
    if isinstance(tab, list):
        sorted_feature = sorted(tab)
    else:
        sorted_feature = tab.sort_values().values
    size = len(sorted_feature)
    if size % 2 == 0:
        res = (sorted_feature[(size // 2 - 1)] + sorted_feature[size // 2]) / 2 # // for int and / for float
    else:
        res = sorted_feature[size // 2]
    return res

def twentyFive(x):
    sorted_feature = db[x].sort_values().values
    size = len(sorted_feature)
    lower_half = sorted_feature[0 : size // 2]
    return median(list(lower_half))

def fifty(x):
    return median(db[x])

def seventyFive(x):
    sorted_feature = db[x].sort_values().values
    size = len(sorted_feature)
    if size % 2 == 0:
        upper_half = sorted_feature[size // 2 : ]
    else:
        upper_half = sorted_feature[size // 2 + 1 : ]
    return median(list(upper_half))


def chooseMetric(name, metric):
    global flag
    if flag:
        printEx()
        flag = False
    match metric:
        case 0:
            print(f"{count(name):>13.6f} ", end="   ")
        case 1:
            print(f"{mean(name):>13.6f}", end="    ")
        case 2:
            print(f"{std(name):>13.6f}", end="    ")
        case 3:
            print(f"{min(name):>13.6f}", end="    ")
        case 4:
            print(f"{twentyFive(name):>13.6f}", end="    ")
        case 5:
            print(f"{fifty(name):>13.6f}", end="    ")
        case 6:
            print(f"{seventyFive(name):>13.6f}", end="    ")
        case 7:
            print(f"{max(name):>13.6f}", end="    ")
        case _: # same as default in c
            print("Unkown", end="    ")

def main():
    metric = 0
    global flag
    for feature in db:
        if pd.api.types.is_numeric_dtype(db[feature]):
            print(f"{feature:<11}", end = "    ")
    print()
    while metric <= len(ex):
        for name in db:
            if pd.api.types.is_numeric_dtype(db[name]):
                chooseMetric(name, metric)
            if metric == 7 and idx == 8 and  name == db.columns[-1]:
                exit()
            if name == db.columns[-1]:
                flag = True
                metric += 1
                print()


if (__name__ == "__main__"):
    main()