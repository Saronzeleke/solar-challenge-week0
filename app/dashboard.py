import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Solar Data Analysis Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    benin = pd.read_csv(r'C:\Users\admin\solar-challenge-week0\data\benin-malanville_clean.csv')
    sierra_leone = pd.read_csv(r'C:\Users\admin\solar-challenge-week0\data\sierraleone-bumbuna_clean.csv')
    togo = pd.read_csv(r'C:\Users\admin\solar-challenge-week0\data\togo-dapaong_qc_clean.csv')
    
    # Add country identifiers
    benin['Country'] = 'Benin'
    sierra_leone['Country'] = 'Sierra Leone'
    togo['Country'] = 'Togo'
    
    combined = pd.concat([benin, sierra_leone, togo], ignore_index=True)
    combined['Timestamp'] = pd.to_datetime(combined['Timestamp'])
    
    return benin, sierra_leone, togo, combined

# Main app
def main():
    st.title("🌍  Africa Solar Data Analysis Dashboard")
    st.markdown("Interactive exploration of solar irradiation data for Benin, Sierra Leone, and Togo")
    
    # Load data
    benin, sierra_leone, togo, combined = load_data()
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", [
        "Overview", 
        "Country Comparison", 
        "Time Series Analysis",
        "Statistical Tests"
    ])
    
    if page == "Overview":
        show_overview(combined)
    elif page == "Country Comparison":
        show_country_comparison(combined)
    elif page == "Time Series Analysis":
        show_time_series(combined)
    elif page == "Statistical Tests":
        show_statistical_tests(combined)

def show_overview(combined):
    st.header("📊 Project Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", f"{len(combined):,}")
    
    with col2:
        st.metric("Countries", "3")
    
    with col3:
        date_range = f"{combined['Timestamp'].min().strftime('%Y-%m-%d')} to {combined['Timestamp'].max().strftime('%Y-%m-%d')}"
        st.metric("Date Range", date_range)
    
    # Key metrics summary
    st.subheader("Key Metrics Summary")
    
    summary = combined.groupby('Country')[['GHI', 'DNI', 'DHI', 'Tamb']].mean().round(2)
    st.dataframe(summary.style.background_gradient(cmap='Blues'))
    
    # Distribution plots
    st.subheader("Distribution of Solar Parameters")
    
    metric = st.selectbox("Select Metric", ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH'])
    
    fig = px.box(combined, x='Country', y=metric, color='Country',
                 title=f'Distribution of {metric} by Country')
    st.plotly_chart(fig, use_container_width=True)

def show_country_comparison(combined):
    st.header("🌍 Country Comparison")
    
    # Scatter plot comparison
    col1, col2 = st.columns(2)
    
    with col1:
        x_axis = st.selectbox("X-Axis", ['GHI', 'DNI', 'DHI', 'Tamb', 'WS'], index=0)
    with col2:
        y_axis = st.selectbox("Y-Axis", ['GHI', 'DNI', 'DHI', 'Tamb', 'WS'], index=1)
    
    fig = px.scatter(combined, x=x_axis, y=y_axis, color='Country',
                     title=f'{y_axis} vs {x_axis} by Country',
                     opacity=0.6)
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation heatmap
    st.subheader("Correlation Analysis")
    
    selected_country = st.selectbox("Select Country", ['All'] + list(combined['Country'].unique()))
    
    if selected_country == 'All':
        data_for_corr = combined[['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH']]
        title = "Correlation Matrix - All Countries"
    else:
        data_for_corr = combined[combined['Country'] == selected_country][['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH']]
        title = f"Correlation Matrix - {selected_country}"
    
    corr_matrix = data_for_corr.corr()
    
    fig = px.imshow(corr_matrix, 
                    text_auto=True, 
                    aspect="auto",
                    color_continuous_scale='RdBu_r',
                    title=title)
    st.plotly_chart(fig, use_container_width=True)

def show_time_series(combined):
    st.header("📈 Time Series Analysis")
    
    # Aggregate by month for clearer visualization
    combined['YearMonth'] = combined['Timestamp'].dt.to_period('M').astype(str)
    monthly_avg = combined.groupby(['Country', 'YearMonth'])[['GHI', 'DNI', 'DHI']].mean().reset_index()
    
    metric = st.selectbox("Select Solar Metric", ['GHI', 'DNI', 'DHI'])
    
    fig = px.line(monthly_avg, x='YearMonth', y=metric, color='Country',
                  title=f'Monthly Average {metric} Over Time',
                  markers=True)
    fig.update_xaxes(title='Month')
    fig.update_yaxes(title=f'{metric} (W/m²)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Daily patterns
    st.subheader("Daily Patterns")
    
    combined['Hour'] = combined['Timestamp'].dt.hour
    hourly_avg = combined.groupby(['Country', 'Hour'])[['GHI', 'DNI', 'DHI']].mean().reset_index()
    
    fig = px.line(hourly_avg, x='Hour', y=metric, color='Country',
                  title=f'Hourly Average {metric} Pattern',
                  markers=True)
    fig.update_xaxes(title='Hour of Day')
    fig.update_yaxes(title=f'{metric} (W/m²)')
    
    st.plotly_chart(fig, use_container_width=True)

def show_statistical_tests(combined):
    st.header("📊 Statistical Significance Testing")
    
    st.markdown("""
    This section tests whether there are statistically significant differences 
    in solar metrics between the three countries.
    """)
    
    from scipy import stats
    
    metric = st.selectbox("Select Metric for Testing", ['GHI', 'DNI', 'DHI', 'Tamb'])
    
    # Prepare data for ANOVA/Kruskal-Wallis
    country_groups = []
    for country in combined['Country'].unique():
        country_data = combined[combined['Country'] == country][metric].dropna()
        country_groups.append(country_data)
    
    if len(country_groups) >= 2:
        # Test for normality
        normal_test = st.checkbox("Perform normality test (Shapiro-Wilk)")
        
        if normal_test:
            st.subheader("Normality Test Results")
            for i, country in enumerate(combined['Country'].unique()):
                if len(country_groups[i]) > 3:
                    stat, p_value = stats.shapiro(country_groups[i])
                    st.write(f"{country}: p-value = {p_value:.4f} {'(Normal)' if p_value > 0.05 else '(Not Normal)'}")
        
        # Perform statistical test
        test_type = st.radio("Select Statistical Test", 
                           ["ANOVA (parametric)", "Kruskal-Wallis (non-parametric)"])
        
        if st.button("Run Statistical Test"):
            if test_type == "ANOVA (parametric)":
                f_stat, p_value = stats.f_oneway(*country_groups)
                st.subheader("ANOVA Results")
                st.write(f"F-statistic: {f_stat:.4f}")
                st.write(f"P-value: {p_value:.4f}")
            else:
                h_stat, p_value = stats.kruskal(*country_groups)
                st.subheader("Kruskal-Wallis Results")
                st.write(f"H-statistic: {h_stat:.4f}")
                st.write(f"P-value: {p_value:.4f}")
            
            # Interpretation
            st.subheader("Interpretation")
            if p_value < 0.05:
                st.success("✅ **Statistically Significant**: There are significant differences between countries.")
                st.write("This means the observed differences in solar metrics are unlikely due to random chance.")
            else:
                st.warning("❌ **Not Statistically Significant**: No significant differences detected.")
                st.write("The observed differences could be due to random variation.")

if __name__ == "__main__":
    main()