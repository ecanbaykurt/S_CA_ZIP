import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Page configuration
st.set_page_config(
    page_title="LA County Zip Code Analysis Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    # Try multiple possible paths
    possible_paths = [
        'LA_County_Analysis_Final_with_Scores.csv',
        os.path.join(os.path.dirname(__file__), 'LA_County_Analysis_Final_with_Scores.csv'),
        os.path.join(os.getcwd(), 'LA_County_Analysis_Final_with_Scores.csv')
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df
    
    # If file not found, raise an error
    raise FileNotFoundError(
        "Could not find 'LA_County_Analysis_Final_with_Scores.csv'. "
        "Please ensure the CSV file is in the same directory as app.py"
    )

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Score category filter
score_categories = ['All'] + sorted(df['score_category'].unique().tolist())
selected_category = st.sidebar.selectbox("Score Category", score_categories)

# City filter
cities = ['All'] + sorted(df['primary_city'].unique().tolist())
selected_city = st.sidebar.selectbox("Primary City", cities)

# Composite score range
min_score = float(df['composite_score'].min())
max_score = float(df['composite_score'].max())
score_range = st.sidebar.slider(
    "Composite Score Range",
    min_value=min_score,
    max_value=max_score,
    value=(min_score, max_score)
)

# Apply filters
filtered_df = df.copy()
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['score_category'] == selected_category]
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['primary_city'] == selected_city]
filtered_df = filtered_df[
    (filtered_df['composite_score'] >= score_range[0]) &
    (filtered_df['composite_score'] <= score_range[1])
]

# Main title
st.title("🏙️ Los Angeles County Zip Code Analysis Dashboard")
st.markdown("---")

# Key Metrics
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Zip Codes", len(filtered_df))
with col2:
    st.metric("Avg Composite Score", f"{filtered_df['composite_score'].mean():.2f}")
with col3:
    st.metric("Avg Median Income", f"${filtered_df['median_income'].mean():,.0f}")
with col4:
    st.metric("Avg Home Value", f"${filtered_df['median_home_value'].mean():,.0f}")
with col5:
    st.metric("Avg Population", f"{filtered_df['estimated_population'].mean():,.0f}")

st.markdown("---")

# Tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "📈 Score Analysis", 
    "💰 Economic Metrics", 
    "🏘️ Demographics", 
    "📋 Data Table"
])

