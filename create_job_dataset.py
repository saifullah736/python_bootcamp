"""
Script to create a realistic job posting dataset for the Data Optimiser recruitment analysis.
This simulates a real-world dataset with various data quality issues that need to be addressed.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define data parameters
n_jobs = 1000

# Job titles and their typical skills
job_roles = {
    'Data Scientist': {
        'weight': 0.4,
        'skills': ['Python', 'R', 'Machine Learning', 'SQL', 'Statistics', 'Deep Learning', 
                  'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Jupyter',
                  'Git', 'Docker', 'AWS', 'Azure', 'GCP', 'Tableau', 'Power BI'],
        'salary_range': (70000, 150000)
    },
    'Data Analyst': {
        'weight': 0.35,
        'skills': ['SQL', 'Excel', 'Python', 'R', 'Tableau', 'Power BI', 'Statistics',
                  'Pandas', 'Matplotlib', 'Seaborn', 'Git', 'PowerQuery', 'DAX',
                  'Google Analytics', 'Looker', 'SPSS'],
        'salary_range': (50000, 90000)
    },
    'Data Engineer': {
        'weight': 0.25,
        'skills': ['Python', 'SQL', 'Apache Spark', 'Hadoop', 'Kafka', 'Airflow',
                  'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'ETL', 'NoSQL',
                  'PostgreSQL', 'MongoDB', 'Redis', 'Git', 'Linux', 'Scala', 'Java'],
        'salary_range': (80000, 140000)
    }
}

# Company information
companies = ['Tech Corp', 'Data Solutions Inc', 'Analytics Pro', 'Big Data Co', 'Smart Analytics',
            'Digital Insights', 'AI Innovations', 'Cloud Data Systems', 'Business Intelligence Ltd',
            'Data Driven Co', 'Analytics First', 'Information Systems Inc', 'Data Science Corp',
            'Intelligence Solutions', 'Analytics Hub', 'Data Experts Ltd', 'Insight Technologies',
            'DataFlow Systems', 'Analytics Partners', 'Information Analytics']

company_sizes = ['Startup (1-50)', 'Small (51-200)', 'Medium (201-1000)', 'Large (1001+)']
experience_levels = ['Entry Level (0-2 years)', 'Mid Level (3-5 years)', 'Senior Level (6-10 years)', 'Lead Level (10+ years)']
locations = ['New York, NY', 'San Francisco, CA', 'Seattle, WA', 'Chicago, IL', 'Boston, MA',
            'Austin, TX', 'Los Angeles, CA', 'Denver, CO', 'Atlanta, GA', 'Washington, DC',
            'Portland, OR', 'San Diego, CA', 'Phoenix, AZ', 'Dallas, TX', 'Miami, FL']

# Work arrangements
work_arrangements = ['Remote', 'On-site', 'Hybrid']

def generate_skills_for_role(role, num_skills=None):
    """Generate a realistic set of skills for a given role"""
    available_skills = job_roles[role]['skills']
    if num_skills is None:
        num_skills = random.randint(3, min(8, len(available_skills)))
    
    # Weight skills by importance (first skills are more common)
    weights = [1.0 / (i + 1) for i in range(len(available_skills))]
    
    selected_skills = np.random.choice(
        available_skills, 
        size=min(num_skills, len(available_skills)), 
        replace=False, 
        p=np.array(weights) / np.sum(weights)
    )
    return ', '.join(selected_skills)

def generate_salary(role, experience, location_factor=1.0):
    """Generate salary based on role, experience, and location"""
    base_min, base_max = job_roles[role]['salary_range']
    
    # Experience multipliers
    exp_multipliers = {
        'Entry Level (0-2 years)': 0.8,
        'Mid Level (3-5 years)': 1.0,
        'Senior Level (6-10 years)': 1.3,
        'Lead Level (10+ years)': 1.6
    }
    
    multiplier = exp_multipliers[experience] * location_factor
    min_salary = int(base_min * multiplier)
    max_salary = int(base_max * multiplier)
    
    return random.randint(min_salary, max_salary)

# Generate dataset
data = []
start_date = datetime.now() - timedelta(days=365)

for i in range(n_jobs):
    # Select role based on weights
    role = np.random.choice(
        list(job_roles.keys()),
        p=[job_roles[role]['weight'] for role in job_roles.keys()]
    )
    
    # Location factors for salary adjustment
    location = random.choice(locations)
    location_factors = {
        'San Francisco, CA': 1.3, 'New York, NY': 1.25, 'Seattle, WA': 1.2,
        'Boston, MA': 1.15, 'Los Angeles, CA': 1.1, 'Washington, DC': 1.1
    }
    location_factor = location_factors.get(location, 1.0)
    
    experience = random.choice(experience_levels)
    company = random.choice(companies)
    company_size = random.choice(company_sizes)
    work_arrangement = random.choice(work_arrangements)
    
    # Generate posting date
    posting_date = start_date + timedelta(days=random.randint(0, 365))
    
    # Generate skills
    skills = generate_skills_for_role(role)
    
    # Generate salary
    salary = generate_salary(role, experience, location_factor)
    
    # Add some data quality issues intentionally
    issues_random = random.random()
    
    # Sometimes make salary missing or unrealistic
    if issues_random < 0.05:
        salary = None
    elif issues_random < 0.08:
        salary = random.randint(20000, 30000)  # Unrealistically low
    elif issues_random < 0.10:
        salary = random.randint(200000, 300000)  # Unrealistically high for most roles
    
    # Sometimes make location inconsistent
    if issues_random < 0.02:
        location = location.replace(',', '')  # Remove comma
    elif issues_random < 0.03:
        location = location.lower()  # Wrong case
    
    # Sometimes make company name inconsistent
    if issues_random < 0.02:
        company = company + ' Inc.'  # Add Inc. inconsistently
    
    # Sometimes make experience level inconsistent
    if issues_random < 0.02:
        experience = experience.replace('(', '').replace(')', '')  # Remove parentheses
    
    job_record = {
        'job_id': f'JOB_{str(i+1).zfill(4)}',
        'job_title': role,
        'company': company,
        'company_size': company_size,
        'location': location,
        'experience_level': experience,
        'work_arrangement': work_arrangement,
        'salary': salary,
        'required_skills': skills,
        'posting_date': posting_date.strftime('%Y-%m-%d'),
        'date_posted': posting_date.strftime('%m/%d/%Y') if random.random() > 0.05 else posting_date.strftime('%Y-%m-%d')  # Inconsistent date formats
    }
    
    data.append(job_record)

# Create DataFrame
df = pd.DataFrame(data)

# Add some duplicate records (data quality issue)
duplicates = df.sample(n=20).copy()
duplicates['job_id'] = [f'JOB_{str(n_jobs + i + 1).zfill(4)}' for i in range(20)]
df = pd.concat([df, duplicates], ignore_index=True)

# Save to CSV
df.to_csv('/home/runner/work/python_bootcamp/python_bootcamp/job_postings_dataset.csv', index=False)

print(f"Dataset created with {len(df)} job postings")
print(f"Data saved to: job_postings_dataset.csv")
print("\nDataset overview:")
print(df.info())
print("\nFirst few rows:")
print(df.head())