import pandas as pd
import seaborn as sns # type: ignore
import matplotlib.pyplot as plt
from src.describe import db

def main():
    numeric_cols = [col for col in db.columns 
                    if pd.api.types.is_numeric_dtype(db[col]) and col != "Index"]

    data = db[numeric_cols + ["Hogwarts House"]].dropna()

    sns.pairplot(data, hue="Hogwarts House", diag_kind="hist", plot_kws={"alpha": 0.6})
    plt.show()

if __name__ == "__main__":
    main()
