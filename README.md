# Singapore Tech Job Market Analysis

This repository contains a comprehensive analysis of Singapore's tech job market data, including exploratory data analysis (EDA) and an interactive Streamlit dashboard for visualizing job market trends.

## 📁 Repository Contents

### Files

- **`app.py`** - Streamlit web application providing an interactive dashboard for analyzing Singapore tech job market data
- **`Group_5_SGJobData.ipynb`** - Jupyter notebook containing exploratory data analysis (EDA) of the job data
- **`Week 4 - EDA for Job Data.pptx`** - PowerPoint presentation documenting the analysis findings and insights
- **`SGJobData.csv`** - Dataset containing Singapore job postings data *(Note: Due to file size limitations, the CSV file is not included in this repository. You'll need to add your own dataset with the same structure.)*
- **`requirements.txt`** - Python package dependencies

## 🎯 Project Overview

This project analyzes Singapore's tech job market by:
- Filtering and identifying technology-related job postings
- Analyzing job posting trends over time
- Examining salary ranges and company hiring patterns
- Investigating sector-wise job distribution and growth trends
- Visualizing key metrics through interactive charts and graphs

### Key Features

The Streamlit dashboard provides three main sections:

1. **Tech Hiring Overview**
   - Top companies by tech job postings
   - Job postings and vacancies trends over time
   - Salary range analysis over time
   - Repost and recency metrics

2. **Tech Job Title Analysis**
   - Top tech job titles by count
   - Salary distribution for different roles
   - Correlation between job postings and salaries

3. **Industry Dynamics**
   - Sector-wise job distribution
   - Growth trends by sector
   - Median salary analysis by sector
   - Dominant roles within each sector

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Conda (recommended) or pip
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/bamsby/job-data-analysis.git
cd job-data-analysis
```

### Step 2: Set Up Conda Environment (Recommended)

Create and activate a new conda environment:

```bash
# Create conda environment
conda create -n pds python=3.10

# Activate the environment
conda activate pds
```

### Step 3: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

**Or using conda:**

```bash
conda run -n pds pip install -r requirements.txt
```

### Step 4: Verify Installation

The installation includes:
- `streamlit` - For the web dashboard
- `plotly` - For interactive visualizations
- `pandas` - For data manipulation
- `numpy` - For numerical operations (installed as a dependency)

## 🖥️ Running the Streamlit Dashboard

### Method 1: Using Conda (Recommended)

If using conda environment:

```bash
conda activate pds
streamlit run app.py
```

**Or directly with conda run:**

```bash
conda run -n pds streamlit run app.py
```

### Method 2: Using Python directly

If using a virtual environment or system Python:

```bash
streamlit run app.py
```

### Accessing the Dashboard

Once the app is running, Streamlit will automatically open your default web browser to:
- **Local URL:** `http://localhost:8501`

If it doesn't open automatically, navigate to the URL shown in your terminal.

## 📊 Data Overview

The dataset (`SGJobData.csv`) contains:
- Job postings from Singapore
- Metadata including posting dates, expiry dates, repost counts
- Company information
- Salary ranges (minimum and maximum)
- Job titles and categories
- Vacancy information

## 🔍 Key Analysis Features

### Interactive Filters
- **Date Range Slider:** Filter time series visualizations by date
- **Top Job Titles Selector:** Adjust the number of top jobs to display
- **Sector Selector:** View dominant roles within specific sectors
- **Top Sectors Selector:** Control the number of sectors displayed

### Visualizations
- Line charts for trends over time
- Bar charts for rankings and comparisons
- Scatter plots for correlation analysis
- Interactive tables with sortable columns

## 📝 Jupyter Notebook

The `Group_5_SGJobData.ipynb` notebook contains detailed EDA including:
- Data loading and preprocessing
- Statistical analysis
- Visualizations
- Insights and findings

To run the notebook:
1. Activate your conda environment: `conda activate pds`
2. Launch Jupyter: `jupyter notebook`
3. Open `Group_5_SGJobData.ipynb`

## 🛠️ Technologies Used

- **Python** - Programming language
- **Streamlit** - Web application framework
- **Plotly** - Interactive visualization library
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Jupyter Notebook** - Interactive development environment

## 📈 Project Structure

```
job-data-analysis/
│
├── app.py                          # Streamlit dashboard application
├── Group_5_SGJobData.ipynb         # EDA Jupyter notebook
├── Week 4 - EDA for Job Data.pptx  # Analysis presentation
├── SGJobData.csv                   # Job market dataset
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is for educational and analytical purposes.

## 👤 Author

- **bamsby** - [@bamsby](https://github.com/bamsby)

## 🙏 Acknowledgments

- Data sourced from Singapore job market databases
- Built as part of Data Science and AI coursework (Week 4 - EDA for Job Data)

---

**Note:** 
- The `SGJobData.csv` file is not included in this repository due to GitHub's file size limitations (100 MB limit).
- You'll need to provide your own dataset file named `SGJobData.csv` in the same directory as `app.py` when running the Streamlit dashboard.
- The CSV file should contain columns matching the expected structure (e.g., `title`, `metadata_newPostingDate`, `metadata_originalPostingDate`, `salary_minimum`, `salary_maximum`, `postedCompany_name`, `categories`, etc.).

## Dashboard Screenshots

### Tech Hiring Overview
![Tech Hiring Overview](images/dashboard-overview.png)

### Job Postings and Salary Trends
![Job Postings and Salary Trends](images/dashboard-posting-salary.png)

### Tech Job Title Analysis
![Top Tech Job Titles](images/dashboard-top-tech-jobs.png)

### Industry Dynamics
![Industry Dynamics](images/dashboard-industry-dynamics.png)

![Top Sectors](images/dashboard-top-sectors.png)