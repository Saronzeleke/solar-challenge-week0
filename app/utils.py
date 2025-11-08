import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import os
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Data Loading & Caching
@lru_cache(maxsize=1)
def load_data():
    """
    Load and merge cleaned datasets from the data folder.
    Caches the result to improve performance for Streamlit.
    """
    data_files = {
        'Benin':r'C:\Users\admin\solar-challenge-week0\data\benin-malanville_clean.csv',
        'Sierra Leone':r'C:\Users\admin\solar-challenge-week0\data\sierraleone-bumbuna_clean.csv', 
        'Togo': r'C:\Users\admin\solar-challenge-week0\data\togo-dapaong_qc_clean.csv'
    }
    
    dataframes = []
    for country, file_path in data_files.items():
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                df['Country'] = country
                dataframes.append(df)
                logging.info(f"Loaded {file_path} successfully with {len(df)} rows.")
            except Exception as e:
                logging.error(f"Error loading {file_path}: {e}")
        else:
            logging.warning(f"{file_path} not found.")
    
    if not dataframes:
        logging.error("No datasets loaded. Check your data folder.")
        return None
    
    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df

# Statistics Calculation

def calculate_statistics(df, metric):
    """
    Calculate professional summary statistics for a given metric, grouped by country.
    
    Returns a DataFrame with Mean, Median, Std, Min, Max, Count.
    """
    stats_list = []
    
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country][metric].dropna()
        stats_dict = {
            'Country': country,
            'Mean': country_data.mean(),
            'Median': country_data.median(),
            'Std_Dev': country_data.std(),
            'Min': country_data.min(),
            'Max': country_data.max(),
            'Count': len(country_data)
        }
        stats_list.append(stats_dict)
    
    stats_df = pd.DataFrame(stats_list)
    return stats_df

# Statistical Testing

def perform_statistical_tests(df, countries, metrics=['GHI', 'DNI', 'DHI']):
    """
    Perform ANOVA or Kruskal-Wallis test for each metric across selected countries.
    Returns a dictionary with test results and post-hoc Tukey HSD if significant.
    """
    results = {}
    
    for metric in metrics:
        groups = []
        valid_countries = []
        
        # Prepare data groups
        for country in countries:
            country_data = df[df['Country'] == country][metric].dropna()
            if len(country_data) > 1:
                groups.append(country_data)
                valid_countries.append(country)
        
        # Skip if insufficient data
        if len(groups) < 2:
            results[metric] = {
                'test': 'Insufficient data',
                'p_value': None,
                'significant': False,
                'posthoc': None
            }
            continue
        
        # Normality check
        normality_pvals = [stats.shapiro(group)[1] for group in groups]
        normal_distribution = all(p > 0.05 for p in normality_pvals)
        
        if normal_distribution:
            # Perform one-way ANOVA
            f_stat, p_value = stats.f_oneway(*groups)
            test_used = 'ANOVA'
        else:
            # Kruskal-Wallis for non-normal data
            h_stat, p_value = stats.kruskal(*groups)
            test_used = 'Kruskal-Wallis'
        
        # Prepare post-hoc Tukey HSD if significant
        posthoc_result = None
        if p_value < 0.05:
            combined_data = pd.concat(groups, ignore_index=True)
            country_labels = []
            for i, country in enumerate(valid_countries):
                country_labels.extend([country] * len(groups[i]))
            tukey = pairwise_tukeyhsd(endog=combined_data, groups=country_labels, alpha=0.05)
            posthoc_result = pd.DataFrame(data=tukey._results_table.data[1:], columns=tukey._results_table.data[0])
        
        results[metric] = {
            'test': test_used,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'posthoc': posthoc_result
        }
    
    return results

# Country Ranking
def get_country_ranking(df, metric='GHI', ascending=False):
    """
    Rank countries based on average value of the selected solar metric.
    Returns a pandas Series with countries ordered by metric.
    """
    ranking = df.groupby('Country')[metric].mean().sort_values(ascending=ascending)
    return ranking

# Filtering Helper
def filter_by_country(df, countries):
    """
    Filter dataframe for selected countries.
    """
    return df[df['Country'].isin(countries)]

# Normalized Radar Chart Data

def prepare_radar_data(df, metrics=['GHI', 'DNI', 'DHI']):
    """
    Normalize metrics for radar chart visualization.
    Returns a DataFrame with normalized values (0-1) for each country.
    """
    avg_metrics = df.groupby('Country')[metrics].mean()
    normalized = (avg_metrics - avg_metrics.min()) / (avg_metrics.max() - avg_metrics.min())
    return normalized

# Quick Insights

def quick_insights(df):
    """
    Return dictionary of top-performing countries for key solar metrics.
    """
    insights = {}
    for metric in ['GHI', 'DNI']:
        best_country = df.groupby('Country')[metric].mean().idxmax()
        best_value = df.groupby('Country')[metric].mean().max()
        insights[metric] = {'country': best_country, 'value': best_value}
    insights['total_records'] = len(df)
    insights['countries_analyzed'] = df['Country'].nunique()
    return insights
