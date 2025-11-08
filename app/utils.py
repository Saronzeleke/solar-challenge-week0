import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import os

def load_data():
    """
    Load and merge cleaned datasets from the data folder
    """
    try:
        # Define file paths
        data_files = {
            'Benin': 'data/benin_clean.csv',
            'Sierra Leone': 'data/sierra_leone_clean.csv', 
            'Togo': 'data/togo_clean.csv'
        }
        
        dataframes = []
        
        for country, file_path in data_files.items():
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df['Country'] = country
                dataframes.append(df)
            else:
                print(f"Warning: {file_path} not found")
        
        if not dataframes:
            return None
            
        merged_df = pd.concat(dataframes, ignore_index=True)
        return merged_df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def calculate_statistics(df, metric):
    """
    Calculate summary statistics for the given metric by country
    """
    stats_list = []
    
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country][metric]
        
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
    
    return pd.DataFrame(stats_list)

def perform_statistical_tests(df, countries):
    """
    Perform statistical tests to compare solar metrics between countries
    """
    metrics = ['GHI', 'DNI', 'DHI']
    results = {}
    
    for metric in metrics:
        # Extract data for selected countries
        groups = []
        valid_countries = []
        
        for country in countries:
            country_data = df[df['Country'] == country][metric].dropna()
            if len(country_data) > 0:
                groups.append(country_data)
                valid_countries.append(country)
        
        if len(groups) < 2:
            results[metric] = {
                'test': 'Insufficient data',
                'p_value': None,
                'significant': False
            }
            continue
        
        # Check normality
        normality_pvals = [stats.shapiro(group)[1] for group in groups]
        normal_distribution = all(p > 0.05 for p in normality_pvals)
        
        if normal_distribution:
            # Perform ANOVA
            f_stat, p_value = stats.f_oneway(*groups)
            test_used = "ANOVA"
        else:
            # Perform Kruskal-Wallis test
            h_stat, p_value = stats.kruskal(*groups)
            test_used = "Kruskal-Wallis"
        
        results[metric] = {
            'test': test_used,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    return results

def get_country_ranking(df, metric='GHI'):
    """
    Get country ranking based on average solar metric
    """
    ranking = df.groupby('Country')[metric].mean().sort_values(ascending=False)
    return ranking

def filter_by_country(df, countries):
    """
    Filter dataframe by selected countries
    """
    return df[df['Country'].isin(countries)]