from describe import mean, db
import pandas as pd
import math

corr = []

def pearsonCorrelation(f1, f2):
    x = [float(v) for v in f1]
    y = [float(v) for v in f2]

    xMean = mean(x)
    yMean = mean(y)

    res = 0
    up = [(x[i] - xMean) * (y[i] - xMean) for i in range(len(x))]
    down = math.sqrt([math.pow(x[i] - xMean, 2) * math.pow(y[i] - yMean, 2) for i in range(len(x))])
    return up / down

def findPair():
    pass


def main():
    for f1 in range(len(db)):
        for f2 in range(f1, len(db)):
            if pd.api.types.is_numeric_dtype(db[f1[0]]) and f1 != "Index" and pd.api.types.is_numeric_dtype(db[f2[0]]) and f2 != "Index" :
                print(f1, f2)
                pearsonCorrelation(f1, f2)


if __name__ == "__main__":
    main()