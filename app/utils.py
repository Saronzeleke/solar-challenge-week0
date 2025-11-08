import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Data Loading & Preparation

def load_data(data_folder='../data'):
    """
    Load and merge cleaned datasets from the specified folder with enhanced timestamp handling.
    """
    try:
        data_files = {
            'Benin': os.path.join(data_folder, r'C:\Users\admin\solar-challenge-week0\data\benin-malanville_clean.csv'),
            'Sierra Leone': os.path.join(data_folder, r'C:\Users\admin\solar-challenge-week0\data\sierraleone-bumbuna_clean.csv'),
            'Togo': os.path.join(data_folder, r'C:\Users\admin\solar-challenge-week0\data\togo-dapaong_qc_clean.csv')
        }
        
        dfs = []
        for country, path in data_files.items():
            if os.path.exists(path):
                df = pd.read_csv(path)
                
                # Enhanced timestamp handling
                if 'Timestamp' in df.columns:
                    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
                
                df['Country'] = country
                dfs.append(df)
                print(f"✅ Loaded {len(df)} records from {country}")
            else:
                print(f"⚠️ Warning: {path} not found.")
        
        if not dfs:
            print("❌ No data files found!")
            return None
            
        merged_df = pd.concat(dfs, ignore_index=True)
        print(f"✅ Successfully merged {len(merged_df)} total records")
        
        return merged_df
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def validate_data(df, required_columns=['GHI', 'DNI', 'DHI', 'Country']):
    """
    Validate data quality and completeness.
    """
    validation_results = {}
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        validation_results['missing_columns'] = missing_columns
        return validation_results
    
    # Check for missing values
    missing_values = df[required_columns].isnull().sum().to_dict()
    validation_results['missing_values'] = missing_values
    
    # Check data types
    data_types = df[required_columns].dtypes.to_dict()
    validation_results['data_types'] = data_types
    
    # Check country distribution
    country_counts = df['Country'].value_counts().to_dict()
    validation_results['country_counts'] = country_counts
    
    # Basic statistics validation
    basic_stats = {}
    for col in ['GHI', 'DNI', 'DHI']:
        if col in df.columns:
            basic_stats[col] = {
                'min': df[col].min(),
                'max': df[col].max(),
                'mean': df[col].mean(),
                'std': df[col].std()
            }
    validation_results['basic_stats'] = basic_stats
    
    return validation_results

# Statistics Calculation

def calculate_statistics(df, metric):
    """
    Calculate comprehensive summary statistics for a given metric, grouped by country.
    Returns a DataFrame with enhanced statistics.
    """
    stats_list = []
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country][metric].dropna()
        
        if len(country_data) > 0:
            stats_dict = {
                'Country': country,
                'Metric': metric,
                'Mean': country_data.mean(),
                'Median': country_data.median(),
                'Std_Dev': country_data.std(),
                'Min': country_data.min(),
                'Max': country_data.max(),
                'Count': len(country_data),
                'Q1': country_data.quantile(0.25),
                'Q3': country_data.quantile(0.75),
                'IQR': country_data.quantile(0.75) - country_data.quantile(0.25),
                'CV': (country_data.std() / country_data.mean()) * 100 if country_data.mean() != 0 else 0,
                'Missing_Percentage': (df[df['Country'] == country][metric].isnull().sum() / len(df[df['Country'] == country])) * 100
            }
            stats_list.append(stats_dict)
    
    return pd.DataFrame(stats_list)

def calculate_correlation_matrix(df, metrics=['GHI', 'DNI', 'DHI']):
    """
    Calculate and return correlation matrix with p-values.
    """
    corr_matrix = df[metrics].corr()
    
    # Calculate p-values for correlations
    n = len(df)
    p_matrix = pd.DataFrame(np.zeros((len(metrics), len(metrics))), 
                           index=metrics, columns=metrics)
    
    for i in range(len(metrics)):
        for j in range(len(metrics)):
            if i != j:
                corr_coef = corr_matrix.iloc[i, j]
                t_stat = (corr_coef * np.sqrt(n - 2)) / np.sqrt(1 - corr_coef**2)
                p_value = 2 * (1 - stats.t.cdf(np.abs(t_stat), n - 2))
                p_matrix.iloc[i, j] = p_value
    
    return corr_matrix, p_matrix

# Statistical Testing

