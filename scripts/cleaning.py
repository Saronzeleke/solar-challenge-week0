
import pandas as pd
import numpy as np
from scipy import stats

def clean_numeric(df, numeric_cols, z_thresh=3):
    """
    Clean numeric columns:
    - Remove outliers using Z-score
    - Impute missing values with median

    Parameters:
        df (pd.DataFrame): input dataframe
        numeric_cols (list): numeric columns to clean
        z_thresh (float): Z-score threshold to detect outliers

    Returns:
        pd.DataFrame: cleaned dataframe
    """
    df_clean = df.copy()

    # Compute Z-scores
    z_scores = np.abs(stats.zscore(df_clean[numeric_cols], nan_policy='omit'))
    outliers = (z_scores > z_thresh).any(axis=1)
    print(f"Outliers detected: {outliers.sum()} rows")

    # Remove outliers
    df_clean = df_clean[~outliers]

    # Impute missing values with median
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())

    return df_clean

def detect_high_missing(df, threshold=5):
    """
    Identify columns with more than threshold % missing values.

    Parameters:
        df (pd.DataFrame)
        threshold (float): percent

    Returns:
        pd.Series
    """
    high_missing = (df.isna().mean() * 100)[(df.isna().mean() * 100) > threshold]
    return high_missing
