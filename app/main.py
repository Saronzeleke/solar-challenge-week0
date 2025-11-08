import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils import load_data, calculate_statistics, perform_statistical_tests

# Page configuration
st.set_page_config(
    page_title="Solar Potential Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .country-ranking {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">☀️ West Africa Solar Potential Analysis</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Unable to load data. Please check if the CSV files exist in the data/ folder.")
        return
    
    # Sidebar
    st.sidebar.title("Dashboard Controls")
    
    # Country selection
    selected_countries = st.sidebar.multiselect(
        "Select Countries:",
        options=df['Country'].unique(),
        default=df['Country'].unique()
    )
    
    # Metric selection
    selected_metric = st.sidebar.selectbox(
        "Select Solar Metric:",
        options=['GHI', 'DNI', 'DHI'],
        index=0
    )
    
    # Filter data based on selection
    filtered_df = df[df['Country'].isin(selected_countries)]
    
    if filtered_df.empty:
        st.warning("Please select at least one country to display data.")
        return
    
    # Main dashboard layout
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader(f"{selected_metric} Distribution by Country")
        
        # Interactive boxplot
        fig = px.box(
            filtered_df, 
            x='Country', 
            y=selected_metric,
            color='Country',
            points="all",
            hover_data=filtered_df.columns
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Country",
            yaxis_title=f"{selected_metric} (W/m²)",
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Key Statistics")
        
        # Calculate and display statistics
        stats = calculate_statistics(filtered_df, selected_metric)
        
        for country in selected_countries:
            country_stats = stats[stats['Country'] == country].iloc[0]
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>{country}</h4>
                <p><strong>Mean:</strong> {country_stats['Mean']:.1f} W/m²</p>
                <p><strong>Median:</strong> {country_stats['Median']:.1f} W/m²</p>
                <p><strong>Std Dev:</strong> {country_stats['Std_Dev']:.1f} W/m²</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
    
    with col3:
        st.subheader("Country Ranking")
        
        # Ranking based on selected metric
        ranking = filtered_df.groupby('Country')[selected_metric].mean().sort_values(ascending=False)
        
        ranking_html = "<div class='country-ranking'>"
        for i, (country, value) in enumerate(ranking.items(), 1):
            medal = ""
            if i == 1: medal = "🥇"
            elif i == 2: medal = "🥈" 
            elif i == 3: medal = "🥉"
            
            ranking_html += f"<p><strong>{medal} {i}. {country}:</strong> {value:.1f} W/m²</p>"
        ranking_html += "</div>"
        
        st.markdown(ranking_html, unsafe_allow_html=True)
    
    # Second row: Comparative analysis
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Comparative Analysis")
        
        # Bar chart comparing averages
        avg_metrics = filtered_df.groupby('Country')[['GHI', 'DNI', 'DHI']].mean()
        
        fig = go.Figure()
        
        for metric in ['GHI', 'DNI', 'DHI']:
            fig.add_trace(go.Bar(
                name=metric,
                x=avg_metrics.index,
                y=avg_metrics[metric],
                hovertemplate=f"{metric}: %{{y:.1f}} W/m²<extra></extra>"
            ))
        
        fig.update_layout(
            barmode='group',
            height=400,
            title="Average Solar Metrics by Country",
            xaxis_title="Country",
            yaxis_title="Solar Radiation (W/m²)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Statistical Significance")
        
        if len(selected_countries) >= 2:
            test_results = perform_statistical_tests(filtered_df, selected_countries)
            
            st.markdown("""
            <div class="metric-card">
                <h4>Hypothesis Testing Results</h4>
            """, unsafe_allow_html=True)
            
            for metric, result in test_results.items():
                st.write(f"**{metric}:**")
                st.write(f"Test: {result['test']}")
                st.write(f"P-value: {result['p_value']:.6f}")
                
                if result['p_value'] < 0.05:
                    st.success("Significant differences detected (p < 0.05)")
                else:
                    st.info("No significant differences (p ≥ 0.05)")
                
                st.write("---")
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Select at least 2 countries for statistical testing")
    
    # Third row: Data overview
    st.markdown("---")
    st.subheader("Data Overview")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Show filtered data
        st.write(f"Displaying {len(filtered_df)} records from {len(selected_countries)} countries")
        st.dataframe(
            filtered_df[['Country', 'GHI', 'DNI', 'DHI']].head(100),
            use_container_width=True
        )
    
    with col2:
        st.subheader("Quick Insights")
        
        # Generate quick insights
        best_ghi_country = filtered_df.groupby('Country')['GHI'].mean().idxmax()
        best_ghi_value = filtered_df.groupby('Country')['GHI'].mean().max()
        
        best_dni_country = filtered_df.groupby('Country')['DNI'].mean().idxmax()
        best_dni_value = filtered_df.groupby('Country')['DNI'].mean().max()
        
        st.markdown(f"""
        <div class="metric-card">
            <p>🏆 <strong>Best GHI:</strong> {best_ghi_country} ({best_ghi_value:.1f} W/m²)</p>
            <p>🎯 <strong>Best DNI:</strong> {best_dni_country} ({best_dni_value:.1f} W/m²)</p>
            <p>📊 <strong>Total Records:</strong> {len(filtered_df):,}</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()