def perform_statistical_tests(df, countries):
    """
    Performs ANOVA or Kruskal-Wallis tests for GHI, DNI, DHI between selected countries.
    Returns enhanced results with effect sizes and confidence intervals.
    """
    metrics = ['GHI', 'DNI', 'DHI']
    results = {}
    
    for metric in metrics:
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
                'significant': False, 
                'posthoc': None,
                'effect_size': None,
                'groups': len(groups)
            }
            continue
        
        # Check normality using Shapiro-Wilk test
        normality_pvals = [stats.shapiro(g)[1] for g in groups]
        normal_distribution = all(p > 0.05 for p in normality_pvals)
        
        # Check homogeneity of variances using Levene's test
        levene_stat, levene_p = stats.levene(*groups) if len(groups) > 1 else (None, None)
        equal_variances = levene_p > 0.05 if levene_p is not None else True
        
        if normal_distribution and equal_variances:
            # Perform ANOVA
            f_stat, p_value = stats.f_oneway(*groups)
            test_used = 'ANOVA'
            
            # Calculate effect size (Eta squared)
            ss_between = sum(len(g) * (np.mean(g) - np.mean(np.concatenate(groups)))**2 for g in groups)
            ss_total = sum((np.concatenate(groups) - np.mean(np.concatenate(groups)))**2)
            effect_size = ss_between / ss_total if ss_total != 0 else 0
            
        else:
            # Perform Kruskal-Wallis test
            h_stat, p_value = stats.kruskal(*groups)
            test_used = 'Kruskal-Wallis'
            
            # Calculate effect size (Epsilon squared)
            n_total = sum(len(g) for g in groups)
            effect_size = (h_stat - len(groups) + 1) / (n_total - len(groups)) if (n_total - len(groups)) != 0 else 0
        
        significant = p_value < 0.05
        posthoc = None
        
        if significant and len(groups) > 1:
            # Prepare data for Tukey HSD
            combined = pd.concat([pd.Series(g) for g in groups], ignore_index=True)
            labels = []
            for i, g in enumerate(groups):
                labels.extend([valid_countries[i]] * len(g))
            
            try:
                posthoc = pairwise_tukeyhsd(combined, labels, alpha=0.05)
            except Exception as e:
                print(f"Post-hoc test failed for {metric}: {e}")
                posthoc = None
        
        results[metric] = {
            'test': test_used,
            'p_value': p_value,
            'significant': significant,
            'posthoc': posthoc,
            'effect_size': effect_size,
            'groups': len(groups),
            'normality_pvals': normality_pvals,
            'equal_variances': equal_variances
        }
    
    return results

# Visualization Data Preparation

def prepare_radar_data(df, metrics=['GHI', 'DNI', 'DHI']):
    """
    Normalizes metrics per country for radar chart visualization.
    Returns both normalized and actual values.
    """
    avg_metrics = df.groupby('Country')[metrics].mean()
    normalized = avg_metrics.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)
    
    return {
        'normalized': normalized,
        'actual': avg_metrics
    }

def prepare_comparative_data(df, metrics=['GHI', 'DNI', 'DHI']):
    """
    Prepare data for comparative visualizations.
    """
    comparative_data = {}
    
    for metric in metrics:
        comparative_data[metric] = {}
        for country in df['Country'].unique():
            country_data = df[df['Country'] == country][metric].dropna()
            comparative_data[metric][country] = {
                'values': country_data,
                'mean': country_data.mean(),
                'std': country_data.std(),
                'count': len(country_data)
            }
    
    return comparative_data

# Country Ranking & Insights

def get_country_ranking(df, metric='GHI'):
    """
    Returns enhanced country ranking with confidence intervals.
    """
    ranking_data = []
    
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country][metric].dropna()
        if len(country_data) > 0:
            mean_val = country_data.mean()
            std_val = country_data.std()
            n = len(country_data)
            
            # Calculate 95% confidence interval
            ci_low, ci_high = stats.t.interval(0.95, n-1, loc=mean_val, scale=std_val/np.sqrt(n))
            
            ranking_data.append({
                'country': country,
                'mean': mean_val,
                'std': std_val,
                'count': n,
                'ci_low': ci_low,
                'ci_high': ci_high,
                'ci_width': ci_high - ci_low
            })
    
    ranking_df = pd.DataFrame(ranking_data)
    ranking_df = ranking_df.sort_values('mean', ascending=False).reset_index(drop=True)
    
    return ranking_df

def quick_insights(df):
    """
    Generates comprehensive key insights with statistical backing.
    """
    insights = {}
    
    # Basic insights
    insights['total_records'] = len(df)
    insights['countries_analyzed'] = df['Country'].nunique()
    insights['date_range'] = {
        'start': df['Timestamp'].min() if 'Timestamp' in df.columns else None,
        'end': df['Timestamp'].max() if 'Timestamp' in df.columns else None
    }
    
    # Metric-specific insights
    for metric in ['GHI', 'DNI', 'DHI']:
        ranking = get_country_ranking(df, metric)
        if not ranking.empty:
            insights[metric] = {
                'best_country': ranking.iloc[0]['country'],
                'best_value': ranking.iloc[0]['mean'],
                'worst_country': ranking.iloc[-1]['country'],
                'worst_value': ranking.iloc[-1]['mean'],
                'performance_gap': ranking.iloc[0]['mean'] - ranking.iloc[-1]['mean'],
                'ranking': ranking[['country', 'mean']].to_dict('records')
            }
    
    # Data quality insights
    missing_analysis = {}
    for metric in ['GHI', 'DNI', 'DHI']:
        missing_count = df[metric].isnull().sum()
        missing_analysis[metric] = {
            'missing_count': missing_count,
            'missing_percentage': (missing_count / len(df)) * 100
        }
    insights['data_quality'] = missing_analysis
    
    # Statistical significance insights
    countries = df['Country'].unique().tolist()
    test_results = perform_statistical_tests(df, countries)
    insights['statistical_tests'] = test_results
    
    return insights

