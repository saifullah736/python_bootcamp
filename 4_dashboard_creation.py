"""
Interactive Dashboard Creation for Data Optimiser Recruitment Analysis
This script creates a comprehensive dashboard using Plotly Dash that mimics 
Power BI functionality for the job posting analysis.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import json
from collections import Counter

# Load and prepare data
def load_and_prepare_data():
    """Load and clean the job posting dataset"""
    df = pd.read_csv('job_postings_dataset.csv')
    df['posting_date_clean'] = pd.to_datetime(df['posting_date'])
    df_clean = df.dropna(subset=['job_title', 'company', 'location']).copy()
    
    # Create additional calculated fields
    df_clean['num_skills'] = df_clean['required_skills'].apply(
        lambda x: len(x.split(', ')) if pd.notna(x) else 0
    )
    df_clean['posting_month'] = df_clean['posting_date_clean'].dt.to_period('M').astype(str)
    
    return df_clean

# Data processing functions
def extract_skills_data(df):
    """Extract and count skills from the dataset"""
    all_skills = []
    for skills_str in df['required_skills'].dropna():
        skills_list = [skill.strip() for skill in skills_str.split(',')]
        all_skills.extend(skills_list)
    return Counter(all_skills)

def calculate_salary_benchmarks(df, group_cols):
    """Calculate salary benchmarks for different groups"""
    return df.groupby(group_cols)['salary'].agg([
        'count', 'mean', 'median',
        ('p25', lambda x: x.quantile(0.25)),
        ('p75', lambda x: x.quantile(0.75)),
        ('p90', lambda x: x.quantile(0.90))
    ]).round(0)

# Load data
df_main = load_and_prepare_data()
salary_data = df_main[df_main['salary'].notna()]

# Create Dash app
app = dash.Dash(__name__)
app.title = "Data Optimiser - Job Market Dashboard"

# Define color scheme
colors = {
    'background': '#f8f9fa',
    'text': '#2c3e50',
    'primary': '#3498db',
    'secondary': '#e74c3c',
    'success': '#2ecc71',
    'warning': '#f39c12'
}

# Dashboard layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Data Optimiser: Job Market Intelligence Dashboard", 
                style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': 30}),
        html.P("Comprehensive analysis of data professional job market trends and opportunities",
               style={'textAlign': 'center', 'color': colors['text'], 'fontSize': 18})
    ], style={'backgroundColor': colors['background'], 'padding': '20px'}),
    
    # Key Metrics Row
    html.Div([
        html.Div([
            html.H3(f"{len(df_main):,}", style={'color': colors['primary'], 'margin': 0}),
            html.P("Total Job Postings", style={'margin': 0})
        ], className='metric-card', style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 
                                          'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3(f"${salary_data['salary'].median():,.0f}", style={'color': colors['success'], 'margin': 0}),
            html.P("Median Salary", style={'margin': 0})
        ], className='metric-card', style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white',
                                          'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3(f"{df_main['location'].nunique()}", style={'color': colors['warning'], 'margin': 0}),
            html.P("Markets Covered", style={'margin': 0})
        ], className='metric-card', style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white',
                                          'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3(f"{len(extract_skills_data(df_main))}", style={'color': colors['secondary'], 'margin': 0}),
            html.P("Unique Skills", style={'margin': 0})
        ], className='metric-card', style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white',
                                          'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'})
    ], style={'display': 'grid', 'grid-template-columns': 'repeat(4, 1fr)', 'gap': '20px', 'margin': '20px'}),
    
    # Main Dashboard Tabs
    dcc.Tabs(id='main-tabs', value='overview', children=[
        dcc.Tab(label='Market Overview', value='overview'),
        dcc.Tab(label='Skills Analysis', value='skills'),
        dcc.Tab(label='Salary Benchmarking', value='salary'),
        dcc.Tab(label='Geographic Analysis', value='geographic'),
        dcc.Tab(label='Strategic Insights', value='strategic')
    ], style={'margin': '20px'}),
    
    # Tab content
    html.Div(id='tab-content', style={'margin': '20px'})
])

# Callback for tab content
@app.callback(
    Output('tab-content', 'children'),
    Input('main-tabs', 'value')
)
def render_tab_content(active_tab):
    if active_tab == 'overview':
        return create_overview_tab()
    elif active_tab == 'skills':
        return create_skills_tab()
    elif active_tab == 'salary':
        return create_salary_tab()
    elif active_tab == 'geographic':
        return create_geographic_tab()
    elif active_tab == 'strategic':
        return create_strategic_tab()

def create_overview_tab():
    """Create the market overview tab"""
    # Job distribution pie chart
    job_dist = df_main['job_title'].value_counts()
    fig_pie = px.pie(values=job_dist.values, names=job_dist.index, 
                     title="Job Market Distribution by Role")
    
    # Monthly posting trends
    monthly_data = df_main.groupby(['posting_month', 'job_title']).size().reset_index(name='count')
    fig_trend = px.line(monthly_data, x='posting_month', y='count', color='job_title',
                        title="Job Posting Trends Over Time")
    
    # Company size distribution
    company_dist = df_main['company_size'].value_counts()
    fig_company = px.bar(x=company_dist.index, y=company_dist.values,
                        title="Job Distribution by Company Size")
    
    # Experience level distribution
    exp_dist = df_main['experience_level'].value_counts()
    fig_exp = px.bar(x=exp_dist.index, y=exp_dist.values,
                    title="Job Distribution by Experience Level")
    
    return html.Div([
        html.Div([
            dcc.Graph(figure=fig_pie),
            dcc.Graph(figure=fig_trend)
        ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '20px'}),
        
        html.Div([
            dcc.Graph(figure=fig_company),
            dcc.Graph(figure=fig_exp)
        ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '20px'})
    ])

def create_skills_tab():
    """Create the skills analysis tab"""
    skills_counter = extract_skills_data(df_main)
    top_skills = dict(skills_counter.most_common(20))
    
    # Overall top skills
    fig_skills = px.bar(x=list(top_skills.values()), y=list(top_skills.keys()),
                       orientation='h', title="Top 20 Most Demanded Skills",
                       labels={'x': 'Frequency', 'y': 'Skills'})
    fig_skills.update_layout(height=600)
    
    # Skills by role
    fig_skills_role = make_subplots(rows=1, cols=3, 
                                   subplot_titles=['Data Scientist', 'Data Analyst', 'Data Engineer'])
    
    roles = df_main['job_title'].unique()
    for i, role in enumerate(roles, 1):
        role_data = df_main[df_main['job_title'] == role]
        role_skills = []
        for skills_str in role_data['required_skills'].dropna():
            role_skills.extend([skill.strip() for skill in skills_str.split(',')])
        
        role_skills_counter = Counter(role_skills)
        top_role_skills = dict(role_skills_counter.most_common(10))
        
        fig_skills_role.add_trace(
            go.Bar(x=list(top_role_skills.values()), y=list(top_role_skills.keys()),
                  orientation='h', name=role, showlegend=False),
            row=1, col=i
        )
    
    fig_skills_role.update_layout(height=500, title_text="Top Skills by Role")
    
    return html.Div([
        dcc.Graph(figure=fig_skills),
        dcc.Graph(figure=fig_skills_role)
    ])

def create_salary_tab():
    """Create the salary benchmarking tab"""
    # Salary by role
    fig_salary_role = px.box(salary_data, x='job_title', y='salary',
                            title="Salary Distribution by Role")
    
    # Salary by experience
    fig_salary_exp = px.box(salary_data, x='experience_level', y='salary',
                           title="Salary Distribution by Experience Level")
    
    # Salary trends
    salary_benchmarks = calculate_salary_benchmarks(salary_data, ['job_title'])
    
    fig_benchmarks = go.Figure()
    for role in salary_benchmarks.index:
        fig_benchmarks.add_trace(go.Bar(
            name=role,
            x=['25th %ile', 'Median', 'Mean', '75th %ile', '90th %ile'],
            y=[salary_benchmarks.loc[role, 'p25'],
               salary_benchmarks.loc[role, 'median'],
               salary_benchmarks.loc[role, 'mean'],
               salary_benchmarks.loc[role, 'p75'],
               salary_benchmarks.loc[role, 'p90']]
        ))
    
    fig_benchmarks.update_layout(
        title="Salary Benchmarks by Role",
        xaxis_title="Percentile",
        yaxis_title="Salary ($)",
        barmode='group'
    )
    
    return html.Div([
        html.Div([
            dcc.Graph(figure=fig_salary_role),
            dcc.Graph(figure=fig_salary_exp)
        ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '20px'}),
        
        dcc.Graph(figure=fig_benchmarks)
    ])

def create_geographic_tab():
    """Create the geographic analysis tab"""
    # Top markets by job count
    location_counts = df_main['location'].value_counts().head(15)
    fig_locations = px.bar(x=location_counts.values, y=location_counts.index,
                          orientation='h', title="Top 15 Markets by Job Count")
    
    # Average salary by location
    salary_by_location = salary_data.groupby('location')['salary'].mean().sort_values(ascending=False).head(15)
    fig_salary_geo = px.bar(x=salary_by_location.values, y=salary_by_location.index,
                           orientation='h', title="Average Salary by Location (Top 15)")
    
    # Role distribution by location
    top_locations = location_counts.head(8).index
    role_geo_data = df_main[df_main['location'].isin(top_locations)]
    role_geo_counts = pd.crosstab(role_geo_data['location'], role_geo_data['job_title'])
    
    fig_role_geo = px.bar(role_geo_counts.reset_index(), x='location', 
                         y=['Data Analyst', 'Data Scientist', 'Data Engineer'],
                         title="Role Distribution in Top Markets")
    
    return html.Div([
        html.Div([
            dcc.Graph(figure=fig_locations),
            dcc.Graph(figure=fig_salary_geo)
        ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '20px'}),
        
        dcc.Graph(figure=fig_role_geo)
    ])

def create_strategic_tab():
    """Create the strategic insights tab"""
    # Calculate opportunity scores for roles
    role_analysis = df_main.groupby('job_title').agg({
        'job_id': 'count',
        'salary': 'mean',
        'num_skills': 'mean'
    }).round(2)
    
    role_analysis['market_share'] = (role_analysis['job_id'] / len(df_main)) * 100
    role_analysis['opportunity_score'] = (
        (role_analysis['market_share'] / role_analysis['market_share'].max()) * 0.4 +
        (role_analysis['salary'] / role_analysis['salary'].mean()) * 0.4 +
        (role_analysis['num_skills'] / role_analysis['num_skills'].max()) * 0.2
    ) * 100
    
    fig_opportunity = px.bar(x=role_analysis.index, y=role_analysis['opportunity_score'],
                            title="Role Opportunity Scores")
    
    # Market attractiveness by location
    geo_analysis = df_main.groupby('location').agg({
        'job_id': 'count',
        'salary': 'mean'
    }).round(2)
    
    geo_analysis = geo_analysis[geo_analysis['job_id'] >= 10]
    geo_analysis['attractiveness'] = (
        (geo_analysis['job_id'] / geo_analysis['job_id'].max()) * 0.6 +
        (geo_analysis['salary'] / geo_analysis['salary'].mean()) * 0.4
    ) * 100
    
    top_markets = geo_analysis.nlargest(10, 'attractiveness')
    fig_market_attract = px.bar(x=top_markets.index, y=top_markets['attractiveness'],
                               title="Top 10 Market Attractiveness Scores")
    
    # Key insights summary
    insights = html.Div([
        html.H3("Key Strategic Insights", style={'color': colors['text']}),
        html.Ul([
            html.Li(f"Data Scientists represent the highest opportunity role with {role_analysis.loc['Data Scientist', 'market_share']:.1f}% market share"),
            html.Li(f"Top market: {top_markets.index[0]} with attractiveness score of {top_markets.iloc[0]['attractiveness']:.1f}"),
            html.Li(f"Average skills per job: {df_main['num_skills'].mean():.1f}"),
            html.Li(f"Salary range spans from ${salary_data['salary'].min():,.0f} to ${salary_data['salary'].max():,.0f}"),
            html.Li(f"Remote work accounts for {(df_main['work_arrangement'].value_counts()['Remote'] / len(df_main) * 100):.1f}% of positions")
        ], style={'fontSize': '16px', 'lineHeight': '1.6'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'border-radius': '10px', 
              'box-shadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '20px 0'})
    
    return html.Div([
        insights,
        html.Div([
            dcc.Graph(figure=fig_opportunity),
            dcc.Graph(figure=fig_market_attract)
        ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '20px'})
    ])

if __name__ == '__main__':
    print("Starting Data Optimiser Dashboard...")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop the server")
    
    # Run the app
    app.run(debug=True, host='127.0.0.1', port=8050)