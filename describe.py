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
    global flag
    if flag:
        printEx()
        flag = False
    res = len(db[x])
    return res

def chooseMetric(name, metric):
    match metric:
        case 0:
            print(f"{count(name):.6f} ", end="   ")
        case 1:
            print("1")
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case _: # same as default in c
            pass



def main():
    metric = 0
    # for name in db:
    while metric < len(db):
        name = db.columns[metric]
        try:
            if metric == 8 and idx == 8:
                break
            nb = float(name)
            chooseMetric(name, metric)
            if name == db.iloc[:, -1].name:
                name = db.columns[0]
                print(name)
        except ValueError:
            # print(i)
            pass
        # i += 1


if (__name__ == "__main__"):
    main()