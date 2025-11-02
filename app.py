import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import numpy as np
import ast

# Configure page layout for better space utilization
st.set_page_config(
    page_title="Singapore Tech Job Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for better spacing and layout
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        padding-bottom: 0.5rem;
    }
    h2 {
        padding-top: 1rem;
        padding-bottom: 0.5rem;
    }
    h3 {
        padding-top: 0.5rem;
        padding-bottom: 0.25rem;
    }
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the CSV data
@st.cache_data
def load_data():
    df = pd.read_csv('SGJobData.csv')
    df['metadata_newPostingDate'] = pd.to_datetime(df['metadata_newPostingDate'], errors='coerce')
    df['metadata_originalPostingDate'] = pd.to_datetime(df['metadata_originalPostingDate'], errors='coerce')
    return df

df = load_data()

# Define tech-related keywords
tech_keywords = ['software', 'developer', 'engineer', 'programmer', 'data scientist', 'analyst', 
                 'architect', 'devops', 'backend', 'frontend', 'fullstack', 'full stack',
                 'machine learning', 'ai', 'artificial intelligence', 'cyber', 'security',
                 'cloud', 'database', 'sql', 'python', 'java', 'javascript', 'tech', 'it',
                 'information technology', 'system', 'network', 'infrastructure']

# Filter for tech jobs
def is_tech_job(title):
    if pd.isna(title):
        return False
    title_lower = str(title).lower()
    return any(keyword in title_lower for keyword in tech_keywords)

tech_mask = df['title'].apply(is_tech_job)
tech_df = df[tech_mask].copy()

# Remove rows with invalid dates
tech_df = tech_df[tech_df['metadata_newPostingDate'].notna()].copy()

# Calculate posting recency for sector analysis
tech_df['posting_recency'] = (tech_df['metadata_newPostingDate'] - tech_df['metadata_originalPostingDate']).dt.days

# Create daily_metrics
daily_metrics = tech_df.groupby(tech_df['metadata_newPostingDate'].dt.date).agg({
    'metadata_jobPostId': 'count',
    'numberOfVacancies': lambda x: x.fillna(0).sum()
}).reset_index()
daily_metrics.columns = ['Date', 'Total Postings', 'Total Vacancies']
daily_metrics['Date'] = pd.to_datetime(daily_metrics['Date'])
daily_metrics = daily_metrics.dropna(subset=['Date'])

# Create salary_over_time
salary_df = tech_df[tech_df['salary_minimum'].notna() & tech_df['salary_maximum'].notna()].copy()
salary_over_time = salary_df.groupby(salary_df['metadata_newPostingDate'].dt.date).agg({
    'salary_minimum': 'mean',
    'salary_maximum': 'mean'
}).reset_index()
salary_over_time.columns = ['metadata_newPostingDate', 'salary_minimum', 'salary_maximum']
salary_over_time['metadata_newPostingDate'] = pd.to_datetime(salary_over_time['metadata_newPostingDate'])
salary_over_time = salary_over_time.dropna(subset=['metadata_newPostingDate'])

# Create average_repost_over_time
repost_df = tech_df[tech_df['metadata_repostCount'].notna()].copy()
average_repost_over_time = repost_df.groupby(repost_df['metadata_newPostingDate'].dt.date).agg({
    'metadata_repostCount': 'mean'
}).reset_index()
average_repost_over_time.columns = ['Date', 'Average Repost Count']
average_repost_over_time['Date'] = pd.to_datetime(average_repost_over_time['Date'])
average_repost_over_time = average_repost_over_time.dropna(subset=['Date'])

# Create average_recency_over_time (days between original and new posting date)
recency_df = tech_df[tech_df['posting_recency'].notna()].copy()
average_recency_over_time = recency_df.groupby(recency_df['metadata_newPostingDate'].dt.date).agg({
    'posting_recency': 'mean'
}).reset_index()
average_recency_over_time.columns = ['Date', 'Average Posting Recency']
average_recency_over_time['Date'] = pd.to_datetime(average_recency_over_time['Date'])
average_recency_over_time = average_recency_over_time.dropna(subset=['Date'])

