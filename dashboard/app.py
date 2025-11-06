import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import logging
import html
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="SG Salary Benchmarking Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Data validation
def validate_salary_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate salary data from CSV file.

    Args:
        df: Raw dataframe from CSV

    Returns:
        pd.DataFrame: Validated dataframe

    Raises:
        ValueError: If data validation fails
    """
    required_columns = ['salary_minimum', 'salary_maximum', 'categories', 'title']
    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        error_msg = f"Missing required columns: {', '.join(missing_cols)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Check for invalid salary ranges
    invalid_salaries = df[df['salary_minimum'] > df['salary_maximum']]
    if not invalid_salaries.empty:
        logger.warning(f"Found {len(invalid_salaries)} rows with invalid salary ranges. These will be filtered.")
        df = df[df['salary_minimum'] <= df['salary_maximum']]

    logger.info(f"Data validation passed. Total rows: {len(df)}")
    return df

# Load data
@st.cache_data
def load_data():
    """Load and preprocess the data"""
    try:
        data_file = Path('../data/SGJobData.csv')
        if not data_file.exists():
            error_msg = f"Data file not found: {data_file}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        logger.info(f"Loading data from {data_file}")
        df = pd.read_csv(data_file, encoding='utf-8-sig')

        # Validate data
        df = validate_salary_data(df)

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        st.error(f"Data file not found. Please ensure the data file exists at './data/SGJobData.csv'")
        raise
    except pd.errors.EmptyDataError as e:
        logger.error(f"Empty data file: {e}")
        st.error("Data file is empty")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        st.error(f"Error loading data: {str(e)}")
        raise

    # Parse categories
    def extract_primary_category(categories_str):
        try:
            if pd.isna(categories_str):
                return 'Unknown'
            categories = json.loads(categories_str)
            if categories and len(categories) > 0:
                category = str(categories[0].get('category', 'Unknown'))
                return category
            return 'Unknown'
        except (json.JSONDecodeError, TypeError, KeyError, IndexError) as e:
            logger.debug(f"Failed to parse categories: {e}, input: {categories_str}")
            return 'Unknown'

    df['primary_category'] = df['categories'].apply(extract_primary_category)

    # Convert dates
    try:
        date_columns = ['metadata_expiryDate', 'metadata_newPostingDate', 'metadata_originalPostingDate']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        logger.info("Date conversion completed")
    except Exception as e:
        logger.warning(f"Error converting dates: {e}")

    # Calculate salary metrics
    try:
        df['salary_average'] = (df['salary_minimum'] + df['salary_maximum']) / 2
        df['salary_range'] = df['salary_maximum'] - df['salary_minimum']
        logger.info("Salary metrics calculated")
    except Exception as e:
        logger.error(f"Error calculating salary metrics: {e}")
        raise

    # Fill missing values
    df['positionLevels'] = df['positionLevels'].fillna('Not Specified')
    df['minimumYearsExperience'] = df['minimumYearsExperience'].fillna(0)

    # Filter monthly salaries and remove extreme outliers
    if 'salary_type' in df.columns:
        df_monthly = df[df['salary_type'] == 'Monthly'].copy()
    else:
        logger.warning("'salary_type' column not found, using all data")
        df_monthly = df.copy()

    initial_count = len(df_monthly)
    df_monthly = df_monthly[
        (df_monthly['salary_minimum'] >= 1000) &
        (df_monthly['salary_maximum'] <= 50000)
    ].copy()
    filtered_count = initial_count - len(df_monthly)

    logger.info(f"Data loaded successfully. Total rows: {len(df_monthly)}, Outliers removed: {filtered_count}")

    return df_monthly

# Load the data
try:
    df = load_data()
    logger.info("Dashboard data loaded successfully")
except Exception as e:
    logger.critical(f"Failed to load dashboard data: {e}")
    st.error("Failed to load data. Please check the logs for details.")
    st.stop()

# Sidebar - Filters
st.sidebar.title("🔍 Filters")

# Category filter
categories = ['All'] + sorted(df['primary_category'].unique().tolist())
selected_category = st.sidebar.selectbox("Job Category", categories)

# Position level filter
positions = ['All'] + sorted(df['positionLevels'].unique().tolist())
selected_position = st.sidebar.selectbox("Position Level", positions)

# Experience filter
min_exp, max_exp = st.sidebar.slider(
    "Years of Experience",
    min_value=int(df['minimumYearsExperience'].min()),
    max_value=int(df['minimumYearsExperience'].max()),
    value=(int(df['minimumYearsExperience'].min()), int(df['minimumYearsExperience'].max()))
)

# Salary filter
min_sal, max_sal = st.sidebar.slider(
    "Salary Range (SGD)",
    min_value=int(df['salary_average'].min()),
    max_value=int(df['salary_average'].max()),
    value=(int(df['salary_average'].min()), int(df['salary_average'].max()))
)

# Apply filters
filtered_df = df.copy()

if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['primary_category'] == selected_category]

if selected_position != 'All':
    filtered_df = filtered_df[filtered_df['positionLevels'] == selected_position]

filtered_df = filtered_df[
    (filtered_df['minimumYearsExperience'] >= min_exp) &
    (filtered_df['minimumYearsExperience'] <= max_exp) &
    (filtered_df['salary_average'] >= min_sal) &
    (filtered_df['salary_average'] <= max_sal)
]

# Main content
st.markdown('<p class="main-header">💼 Singapore Salary Benchmarking Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">HR Consulting Firm - Market Intelligence Tool</p>', unsafe_allow_html=True)

# Show filter status
if len(filtered_df) < len(df):
    st.info(f"📊 Showing {len(filtered_df):,} jobs out of {len(df):,} total postings based on your filters")

# Key Metrics
st.markdown("### 📈 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Jobs",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df):,}" if len(filtered_df) != len(df) else None
    )

with col2:
    st.metric(
        label="Median Salary",
        value=f"${filtered_df['salary_average'].median():,.0f}",
        delta=f"${filtered_df['salary_average'].median() - df['salary_average'].median():,.0f}" if len(filtered_df) != len(df) else None
    )

with col3:
    st.metric(
        label="Mean Salary",
        value=f"${filtered_df['salary_average'].mean():,.0f}",
        delta=f"${filtered_df['salary_average'].mean() - df['salary_average'].mean():,.0f}" if len(filtered_df) != len(df) else None
    )

with col4:
    st.metric(
        label="25th Percentile",
        value=f"${filtered_df['salary_average'].quantile(0.25):,.0f}"
    )

with col5:
    st.metric(
        label="75th Percentile",
        value=f"${filtered_df['salary_average'].quantile(0.75):,.0f}"
    )

# Tabs for different analyses
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "💰 Salary Analysis",
    "🎯 By Category",
    "📈 Experience Impact",
    "🔍 Detailed Insights"
])

with tab1:
    st.markdown("### Salary Distribution Overview")

    col1, col2 = st.columns(2)

    with col1:
        # Histogram
        fig = px.histogram(
            filtered_df,
            x='salary_average',
            nbins=50,
            title="Distribution of Average Salaries",
            labels={'salary_average': 'Average Salary (SGD)', 'count': 'Frequency'},
            color_discrete_sequence=['#1f77b4']
        )
        fig.add_vline(
            x=filtered_df['salary_average'].median(),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Median: ${filtered_df['salary_average'].median():,.0f}"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Box plot
        fig = px.box(
            filtered_df,
            y='salary_average',
            title="Salary Distribution (Box Plot)",
            labels={'salary_average': 'Average Salary (SGD)'},
            color_discrete_sequence=['#2ca02c']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Position level distribution
    st.markdown("### Job Distribution by Position Level")
    position_counts = filtered_df['positionLevels'].value_counts().reset_index()
    position_counts.columns = ['Position Level', 'Count']

    fig = px.bar(
        position_counts,
        x='Position Level',
        y='Count',
        title="Number of Positions by Level",
        color='Count',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Salary Analysis by Position Level")

    # Salary by position
    salary_by_position = filtered_df.groupby('positionLevels').agg({
        'salary_average': ['mean', 'median', 'count']
    }).reset_index()
    salary_by_position.columns = ['Position Level', 'Mean Salary', 'Median Salary', 'Count']
    salary_by_position = salary_by_position.sort_values('Median Salary', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            salary_by_position,
            y='Position Level',
            x='Median Salary',
            orientation='h',
            title="Median Salary by Position Level",
            labels={'Median Salary': 'Median Salary (SGD)'},
            color='Median Salary',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Detailed box plot by position
        fig = px.box(
            filtered_df,
            y='positionLevels',
            x='salary_average',
            orientation='h',
            title="Salary Distribution by Position Level",
            labels={'salary_average': 'Average Salary (SGD)', 'positionLevels': 'Position Level'},
            color='positionLevels'
        )
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Show table
    st.markdown("#### Detailed Statistics by Position Level")
    st.dataframe(
        salary_by_position.style.format({
            'Mean Salary': '${:,.0f}',
            'Median Salary': '${:,.0f}',
            'Count': '{:,}'
        }),
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.markdown("### Analysis by Job Category")

    # Top categories by count
    top_categories = filtered_df['primary_category'].value_counts().head(15).reset_index()
    top_categories.columns = ['Category', 'Count']

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            top_categories,
            y='Category',
            x='Count',
            orientation='h',
            title="Top 15 Job Categories by Volume",
            color='Count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Salary by category
        salary_by_category = filtered_df.groupby('primary_category').agg({
            'salary_average': ['mean', 'median'],
            'title': 'count'
        }).reset_index()
        salary_by_category.columns = ['Category', 'Mean Salary', 'Median Salary', 'Count']
        salary_by_category = salary_by_category[salary_by_category['Count'] >= 5]
        salary_by_category = salary_by_category.sort_values('Median Salary', ascending=False).head(15)

        fig = px.bar(
            salary_by_category,
            y='Category',
            x='Median Salary',
            orientation='h',
            title="Top 15 Highest Paying Categories (min 5 jobs)",
            labels={'Median Salary': 'Median Salary (SGD)'},
            color='Median Salary',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    # Category comparison
    st.markdown("#### Salary Statistics by Category")
    category_stats = filtered_df.groupby('primary_category').agg({
        'salary_average': ['mean', 'median', 'std', 'count']
    }).reset_index()
    category_stats.columns = ['Category', 'Mean', 'Median', 'Std Dev', 'Count']
    category_stats = category_stats[category_stats['Count'] >= 5].sort_values('Median', ascending=False)

    st.dataframe(
        category_stats.style.format({
            'Mean': '${:,.0f}',
            'Median': '${:,.0f}',
            'Std Dev': '${:,.0f}',
            'Count': '{:,}'
        }),
        use_container_width=True,
        hide_index=True,
        height=400
    )

with tab4:
    st.markdown("### Impact of Experience on Salary")

    # Salary vs experience scatter plot
    fig = px.scatter(
        filtered_df,
        x='minimumYearsExperience',
        y='salary_average',
        title="Salary vs Years of Experience",
        labels={
            'minimumYearsExperience': 'Minimum Years of Experience',
            'salary_average': 'Average Salary (SGD)'
        },
        opacity=0.5,
        trendline="ols",
        trendline_color_override="red"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Salary by experience brackets
    col1, col2 = st.columns(2)

    with col1:
        salary_by_exp = filtered_df.groupby('minimumYearsExperience').agg({
            'salary_average': ['mean', 'median', 'count']
        }).reset_index()
        salary_by_exp.columns = ['Years', 'Mean', 'Median', 'Count']
        salary_by_exp = salary_by_exp[salary_by_exp['Years'] <= 20]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=salary_by_exp['Years'],
            y=salary_by_exp['Mean'],
            mode='lines+markers',
            name='Mean Salary',
            line=dict(color='blue', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=salary_by_exp['Years'],
            y=salary_by_exp['Median'],
            mode='lines+markers',
            name='Median Salary',
            line=dict(color='green', width=2)
        ))
        fig.update_layout(
            title="Salary Trend by Experience Level",
            xaxis_title="Years of Experience",
            yaxis_title="Salary (SGD)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Calculate correlation
        corr = filtered_df['minimumYearsExperience'].corr(filtered_df['salary_average'])

        st.markdown(f"""
        <div class="insight-box">
            <h4>Experience-Salary Correlation</h4>
            <p style="font-size: 2rem; font-weight: bold; color: #1f77b4; margin: 0;">
                {corr:.3f}
            </p>
            <p>A correlation of {corr:.3f} indicates a {'strong' if abs(corr) > 0.7 else 'moderate' if abs(corr) > 0.4 else 'weak'}
            positive relationship between years of experience and salary.</p>
        </div>
        """, unsafe_allow_html=True)

        # Experience brackets
        experience_brackets = pd.cut(
            filtered_df['minimumYearsExperience'],
            bins=[0, 2, 5, 10, 20, 100],
            labels=['Entry (0-2y)', 'Junior (3-5y)', 'Mid (6-10y)', 'Senior (11-20y)', 'Expert (20+y)']
        )
        filtered_df_exp = filtered_df.copy()
        filtered_df_exp['exp_bracket'] = experience_brackets

        exp_bracket_salary = filtered_df_exp.groupby('exp_bracket', observed=True).agg({
            'salary_average': 'median'
        }).reset_index()

        fig = px.bar(
            exp_bracket_salary,
            x='exp_bracket',
            y='salary_average',
            title="Median Salary by Experience Bracket",
            labels={'exp_bracket': 'Experience Level', 'salary_average': 'Median Salary (SGD)'},
            color='salary_average',
            color_continuous_scale='Teal'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.markdown("### Detailed Insights and Outliers")

    col1, col2 = st.columns(2)

    with col1:
        # Top paying jobs
        st.markdown("#### Top 10 Highest Paying Jobs")
        top_jobs = filtered_df.nlargest(10, 'salary_average')[[
            'title', 'primary_category', 'positionLevels', 'minimumYearsExperience',
            'salary_average', 'postedCompany_name'
        ]].reset_index(drop=True)

        st.dataframe(
            top_jobs.style.format({
                'salary_average': '${:,.0f}',
                'minimumYearsExperience': '{:.0f}'
            }),
            use_container_width=True,
            hide_index=True
        )

    with col2:
        # Salary range analysis
        st.markdown("#### Salary Range Analysis")

        avg_range = filtered_df['salary_range'].mean()
        median_range = filtered_df['salary_range'].median()

        st.markdown(f"""
        <div class="insight-box">
            <h4>Salary Flexibility</h4>
            <p><strong>Average Range:</strong> ${avg_range:,.0f}</p>
            <p><strong>Median Range:</strong> ${median_range:,.0f}</p>
            <p>The salary range indicates negotiation flexibility and skill variance within roles.</p>
        </div>
        """, unsafe_allow_html=True)

        fig = px.scatter(
            filtered_df.sample(min(1000, len(filtered_df))),
            x='salary_average',
            y='salary_range',
            title="Salary Range vs Average Salary",
            labels={
                'salary_average': 'Average Salary (SGD)',
                'salary_range': 'Salary Range (SGD)'
            },
            opacity=0.5
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Market demand vs compensation
    st.markdown("#### Market Demand vs Compensation")

    category_analysis = filtered_df.groupby('primary_category').agg({
        'title': 'count',
        'salary_average': 'median'
    }).reset_index()
    category_analysis.columns = ['Category', 'Job Count', 'Median Salary']
    category_analysis = category_analysis[category_analysis['Job Count'] >= 10].nlargest(20, 'Job Count')

    fig = px.scatter(
        category_analysis,
        x='Job Count',
        y='Median Salary',
        size='Job Count',
        hover_data=['Category'],
        title="Market Demand vs Median Salary by Category",
        labels={
            'Job Count': 'Number of Job Postings',
            'Median Salary': 'Median Salary (SGD)'
        }
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# Recommendations section
st.markdown("---")
st.markdown("### 💡 Key Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="insight-box">
        <h4>1. Market Positioning</h4>
        <p>Use median salary benchmarks by category and position level to advise clients on competitive compensation packages.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-box">
        <h4>2. Experience Premium</h4>
        <p>Clear correlation between experience and salary exists. Recommend structured progression paths to clients.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="insight-box">
        <h4>3. Category Focus</h4>
        <p>High-paying categories should be prioritized for talent acquisition and retention strategies.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Singapore Job Market - Salary Benchmarking Dashboard</p>
        <p>Data Source: MyCareersFuture Singapore | Last Updated: 2023</p>
    </div>
""", unsafe_allow_html=True)