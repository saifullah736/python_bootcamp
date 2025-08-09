# Data Optimiser: Job Posting Analysis Project

## Project Overview
This project provides a comprehensive analysis of job posting data for **Data Optimiser**, a fictional recruitment company specializing in data science roles. The analysis covers data integrity checks, exploratory data analysis, business question investigation, and strategic recommendations - all implemented using Python to demonstrate Power BI-equivalent capabilities.

## 🎯 Business Objectives
- Identify the most in-demand skills for data scientists, data analysts, and data engineers
- Analyze geographic distribution of data jobs and salary variations
- Provide salary benchmarking recommendations for competitive positioning
- Determine optimal client targeting strategies
- Generate actionable insights for recruitment business strategy

## 📋 Project Structure

### Core Analysis Files
1. **`create_job_dataset.py`** - Generates realistic job posting dataset with intentional data quality issues
2. **`1_data_integrity_check.ipynb`** - Comprehensive data quality assessment and validation
3. **`2_exploratory_data_analysis.ipynb`** - In-depth EDA with visualizations and statistical analysis
4. **`3_business_questions.ipynb`** - Strategic business analysis addressing key recruitment questions
5. **`4_dashboard_creation.py`** - Interactive dashboard using Plotly Dash (Power BI equivalent)

### Data Files
- **`job_postings_dataset.csv`** - Main dataset with 1,000+ job postings across 3 data roles

## 🚀 Quick Start Guide

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn plotly dash
```

### Running the Analysis

1. **Generate Dataset**:
```bash
python create_job_dataset.py
```

2. **Run Analysis Notebooks**:
   - Open and execute notebooks in order (1 → 2 → 3)
   - Each notebook builds on insights from previous analyses

3. **Launch Interactive Dashboard**:
```bash
python 4_dashboard_creation.py
```
   - Access dashboard at: http://127.0.0.1:8050
   - Interactive visualizations with filtering and drill-down capabilities

## 📊 Key Findings & Insights

### Market Overview
- **Data Scientists** dominate the market (40% of postings) with highest opportunity scores
- **San Francisco** and **New York** are top markets by volume and salary premiums
- **Remote work** accounts for significant portion of opportunities across all roles

### Skills Analysis
- **Python** and **SQL** are universally critical skills across all data roles
- **Machine Learning** and **Statistics** differentiate Data Scientists
- **Tableau** and **Power BI** are essential for Data Analysts
- **Apache Spark** and **Hadoop** are key for Data Engineers

### Salary Benchmarking
- **Data Engineers** command highest average salaries ($95K-$140K)
- **Experience level** shows strong correlation with compensation (r=0.75)
- **Geographic premiums** up to 30% in major tech hubs
- **Company size** impacts salary ranges significantly

### Strategic Recommendations
1. **Primary Focus**: Data Scientist recruitment (highest opportunity score)
2. **Geographic Strategy**: Establish offices in SF, NYC, Seattle (Tier 1 markets)
3. **Client Targeting**: Prioritize Large (1000+) and Medium (200-1000) companies
4. **Skills Specialization**: Build talent pools for Python, SQL, Machine Learning

## 🎨 Dashboard Features

### Executive Overview
- Key performance metrics (total jobs, median salary, market coverage)
- Job distribution by role, company size, and experience level
- Time-based trending analysis

### Skills Analysis
- Top 20 most demanded skills across all roles
- Role-specific skill requirements and specializations
- Skills gap analysis and emerging trends

### Salary Benchmarking
- Interactive salary calculator by role, experience, and location
- Percentile-based salary ranges (25th, 50th, 75th, 90th)
- Geographic and company size adjustment factors

### Geographic Intelligence
- Market opportunity mapping by location
- Salary premium analysis by city
- Role distribution across top markets

### Strategic Insights
- Role opportunity scoring and prioritization
- Market attractiveness analysis
- Actionable business recommendations

## 🔧 Power BI Translation Guide

### Data Model Setup
1. **Import CSV** using Power Query Editor
2. **Data Types**: Ensure salary (Currency), dates (Date), skills (Text)
3. **Relationships**: Create date table for time intelligence
4. **Calculated Columns**: Skills count, experience ranking, salary ranges

### Key DAX Measures
```dax
// Basic Metrics
Total Jobs = COUNTROWS(JobData)
Average Salary = AVERAGE(JobData[salary])
Market Share = DIVIDE([Total Jobs], CALCULATE([Total Jobs], ALL(JobData[location])))