# Create company_tech_job_counts
company_tech_job_counts = tech_df.groupby('postedCompany_name').agg({
    'metadata_jobPostId': 'count'
}).reset_index()
company_tech_job_counts.columns = ['Company', 'Job Count']
company_tech_job_counts = company_tech_job_counts.sort_values('Job Count', ascending=False).reset_index(drop=True)

# Create tech_job_salary_summary
tech_job_salary_summary = tech_df.groupby('title').agg({
    'metadata_jobPostId': 'count',
    'salary_minimum': 'mean',
    'salary_maximum': 'mean'
}).reset_index()
tech_job_salary_summary['Average_Salary'] = (tech_job_salary_summary['salary_minimum'] + tech_job_salary_summary['salary_maximum']) / 2
tech_job_salary_summary.columns = ['Tech Job Title', 'Count', 'Avg_Min_Salary', 'Avg_Max_Salary', 'Average_Salary']
tech_job_salary_summary = tech_job_salary_summary.sort_values('Count', ascending=False).reset_index(drop=True)

# Extract sector from categories by parsing JSON
def extract_first_category(categories_str):
    """Extract the first category name from JSON string."""
    if pd.isna(categories_str) or categories_str == '':
        return 'Unknown'
    try:
        # Parse the JSON string (it's stored as a string representation of a list)
        categories_list = ast.literal_eval(str(categories_str))
        if isinstance(categories_list, list) and len(categories_list) > 0:
            # Get the first category name
            if isinstance(categories_list[0], dict) and 'category' in categories_list[0]:
                return categories_list[0]['category']
        return 'Unknown'
    except (ValueError, SyntaxError, TypeError, KeyError, IndexError):
        # If parsing fails, return Unknown
        return 'Unknown'

if 'categories' in tech_df.columns:
    # Extract readable category names from JSON
    tech_df['Sector'] = tech_df['categories'].apply(extract_first_category)
else:
    tech_df['Sector'] = 'Unknown'

# Create dominant_roles_per_sector
dominant_roles_per_sector = tech_df.groupby(['Sector', 'title']).agg({
    'metadata_jobPostId': 'count'
}).reset_index()
dominant_roles_per_sector.columns = ['Sector', 'Job Title', 'Count']
dominant_roles_per_sector = dominant_roles_per_sector.sort_values(['Sector', 'Count'], ascending=[True, False])
dominant_roles_per_sector = dominant_roles_per_sector.groupby('Sector').head(5).reset_index(drop=True)

# Create sector_postings
sector_postings = tech_df.groupby('Sector').agg({
    'metadata_jobPostId': 'count'
}).reset_index()
sector_postings.columns = ['Sector', 'Total Postings']

# Create sector_growth_trend (using posting recency as age indicator)
sector_recency_df = tech_df[tech_df['posting_recency'].notna()].copy()
sector_growth_trend = sector_recency_df.groupby('Sector').agg({
    'posting_recency': 'mean'
}).reset_index()
sector_growth_trend.columns = ['Sector', 'Average Posting Age']

# Create sector_median_salary
sector_median_salary = tech_df.groupby('Sector').agg({
    'salary_minimum': 'median',
    'salary_maximum': 'median'
}).reset_index()
sector_median_salary['Median Salary'] = (sector_median_salary['salary_minimum'] + sector_median_salary['salary_maximum']) / 2
sector_median_salary = sector_median_salary[['Sector', 'Median Salary']]

# Define dashboard_plan configuration
dashboard_plan = {
    "title": "Singapore Tech Job Market Dashboard",
    "sections": [
        {
            "section_title": "Tech Hiring Overview",
            "description": "Overview of tech job postings and trends",
            "interactive_elements": [
                {
                    "description": "Select Date Range"
                }
            ],
            "visualizations": [
                {"title": "Top 10 Companies by Tech Job Postings"},
                {"title": "Total Job Postings and Vacancies Over Time"},
                {"title": "Average Salary Range Over Time"},
                {"title": "Average Repost Count Over Time"},
                {"title": "Average Posting Recency Over Time"}
            ]
        },
        {
            "section_title": "Tech Job Title Analysis",
            "description": "Analysis of tech job titles and salaries",
            "interactive_elements": [
                {
                    "description": "Select Number of Top Job Titles"
                }
            ],
            "visualizations": [
                {"title": "Top 20 Tech Job Titles by Count and Salary"},
                {"title": "Tech Job Title Count vs. Average Salary (Top 20)"}
            ]
        },
        {
            "section_title": "Industry Dynamics",
            "description": "Analysis of industry sectors and trends",
            "interactive_elements": [
                {
                    "description": "Select Sector to View Dominant Roles"
                },
                {
                    "description": "Select Number of Top Sectors"
                }
            ],
            "visualizations": [
                {"title": "Top 20 Sectors by Total Postings"},
                {"title": "Top 20 Sectors by Average Posting Age"},
                {"title": "Top 20 Sectors by Median Salary"}
            ]
        }
    ]
}