# Export Functions

def export_summary_table(df, metrics=['GHI', 'DNI', 'DHI'], filename='summary_statistics.csv'):
    """
    Exports comprehensive summary statistics table to CSV for reporting.
    """
    summary_list = []
    for metric in metrics:
        stats_df = calculate_statistics(df, metric)
        summary_list.append(stats_df)
    
    summary = pd.concat(summary_list, ignore_index=True)
    
    # Enhanced formatting
    summary['Mean'] = summary['Mean'].round(3)
    summary['Std_Dev'] = summary['Std_Dev'].round(3)
    summary['CV'] = summary['CV'].round(1)
    
    summary.to_csv(filename, index=False)
    print(f"✅ Summary table exported to {filename}")
    return summary

def export_visualization_data(df, output_dir='../figures'):
    """
    Export processed data for visualizations.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Export radar chart data
    radar_data = prepare_radar_data(df)
    radar_data['actual'].to_csv(os.path.join(output_dir, 'radar_actual_values.csv'))
    radar_data['normalized'].to_csv(os.path.join(output_dir, 'radar_normalized_values.csv'))
    
    # Export country rankings
    for metric in ['GHI', 'DNI', 'DHI']:
        ranking = get_country_ranking(df, metric)
        ranking.to_csv(os.path.join(output_dir, f'ranking_{metric.lower()}.csv'), index=False)
    
    # Export correlation matrix
    corr_matrix, p_matrix = calculate_correlation_matrix(df)
    corr_matrix.to_csv(os.path.join(output_dir, 'correlation_matrix.csv'))
    p_matrix.to_csv(os.path.join(output_dir, 'correlation_pvalues.csv'))
    
    print(f"✅ Visualization data exported to {output_dir}")

# Streamlit-Specific Utilities

def create_interactive_boxplot(df, metric, selected_countries):
    """
    Create interactive boxplot for Streamlit dashboard.
    """
    filtered_df = df[df['Country'].isin(selected_countries)]
    
    fig = px.box(
        filtered_df, 
        x='Country', 
        y=metric,
        color='Country',
        points="all",
        title=f'{metric} Distribution by Country',
        hover_data=['Country', metric]
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        xaxis_title="Country",
        yaxis_title=f"{metric} (W/m²)",
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    # Add mean markers
    means = filtered_df.groupby('Country')[metric].mean()
    for i, (country, mean_val) in enumerate(means.items()):
        fig.add_annotation(
            x=country,
            y=mean_val,
            text=f"Mean: {mean_val:.1f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="red",
            bgcolor="white",
            bordercolor="red",
            borderwidth=1,
            borderpad=4
        )
    
    return fig

def create_interactive_radar(df, selected_countries):
    """
    Create interactive radar chart for Streamlit dashboard.
    """
    radar_data = prepare_radar_data(df)
    normalized_data = radar_data['normalized']
    actual_data = radar_data['actual']
    
    # Filter selected countries
    normalized_data = normalized_data.loc[selected_countries]
    actual_data = actual_data.loc[selected_countries]
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set3
    
    for i, (country, row) in enumerate(normalized_data.iterrows()):
        values = row.values.tolist()
        values += values[:1]  # Complete the circle
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=normalized_data.columns.tolist() + [normalized_data.columns[0]],
            fill='toself',
            name=country,
            line=dict(color=colors[i % len(colors)], width=2),
            hoverinfo='text',
            hovertext=[f"{metric}: {actual_data.loc[country, metric]:.1f} W/m²" 
                      for metric in normalized_data.columns] + 
                     [f"{normalized_data.columns[0]}: {actual_data.loc[country, normalized_data.columns[0]]:.1f} W/m²"]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                ticktext=['0', '0.2', '0.4', '0.6', '0.8', '1.0'],
                ticks="outside"
            )
        ),
        showlegend=True,
        title="Normalized Solar Metrics Radar Chart",
        height=500
    )
    
    return fig

def create_correlation_heatmap(df):
    """
    Create interactive correlation heatmap for Streamlit.
    """
    corr_matrix, p_matrix = calculate_correlation_matrix(df)
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu_r',
        zmin=-1,
        zmax=1,
        hoverongaps=False,
        text=corr_matrix.round(3).values,
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Solar Metric Correlation Matrix',
        xaxis_title='Metrics',
        yaxis_title='Metrics',
        height=400,
        width=500
    )
    
    return fig