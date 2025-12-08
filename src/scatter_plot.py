from describe import db
import pandas as pd
import math
import matplotlib.pyplot as plt

def mean(series):
    values = [float(v) for v in series if pd.notna(v)]
    return sum(values) / len(values)


def pearsonCorrelation(f1, f2):
    df = pd.DataFrame({'x': f1, 'y': f2}).dropna()
    x = df['x'].astype(float).values
    y = df['y'].astype(float).values

    xMean = x.mean()
    yMean = y.mean()

    num = ((x - xMean) * (y - yMean)).sum()
    den = math.sqrt(((x - xMean)**2).sum() * ((y - yMean)**2).sum())

    return num / den


def findPair():
    features = [c for c in db.columns if pd.api.types.is_numeric_dtype(db[c])]
    best = None
    best_corr = -1

    for i in range(len(features)):
        for j in range(i+1, len(features)):
            f1, f2 = features[i], features[j]
            corr = abs(pearsonCorrelation(db[f1], db[f2]))
            if corr > best_corr:
                best_corr = corr
                best = (f1, f2)

    return best


def main():

    (f1, f2) = findPair()
    plt.scatter(db["History of Magic"], db["Potions"], alpha=0.6) # more visible 
    # plt.scatter(db[f1], db[f2], alpha=0.6)
    plt.xlabel(f1)
    plt.ylabel(f2)
    plt.title(f"Scatter plot: {f1} vs {f2}")
    plt.show()


if __name__ == "__main__":
    main()