import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from transform import parse_matches

def eda_visualizations():
    df = parse_matches()
    
    # 1. Matches by format
    plt.figure(figsize=(6,4))
    sns.countplot(x="format", data=df)
    plt.title("Matches by Format")
    plt.savefig("../eda/matches_by_format.png")

    # 2. Winners distribution
    plt.figure(figsize=(8,4))
    df['winner'].value_counts().head(10).plot(kind='bar')
    plt.title("Top 10 Winning Teams")
    plt.savefig("../eda/top_winning_teams.png")

if __name__ == "__main__":
    eda_visualizations()
    print("EDA plots saved.")
