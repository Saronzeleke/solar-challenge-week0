import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.utils import (
    load_data, calculate_statistics, perform_statistical_tests, 
    get_country_ranking, quick_insights, create_interactive_boxplot,
    create_interactive_radar, create_correlation_heatmap, validate_data
)

# Page configuration
st.set_page_config(
    page_title="Solar Potential Analytics Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        background: linear-gradient(45deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .country-ranking {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #1f77b4;
    }
    .stat-significant {
        color: #28a745;
        font-weight: bold;
        background-color: #d4edda;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
    }
    .stat-not-significant {
        color: #dc3545;
        font-weight: bold;
        background-color: #f8d7da;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .section-header {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def display_welcome():
    """Display welcome message and data overview"""
    st.markdown('<h1 class="main-header">☀️ West Africa Solar Potential Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>📊 Dashboard Overview</h4>
        <p>This interactive dashboard provides comprehensive analysis of solar radiation metrics 
        across Benin, Sierra Leone, and Togo. Compare countries, analyze statistical significance, 
        and identify optimal locations for solar energy projects.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h4>🎯 Key Metrics</h4>
        <p>• <b>GHI</b>: Global Horizontal Irradiance<br>
           • <b>DNI</b>: Direct Normal Irradiance<br>
           • <b>DHI</b>: Diffuse Horizontal Irradiance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-box">
        <h4>🔍 Analysis Features</h4>
        <p>• Comparative Statistics<br>
           • Statistical Testing<br>
           • Interactive Visualizations<br>
           • Country Rankings</p>
        </div>
        """, unsafe_allow_html=True)

def create_comparative_bar_chart(df, countries):
    """Create comparative bar chart with enhanced styling"""
    avg_metrics = df.groupby('Country')[['GHI', 'DNI', 'DHI']].mean()
    avg_metrics = avg_metrics.loc[countries]  
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, metric in enumerate(['GHI', 'DNI', 'DHI']):
        fig.add_trace(go.Bar(
            name=metric,
            x=avg_metrics.index,
            y=avg_metrics[metric],
            marker_color=colors[i],
            hovertemplate=f"<b>%{{x}}</b><br>{metric}: %{{y:.1f}} W/m²<extra></extra>",
            text=avg_metrics[metric].round(1),
            textposition='auto',
        ))
    
    fig.update_layout(
        barmode='group',
        height=500,
        title="Average Solar Metrics by Country",
        xaxis_title="Country",
        yaxis_title="Solar Radiation (W/m²)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    return fig

def display_statistical_results(test_results):
    """Display statistical test results in a professional format"""
    st.markdown("#### 📈 Hypothesis Testing Results")
    
    for metric, result in test_results.items():
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            
            with col1:
                st.write(f"**{metric}**")
            
            with col2:
                if result['p_value'] is not None:
                    st.write(f"**{result['test']}**")
                else:
                    st.write("N/A")
            
            with col3:
                if result['p_value'] is not None:
                    st.write(f"p = {result['p_value']:.4f}")
                else:
                    st.write("N/A")
            
            with col4:
                if result['p_value'] is not None:
                    if result['p_value'] < 0.05:
                        st.markdown('<p class="stat-significant">✅ Statistically Significant</p>', 
                                  unsafe_allow_html=True)
                    else:
                        st.markdown('<p class="stat-not-significant">❌ Not Significant</p>', 
                                  unsafe_allow_html=True)
                else:
                    st.write("Insufficient data")
            
            # Show effect size if available
            if result.get('effect_size') is not None:
                st.write(f"Effect size: {result['effect_size']:.3f}")
            
            st.markdown("---")

def display_country_ranking(df, metric):
    """Display enhanced country ranking with confidence intervals"""
    ranking_df = get_country_ranking(df, metric)
    
    st.markdown(f"#### 🏆 Country Ranking by {metric}")
    
    for i, row in ranking_df.iterrows():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            medal = ""
            if i == 0: medal = "🥇"
            elif i == 1: medal = "🥈" 
            elif i == 2: medal = "🥉"
            st.markdown(f"### {medal}")
        
        with col2:
            st.markdown(f"**{row['country']}**")
            st.write(f"Mean: **{row['mean']:.1f}** W/m²")
            st.write(f"95% CI: [{row['ci_low']:.1f}, {row['ci_high']:.1f}]")
        
        with col3:
            st.metric("Records", f"{row['count']:,}")
        
        if i < len(ranking_df) - 1:
            st.markdown("---")

def main():
    # Display welcome section
    display_welcome()
    
    # Load data with progress indicator
    with st.spinner('Loading and validating solar data...'):
        df = load_data('../data')
    
    if df is None:
        st.error("""
        ❌ Unable to load data. Please ensure the following files exist in the data/ folder:
        - benin_clean.csv
        - sierra_leone_clean.csv  
        - togo_clean.csv
        """)
        return
    
    # Data validation
    validation = validate_data(df)
    if 'missing_columns' in validation:
        st.error(f"Missing required columns: {validation['missing_columns']}")
        return
    
    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Country selection
    available_countries = df['Country'].unique()
    selected_countries = st.sidebar.multiselect(
        "Select Countries:",
        options=available_countries,
        default=available_countries,
        help="Choose countries to include in the analysis"
    )
    
    # Metric selection
    selected_metric = st.sidebar.selectbox(
        "Primary Metric:",
        options=['GHI', 'DNI', 'DHI'],
        index=0,
        help="Select the main solar metric for analysis"
    )
    
    # Analysis type
    analysis_type = st.sidebar.radio(
        "Analysis Focus:",
        ["Comparative Analysis", "Statistical Testing", "Country Rankings"],
        help="Choose the type of analysis to display"
    )
    
    # Filter data based on selection
    filtered_df = df[df['Country'].isin(selected_countries)]
    
    if filtered_df.empty:
        st.warning("Please select at least one country to display data.")
        return
    
    # Display data overview
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Data Overview")
    st.sidebar.write(f"**Total Records:** {len(filtered_df):,}")
    st.sidebar.write(f"**Countries:** {len(selected_countries)}")
    st.sidebar.write(f"**Date Range:** {filtered_df['Timestamp'].min().date() if 'Timestamp' in filtered_df.columns else 'N/A'} to {filtered_df['Timestamp'].max().date() if 'Timestamp' in filtered_df.columns else 'N/A'}")
    
    # Main content based on analysis type
    if analysis_type == "Comparative Analysis":
        display_comparative_analysis(filtered_df, selected_metric, selected_countries)
    elif analysis_type == "Statistical Testing":
        display_statistical_analysis(filtered_df, selected_countries)
    else:  # Country Rankings
        display_ranking_analysis(filtered_df, selected_metric)

def display_comparative_analysis(df, metric, countries):
    """Display comparative analysis section"""
    st.markdown('<div class="section-header">📊 Comparative Analysis</div>', 
                unsafe_allow_html=True)
    
    # First row: Boxplot and Statistics
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(create_interactive_boxplot(df, metric, countries), 
                       use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Key Statistics")
        stats_df = calculate_statistics(df, metric)
        
        for _, row in stats_df[stats_df['Country'].isin(countries)].iterrows():
            st.markdown(f"""
            <div class="metric-card">
                <h4>{row['Country']}</h4>
                <p>📊 Mean: <b>{row['Mean']:.1f}</b> W/m²</p>
                <p>📏 Median: <b>{row['Median']:.1f}</b> W/m²</p>
                <p>📐 Std Dev: <b>{row['Std_Dev']:.1f}</b> W/m²</p>
                <p>📋 Records: <b>{row['Count']:,}</b></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Second row: Comparative charts
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_comparative_bar_chart(df, countries), 
                       use_container_width=True)
    
    with col2:
        st.plotly_chart(create_interactive_radar(df, countries), 
                       use_container_width=True)
    
    # Third row: Correlation heatmap
    st.markdown("---")
    st.markdown("#### 🔗 Metric Correlations")
    st.plotly_chart(create_correlation_heatmap(df), use_container_width=True)

def display_statistical_analysis(df, countries):
    """Display statistical testing section"""
    st.markdown('<div class="section-header">🔬 Statistical Significance Testing</div>', 
                unsafe_allow_html=True)
    
    if len(countries) < 2:
        st.warning("Select at least 2 countries for statistical testing")
        return
    
    # Perform statistical tests
    with st.spinner('Performing statistical tests...'):
        test_results = perform_statistical_tests(df, countries)
    
    # Display results
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_statistical_results(test_results)
    
    with col2:
        st.markdown("#### 📋 Test Information")
        st.markdown("""
        <div class="insight-box">
        <h5>Tests Used:</h5>
        <p><b>ANOVA:</b> Used when data is normally distributed with equal variances</p>
        <p><b>Kruskal-Wallis:</b> Non-parametric alternative when assumptions aren't met</p>
        <p><b>Significance Level:</b> α = 0.05</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick insights from tests
        significant_tests = [metric for metric, result in test_results.items() 
                           if result.get('significant', False)]
        
        if significant_tests:
            st.success(f"**Significant differences found in:** {', '.join(significant_tests)}")
        else:
            st.info("No statistically significant differences detected between selected countries")

def display_ranking_analysis(df, metric):
    """Display country ranking analysis"""
    st.markdown('<div class="section-header">🏆 Country Ranking Analysis</div>', 
                unsafe_allow_html=True)
    
    # Display rankings
    display_country_ranking(df, metric)
    
    # Additional insights
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💡 Key Insights")
        insights = quick_insights(df)
        
        if metric in insights:
            metric_insights = insights[metric]
            st.write(f"**Performance Gap:** {metric_insights['performance_gap']:.1f} W/m²")
            st.write(f"**Best Performer:** {metric_insights['best_country']}")
            st.write(f"**Development Potential:** {metric_insights['worst_country']}")
    
    with col2:
        st.markdown("#### 🎯 Recommendations")
        ranking_df = get_country_ranking(df, metric)
        
        if not ranking_df.empty:
            best_country = ranking_df.iloc[0]['country']
            worst_country = ranking_df.iloc[-1]['country']
            
            st.markdown(f"""
            <div class="insight-box">
            <p>🚀 <b>Priority Investment:</b> {best_country}</p>
            <p>📈 <b>Growth Potential:</b> {worst_country}</p>
            <p>⚡ <b>Technology Focus:</b> Tailor solutions based on DNI/GHI ratios</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()