# Set the title of the Streamlit application
st.title(dashboard_plan["title"])

# --- Tech Hiring Overview Section ---
st.header(dashboard_plan["sections"][0]["section_title"])
st.write(dashboard_plan["sections"][0]["description"])

# Date range slider for filtering time series data
date_list = pd.to_datetime(daily_metrics['Date']).tolist()
min_date = min(date_list).date()
max_date = max(date_list).date()

selected_date_range = st.slider(
    dashboard_plan["sections"][0]["interactive_elements"][0]["description"],
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# Convert selected_date_range to datetime objects
start_date = datetime.combine(selected_date_range[0], datetime.min.time())
end_date = datetime.combine(selected_date_range[1], datetime.max.time())

# Filter time series dataframes based on selected date range
filtered_daily_metrics = daily_metrics[
    (pd.to_datetime(daily_metrics['Date']) >= start_date) &
    (pd.to_datetime(daily_metrics['Date']) <= end_date)
]

filtered_salary_over_time = salary_over_time[
    (pd.to_datetime(salary_over_time['metadata_newPostingDate']) >= start_date) &
    (pd.to_datetime(salary_over_time['metadata_newPostingDate']) <= end_date)
]

filtered_average_repost_over_time = average_repost_over_time[
    (pd.to_datetime(average_repost_over_time['Date']) >= start_date) &
    (pd.to_datetime(average_repost_over_time['Date']) <= end_date)
]

filtered_average_recency_over_time = average_recency_over_time[
    (pd.to_datetime(average_recency_over_time['Date']) >= start_date) &
    (pd.to_datetime(average_recency_over_time['Date']) <= end_date)
]


# Layout for Tech Hiring Overview - Optimized grid layout
# First row: Top Companies table (1/3) + Postings chart (2/3)
row1_col1, row1_col2 = st.columns([1, 2])

with row1_col1:
    st.subheader(dashboard_plan["sections"][0]["visualizations"][0]["title"])
    st.dataframe(company_tech_job_counts.head(10), use_container_width=True)

with row1_col2:
    # Plot Total Job Postings and Vacancies Over Time
    fig_postings_vacancies = go.Figure()
    fig_postings_vacancies.add_trace(go.Scatter(x=filtered_daily_metrics['Date'], y=filtered_daily_metrics['Total Postings'], mode='lines', name='Total Postings',
                                             hovertemplate='Date: %{x}<br>Total Postings: %{y}<extra></extra>', fill='tozeroy'))
    fig_postings_vacancies.add_trace(go.Scatter(x=filtered_daily_metrics['Date'], y=filtered_daily_metrics['Total Vacancies'], mode='lines', name='Total Vacancies',
                                             hovertemplate='Date: %{x}<br>Total Vacancies: %{y}<extra></extra>', fill='tonexty'))
    fig_postings_vacancies.update_layout(title=dashboard_plan["sections"][0]["visualizations"][1]["title"], 
                                        xaxis_title='Date', 
                                        yaxis_title='Count',
                                        height=350)
    st.plotly_chart(fig_postings_vacancies, use_container_width=True)

# Second row: Salary Range and Repost Count side by side
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    # Plot Average Minimum and Maximum Salary Over Time
    fig_salary_range = go.Figure()
    fig_salary_range.add_trace(go.Scatter(x=filtered_salary_over_time['metadata_newPostingDate'], 
                                         y=filtered_salary_over_time['salary_minimum'], 
                                         mode='lines', 
                                         name='Average Minimum Salary',
                                         fill='tozeroy'))
    fig_salary_range.add_trace(go.Scatter(x=filtered_salary_over_time['metadata_newPostingDate'], 
                                         y=filtered_salary_over_time['salary_maximum'], 
                                         mode='lines', 
                                         name='Average Maximum Salary',
                                         fill='tonexty'))
    fig_salary_range.update_layout(title=dashboard_plan["sections"][0]["visualizations"][2]["title"], 
                                  xaxis_title='Date', 
                                  yaxis_title='Salary',
                                  height=350)
    st.plotly_chart(fig_salary_range, use_container_width=True)

with row2_col2:
    # Plot Average Repost Count Over Time
    fig_repost = px.line(filtered_average_repost_over_time, 
                        x='Date', 
                        y='Average Repost Count', 
                        title=dashboard_plan["sections"][0]["visualizations"][3]["title"],
                        hover_data={'Date': True, 'Average Repost Count': ':.2f'})
    fig_repost.update_layout(height=350)
    st.plotly_chart(fig_repost, use_container_width=True)

# Third row: Posting Recency chart (can be full width or half)
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    # Plot Average Posting Recency Over Time
    fig_recency = px.line(filtered_average_recency_over_time, 
                         x='Date', 
                         y='Average Posting Recency', 
                         title=dashboard_plan["sections"][0]["visualizations"][4]["title"],
                         hover_data={'Date': True, 'Average Posting Recency': ':.2f'})
    fig_recency.update_layout(height=350)
    st.plotly_chart(fig_recency, use_container_width=True)

with row3_col2:
    # Add a summary metrics card or keep empty for future expansion
    st.subheader("Quick Stats")
    col1_stat, col2_stat, col3_stat = st.columns(3)
    with col1_stat:
        st.metric("Total Tech Jobs", f"{len(tech_df):,}")
    with col2_stat:
        avg_salary = tech_df[tech_df['salary_minimum'].notna() & tech_df['salary_maximum'].notna()]
        if len(avg_salary) > 0:
            avg_sal = (avg_salary['salary_minimum'].mean() + avg_salary['salary_maximum'].mean()) / 2
            st.metric("Avg Salary", f"${avg_sal:,.0f}")
        else:
            st.metric("Avg Salary", "N/A")
    with col3_stat:
        total_vacancies = tech_df['numberOfVacancies'].fillna(0).sum()
        st.metric("Total Vacancies", f"{total_vacancies:,.0f}")


# --- Tech Job Title Analysis Section ---
st.header(dashboard_plan["sections"][1]["section_title"])
st.write(dashboard_plan["sections"][1]["description"])

# Dropdown for selecting number of top job titles
num_top_titles = st.selectbox(
    dashboard_plan["sections"][1]["interactive_elements"][0]["description"],
    options=[10, 20, 50, 100],
    index=1
)

# Filter tech_job_salary_summary based on dropdown selection
filtered_tech_job_salary_summary = tech_job_salary_summary.head(num_top_titles)

# Layout: Table and Scatter plot side by side
job_title_col1, job_title_col2 = st.columns([1, 1.5])

with job_title_col1:
    st.subheader(dashboard_plan["sections"][1]["visualizations"][0]["title"].replace("20", str(num_top_titles)))
    st.dataframe(filtered_tech_job_salary_summary, use_container_width=True, height=400)

with job_title_col2:
    # Scatter plot of Tech Job Title Count vs. Average Salary
    fig_tech_salary_scatter = px.scatter(filtered_tech_job_salary_summary,
                                         x='Count',
                                         y='Average_Salary',
                                         text='Tech Job Title',
                                         title=dashboard_plan["sections"][1]["visualizations"][1]["title"].replace("20", str(num_top_titles)))
    fig_tech_salary_scatter.update_traces(textposition='top center')
    fig_tech_salary_scatter.update_layout(xaxis_title='Number of Postings', 
                                         yaxis_title='Average Salary', 
                                         hovermode='closest',
                                         height=400)
    st.plotly_chart(fig_tech_salary_scatter, use_container_width=True)


# --- Industry Dynamics Section ---
st.header(dashboard_plan["sections"][2]["section_title"])
st.write(dashboard_plan["sections"][2]["description"])

# Dropdown controls in a row
industry_control_col1, industry_control_col2 = st.columns(2)

with industry_control_col1:
    # Dropdown for selecting a sector to view dominant roles
    # Get sorted list of unique sectors (excluding 'Unknown' if there are other options)
    available_sectors = sorted([s for s in dominant_roles_per_sector['Sector'].unique() if s != 'Unknown'])
    if not available_sectors:  # If only 'Unknown' exists, include it
        available_sectors = ['Unknown']
    elif 'Unknown' in dominant_roles_per_sector['Sector'].unique():  # Add Unknown at the end if it exists
        available_sectors.append('Unknown')
    
    selected_sector = st.selectbox(
        dashboard_plan["sections"][2]["interactive_elements"][0]["description"],
        options=available_sectors,
        index=0 if available_sectors else None
    )

with industry_control_col2:
    # Dropdown for selecting number of top sectors for bar charts
    num_top_sectors = st.selectbox(
        dashboard_plan["sections"][2]["interactive_elements"][1]["description"],
        options=[10, 20, 30, 40],
        index=1
    )

# Filter dominant_roles_per_sector based on selected sector
filtered_dominant_roles = dominant_roles_per_sector[dominant_roles_per_sector['Sector'] == selected_sector]

# Filter sector dataframes based on dropdown selection for number of top sectors
filtered_sector_postings = sector_postings.sort_values(by='Total Postings', ascending=False).head(num_top_sectors)
filtered_sector_growth_trend = sector_growth_trend.sort_values(by='Average Posting Age', ascending=True).head(num_top_sectors)
filtered_sector_median_salary = sector_median_salary.sort_values(by='Median Salary', ascending=False).head(num_top_sectors)

# Layout: Dominant Roles table + first chart side by side
industry_row1_col1, industry_row1_col2 = st.columns([1, 1.5])

with industry_row1_col1:
    # Display Dominant Roles Table for the selected sector
    st.subheader(f"Dominant Roles in '{selected_sector}'")
    st.dataframe(filtered_dominant_roles, use_container_width=True, height=300)

with industry_row1_col2:
    # Plotting Industry Dynamics - Total Postings
    st.subheader(dashboard_plan["sections"][2]["visualizations"][0]["title"].replace("20", str(num_top_sectors)))
    fig_sector_postings = px.bar(filtered_sector_postings, 
                                 x='Sector', 
                                 y='Total Postings', 
                                 title=dashboard_plan["sections"][2]["visualizations"][0]["title"].replace("20", str(num_top_sectors)))
    fig_sector_postings.update_layout(
        xaxis={'categoryorder':'total descending', 'tickangle': -45},
        height=300
    )
    st.plotly_chart(fig_sector_postings, use_container_width=True)

# Layout: Growth trend and Median Salary side by side
industry_row2_col1, industry_row2_col2 = st.columns(2)

with industry_row2_col1:
    st.subheader(dashboard_plan["sections"][2]["visualizations"][1]["title"].replace("20", str(num_top_sectors)))
    fig_sector_growth = px.bar(filtered_sector_growth_trend, 
                              x='Sector', 
                              y='Average Posting Age', 
                              title=dashboard_plan["sections"][2]["visualizations"][1]["title"].replace("20", str(num_top_sectors)))
    fig_sector_growth.update_layout(
        xaxis={'categoryorder':'total ascending', 'tickangle': -45},
        height=350
    )
    st.plotly_chart(fig_sector_growth, use_container_width=True)

with industry_row2_col2:
    st.subheader(dashboard_plan["sections"][2]["visualizations"][2]["title"].replace("20", str(num_top_sectors)))
    fig_sector_salary = px.bar(filtered_sector_median_salary, 
                              x='Sector', 
                              y='Median Salary', 
                              title=dashboard_plan["sections"][2]["visualizations"][2]["title"].replace("20", str(num_top_sectors)))
    fig_sector_salary.update_layout(
        xaxis={'categoryorder':'total descending', 'tickangle': -45},
        height=350
    )
    st.plotly_chart(fig_sector_salary, use_container_width=True)