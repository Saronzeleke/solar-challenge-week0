import pandas as pd
import numpy as np
from scipy import stats

def clean_solar_data(df, numeric_cols):
    z_scores = np.abs(stats.zscore(df[numeric_cols]))
    df_clean = df[~(z_scores > 3).any(axis=1)].copy()
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    return df_clean