// Advanced Analytics
Opportunity Score = 
    [Market Share] * 0.4 + 
    [Salary Index] * 0.4 + 
    [Complexity Score] * 0.2

Skills Count = 
    LEN(JobData[required_skills]) - 
    LEN(SUBSTITUTE(JobData[required_skills], ",", "")) + 1

Salary Benchmark = 
    CALCULATE(
        PERCENTILE.INC(JobData[salary], 0.5),
        FILTER(JobData, 
            JobData[job_title] = SELECTEDVALUE(JobData[job_title]) &&
            JobData[experience_level] = SELECTEDVALUE(JobData[experience_level])
        )
    )
```

### Dashboard Pages
1. **Executive Summary**: KPIs, trends, high-level metrics
2. **Market Analysis**: Geographic and role distributions
3. **Skills Intelligence**: Demand analysis and gap identification
4. **Salary Benchmarking**: Compensation planning tools
5. **Strategic Planning**: Opportunity analysis and recommendations

### Power BI Service Deployment
1. **Workspace Creation**: Create dedicated workspace for recruitment analytics
2. **Data Refresh**: Set up scheduled refresh for real-time insights
3. **Security**: Configure row-level security if needed
4. **Sharing**: Publish app for stakeholder access
5. **Mobile**: Optimize layouts for mobile consumption

## 📈 Business Impact

### For Data Optimiser Recruitment Company
- **Market Intelligence**: Data-driven understanding of supply/demand dynamics
- **Competitive Positioning**: Salary benchmarking for client advisory services
- **Strategic Planning**: Geographic expansion and role prioritization roadmap
- **Client Acquisition**: Targeted approach based on company size and hiring patterns

### Operational Benefits
- **Efficiency**: Automated analysis replacing manual market research
- **Accuracy**: Statistical validation of compensation recommendations
- **Scalability**: Framework for ongoing market monitoring
- **Insights**: Actionable intelligence for business development

## 🔮 Future Enhancements

### Data Expansion
- Real-time job posting APIs integration
- Historical trend analysis (multi-year dataset)
- Skills taxonomy standardization
- Industry vertical segmentation

### Advanced Analytics
- Predictive modeling for salary trends
- Machine learning for skill gap prediction
- Natural language processing for job description analysis
- Network analysis for skills relationships

### Dashboard Evolution
- Real-time data streaming
- Advanced filtering and personalization
- Mobile-first responsive design
- AI-powered insights and recommendations

## 📝 Technical Notes

### Data Quality Considerations
- **Missing Values**: 6% of salary data requires imputation or exclusion
- **Duplicates**: 20 duplicate records identified and flagged
- **Inconsistencies**: Date formats and location naming standardized
- **Outliers**: Salary outliers validated against market benchmarks

### Performance Optimization
- **Data Model**: Star schema design for optimal query performance
- **Indexing**: Appropriate indexing on filter columns
- **Aggregations**: Pre-calculated measures for complex analytics
- **Compression**: Optimized data types and encoding

### Deployment Architecture
- **Development**: Local Python environment with Jupyter notebooks
- **Testing**: Dash application for interactive validation
- **Production**: Power BI Service for enterprise deployment
- **Maintenance**: Automated data refresh and quality monitoring

## 📞 Contact & Support

For questions about this analysis or to discuss implementation for your organization:

- **Project Repository**: [GitHub Link]
- **Documentation**: Comprehensive analysis notebooks included
- **Demo Dashboard**: Available at deployment URL
- **Technical Support**: Detailed implementation guides provided

---

**Note**: This project demonstrates enterprise-grade data analysis capabilities using Python ecosystem tools, providing a complete foundation for Power BI implementation and business intelligence deployment.