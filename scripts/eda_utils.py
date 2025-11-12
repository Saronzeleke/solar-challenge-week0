<<<<<<< HEAD

import pandas as pd
from scipy.stats import skew, kurtosis

def summary_stats(df, numeric_cols):
    """Return descriptive statistics for numeric columns."""
    return df[numeric_cols].describe()

def missing_values_report(df):
    """Return missing values count and percentage for each column."""
    missing_count = df.isna().sum()
    missing_pct = df.isna().mean() * 100
    report = pd.DataFrame({'missing_count': missing_count, 'missing_pct': missing_pct})
    return report

def compute_skew_kurtosis(df, cols):
    """Return skewness and kurtosis for selected columns."""
    result = {}
    for col in cols:
        result[col] = {'skew': skew(df[col]), 'kurtosis': kurtosis(df[col])}
    return result

def correlation_matrix(df, cols):
    """Return correlation matrix for selected columns."""
    return df[cols].corr()
=======
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
>>>>>>> eda-togo
