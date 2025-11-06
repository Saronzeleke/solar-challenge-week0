import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation(df, cols):
    sns.heatmap(df[cols].corr(), annot=True, cmap='coolwarm')
    plt.show()

def plot_time_series(df, cols, timestamp_col='Timestamp'):
    plt.figure(figsize=(12,6))
    for col in cols:
        plt.plot(df[timestamp_col], df[col], label=col)
    plt.legend()
    plt.show()