with tab1:
    st.header("Overview Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Score category distribution
        category_counts = filtered_df['score_category'].value_counts()
        fig_pie = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Distribution by Score Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Composite score distribution
        fig_hist = px.histogram(
            filtered_df,
            x='composite_score',
            nbins=30,
            title="Composite Score Distribution",
            labels={'composite_score': 'Composite Score', 'count': 'Number of Zip Codes'},
            color_discrete_sequence=['#1f77b4']
        )
        fig_hist.update_layout(showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Top and bottom zip codes
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 Zip Codes by Composite Score")
        top_10 = filtered_df.nlargest(10, 'composite_score')[
            ['zip_code', 'primary_city', 'composite_score', 'median_income', 'median_home_value']
        ]
        top_10 = top_10.reset_index(drop=True)
        top_10.index = top_10.index + 1
        st.dataframe(top_10, use_container_width=True)
    
    with col2:
        st.subheader("📉 Bottom 10 Zip Codes by Composite Score")
        bottom_10 = filtered_df.nsmallest(10, 'composite_score')[
            ['zip_code', 'primary_city', 'composite_score', 'median_income', 'median_home_value']
        ]
        bottom_10 = bottom_10.reset_index(drop=True)
        bottom_10.index = bottom_10.index + 1
        st.dataframe(bottom_10, use_container_width=True)

with tab2:
    st.header("Score Analysis")
    
    # Score components comparison
    col1, col2 = st.columns(2)
    
    with col1:
        score_cols = ['density_score', 'transit_score', 'income_score', 'education_score', 'housing_score']
        avg_scores = filtered_df[score_cols].mean()
        
        fig_bar = px.bar(
            x=score_cols,
            y=avg_scores.values,
            title="Average Scores by Component",
            labels={'x': 'Score Component', 'y': 'Average Score'},
            color=avg_scores.values,
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Score correlation heatmap
        score_df = filtered_df[['composite_score', 'density_score', 'transit_score', 
                                'income_score', 'education_score', 'housing_score']]
        corr_matrix = score_df.corr()
        
        fig_heatmap = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale='RdBu',
            aspect="auto",
            title="Score Components Correlation Matrix"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Scatter plot: Composite score vs individual scores
    st.subheader("Score Relationships")
    score_x = st.selectbox("X-axis Score", ['density_score', 'transit_score', 'income_score', 
                                            'education_score', 'housing_score'], key='x_score')
    score_y = st.selectbox("Y-axis Score", ['composite_score', 'density_score', 'transit_score', 
                                            'income_score', 'education_score', 'housing_score'], key='y_score')
    
    fig_scatter = px.scatter(
        filtered_df,
        x=score_x,
        y=score_y,
        color='score_category',
        size='estimated_population',
        hover_data=['zip_code', 'primary_city', 'composite_score'],
        title=f"{score_x.replace('_', ' ').title()} vs {score_y.replace('_', ' ').title()}",
        labels={score_x: score_x.replace('_', ' ').title(),
                score_y: score_y.replace('_', ' ').title()}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.header("Economic Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Median income distribution
        fig_income = px.histogram(
            filtered_df,
            x='median_income',
            nbins=30,
            title="Median Income Distribution",
            labels={'median_income': 'Median Income ($)', 'count': 'Number of Zip Codes'},
            color_discrete_sequence=['#2ca02c']
        )
        st.plotly_chart(fig_income, use_container_width=True)
    
    with col2:
        # Median home value distribution
        fig_home = px.histogram(
            filtered_df,
            x='median_home_value',
            nbins=30,
            title="Median Home Value Distribution",
            labels={'median_home_value': 'Median Home Value ($)', 'count': 'Number of Zip Codes'},
            color_discrete_sequence=['#ff7f0e']
        )
        st.plotly_chart(fig_home, use_container_width=True)
    
    # Income vs Home Value
    fig_income_home = px.scatter(
        filtered_df,
        x='median_income',
        y='median_home_value',
        color='composite_score',
        size='estimated_population',
        hover_data=['zip_code', 'primary_city', 'score_category'],
        title="Median Income vs Median Home Value",
        labels={'median_income': 'Median Income ($)',
                'median_home_value': 'Median Home Value ($)',
                'composite_score': 'Composite Score'},
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_income_home, use_container_width=True)
    
    # Top cities by economic metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Cities by Average Income")
        city_income = filtered_df.groupby('primary_city')['median_income'].mean().sort_values(ascending=False).head(10)
        fig_city_income = px.bar(
            x=city_income.values,
            y=city_income.index,
            orientation='h',
            title="Top 10 Cities by Average Median Income",
            labels={'x': 'Average Median Income ($)', 'y': 'City'},
            color=city_income.values,
            color_continuous_scale='Greens'
        )
        fig_city_income.update_layout(showlegend=False)
        st.plotly_chart(fig_city_income, use_container_width=True)
    
    with col2:
        st.subheader("Top Cities by Average Home Value")
        city_home = filtered_df.groupby('primary_city')['median_home_value'].mean().sort_values(ascending=False).head(10)
        fig_city_home = px.bar(
            x=city_home.values,
            y=city_home.index,
            orientation='h',
            title="Top 10 Cities by Average Home Value",
            labels={'x': 'Average Home Value ($)', 'y': 'City'},
            color=city_home.values,
            color_continuous_scale='Oranges'
        )
        fig_city_home.update_layout(showlegend=False)
        st.plotly_chart(fig_city_home, use_container_width=True)

with tab4:
    st.header("Demographics & Location Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Population distribution
        fig_pop = px.histogram(
            filtered_df,
            x='estimated_population',
            nbins=30,
            title="Population Distribution",
            labels={'estimated_population': 'Estimated Population', 'count': 'Number of Zip Codes'},
            color_discrete_sequence=['#9467bd']
        )
        st.plotly_chart(fig_pop, use_container_width=True)
    
    with col2:
        # Population density distribution
        fig_density = px.histogram(
            filtered_df,
            x='population_density',
            nbins=30,
            title="Population Density Distribution",
            labels={'population_density': 'Population Density', 'count': 'Number of Zip Codes'},
            color_discrete_sequence=['#8c564b']
        )
        st.plotly_chart(fig_density, use_container_width=True)
    
    # Public transit usage
    col1, col2 = st.columns(2)
    
    with col1:
        fig_transit = px.histogram(
            filtered_df,
            x='public_transit_pct',
            nbins=30,
            title="Public Transit Usage Distribution",
            labels={'public_transit_pct': 'Public Transit Usage (%)', 'count': 'Number of Zip Codes'},
            color_discrete_sequence=['#e377c2']
        )
        st.plotly_chart(fig_transit, use_container_width=True)
    
    with col2:
        fig_education = px.histogram(
            filtered_df,
            x='education_pct',
            nbins=30,
            title="Education Level Distribution",
            labels={'education_pct': 'Education Level (%)', 'count': 'Number of Zip Codes'},
            color_discrete_sequence=['#7f7f7f']
        )
        st.plotly_chart(fig_education, use_container_width=True)
    
    # Scatter: Population vs Density
    fig_pop_density = px.scatter(
        filtered_df,
        x='estimated_population',
        y='population_density',
        color='composite_score',
        size='median_income',
        hover_data=['zip_code', 'primary_city', 'score_category'],
        title="Population vs Population Density",
        labels={'estimated_population': 'Estimated Population',
                'population_density': 'Population Density',
                'composite_score': 'Composite Score'},
        color_continuous_scale='Plasma'
    )
    st.plotly_chart(fig_pop_density, use_container_width=True)

with tab5:
    st.header("Data Table")
    
    # Search functionality
    search_term = st.text_input("🔍 Search (zip code, city, etc.)", "")
    
    if search_term:
        mask = (
            filtered_df['zip_code'].astype(str).str.contains(search_term, case=False, na=False) |
            filtered_df['primary_city'].str.contains(search_term, case=False, na=False) |
            filtered_df['score_category'].str.contains(search_term, case=False, na=False)
        )
        display_df = filtered_df[mask]
    else:
        display_df = filtered_df.copy()
    
    # Column selection
    default_cols = ['zip_code', 'primary_city', 'composite_score', 'score_category', 
                    'median_income', 'median_home_value', 'estimated_population']
    available_cols = filtered_df.columns.tolist()
    selected_cols = st.multiselect(
        "Select columns to display",
        available_cols,
        default=default_cols
    )
    
    if selected_cols:
        display_df = display_df[selected_cols]
    
    # Display dataframe
    st.dataframe(
        display_df,
        use_container_width=True,
        height=600
    )
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download filtered data as CSV",
        data=csv,
        file_name="filtered_la_county_data.csv",
        mime="text/csv"
    )
    
    # Summary statistics
    st.subheader("Summary Statistics")
    numeric_cols = display_df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        st.dataframe(display_df[numeric_cols].describe(), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Dashboard created for LA County Zip Code Analysis** | Data includes composite scores, economic metrics, and demographic information")

