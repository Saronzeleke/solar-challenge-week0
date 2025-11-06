import matplotlib.pyplot as plt
import seaborn as sns

def plot_time_series(df, cols, timestamp='Timestamp', title="Time Series Plot"):
    """Plot multiple columns over time."""
    plt.figure(figsize=(12,6))
    for col in cols:
        plt.plot(df[timestamp], df[col], label=col)
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.title(title)
    plt.legend()
    plt.show()

def plot_correlation_heatmap(df, cols, title="Correlation Heatmap"):
    """Plot correlation heatmap for selected columns."""
    plt.figure(figsize=(10,6))
    sns.heatmap(df[cols].corr(), annot=True, cmap='coolwarm')
    plt.title(title)
    plt.show()

def plot_scatter(df, x, y, hue=None, size=None, title="Scatter Plot"):
    """Generic scatter plot."""
    plt.figure(figsize=(8,5))
    sns.scatterplot(data=df, x=x, y=y, hue=hue, size=size, alpha=0.5)
    plt.title(title)
    plt.show()

def plot_histograms(df, cols, bins=30, kde=True, title="Histogram"):
    """Plot histograms for multiple columns."""
    n = len(cols)
    fig, axes = plt.subplots(1, n, figsize=(6*n,5))
    if n == 1:
        axes = [axes]
    for i, col in enumerate(cols):
        sns.histplot(df[col], bins=bins, kde=kde, ax=axes[i])
        axes[i].set_title(col)
    plt.suptitle(title)
    plt.show()

def plot_bar(df, x, y_cols, title="Bar Plot"):
    """Grouped bar plot."""
    df.groupby(x)[y_cols].mean().plot(kind='bar', figsize=(8,6))
    plt.title(title)
    plt.show()

def plot_bubble(df, x, y, size_col, title="Bubble Plot"):
    """Bubble chart for two variables and a size metric."""
    plt.figure(figsize=(8,6))
    plt.scatter(df[x], df[y], s=df[size_col], alpha=0.5)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.show()

def plot_wind_rose(df, ws_col='WS', wd_col='WD', bins=16, title="Wind Direction Distribution"):
    """Simplified wind rose using histogram."""
    plt.figure(figsize=(8,6))
    plt.hist(df[wd_col], bins=bins, weights=df[ws_col])
    plt.title(title)
    plt.show()
