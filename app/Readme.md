## Task 3 – Cross-Country Solar Potential Analysis

## Overview

## Task 3 implements a comparative analysis of solar radiation metrics (GHI, DNI, DHI) across Benin, Sierra Leone, and Togo. The module provides:


**Cleaned and merged datasets across multiple countries.**

**Statistical summary and comparative analysis.**

**Visualizations: boxplots, correlation heatmaps, radar charts.**

**Country-level ranking and actionable solar energy insights.**

**Professional data quality assessment and reporting.**

## Features

**Data Loading: Reads cleaned CSVs and merges them into a unified dataframe.**

**Statistical Analysis: Computes mean, median, standard deviation, and performs significance tests.**

## Visualization:

Comparative boxplots with mean markers.

Correlation heatmaps for solar metrics.

Radar charts with normalized metrics and interactive hover annotations.

Country Ranking & Insights: Automated ranking of countries based on solar potential metrics.

Export Functions: Save professional-quality tables and figures for reporting.

## File Structure

project-root/

├── app/

│   ├── utils.py  
              # Task 3 utility functions (data loading, stats, visualizations)

│   └── Task3_Readme.md  

       # Documentation (this file)

├── data/         
              # Input CSV files (Benin, Sierra Leone, Togo)

├── notebooks/  
                # Jupyter notebooks with analysis and visualizations

│   └── cross_country_analysis.ipynb

│   └──figures/# Generated visualizations (plots, radar charts, heatmaps)     

## Dependencies

Python ≥ 3.10

pandas

numpy

matplotlib

seaborn

scipy

statsmodels

mplcursors (for interactive radar charts)

## Install via:

**pip install pandas numpy matplotlib seaborn scipy statsmodels mplcursors**

## Usage Example

from app.utils import load_data, calculate_statistics, perform_statistical_tests, get_country_ranking, 

prepare_radar_data, quick_insights, export_summary_table

# Load and merge data
merged_df = load_data('data')

# Compute statistics
metrics = ['GHI', 'DNI', 'DHI']

summary_df = calculate_statistics(merged_df, 'GHI')

# Perform statistical tests
test_results = perform_statistical_tests(merged_df, merged_df['Country'].unique().tolist())

# Generate radar chart
radar_data = prepare_radar_data(merged_df)

# Export summary table
export_summary_table(merged_df, filename='summary_statistics.csv')

Data Requirements

CSV files for each country with at least the following columns:

Timestamp – Datetime of measurement

Country – Country name

GHI – Global Horizontal Irradiance (W/m²)

DNI – Direct Normal Irradiance (W/m²)

DHI – Diffuse Horizontal Irradiance (W/m²)

Example filenames: Benin.csv, Sierra_Leone.csv, Togo.csv.

Output

figures/comparative_boxplots.png – Comparative distribution of solar metrics.

figures/correlation_heatmap.png – Correlation heatmap for solar metrics.

figures/radar_comparison.png – Normalized radar chart with interactive annotations.

summary_statistics.csv – Detailed summary table per country and metric.

Key Insights (Generated Automatically)

Highest GHI country → Best for utility-scale PV installations.

Highest DNI country → Optimal for concentrated solar power (CSP) deployment.

Data completeness and reliability reported per country for quality assurance.

Actionable recommendations for phased solar development projects.

## License

This project is released under the MIT License – see LICENSE

 for details.