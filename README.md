# Solar Data Analysis Challenge

## Project Overview
Comprehensive analysis of solar irradiation data for Benin, Sierra Leone, and Togo. This project includes data 

profiling, cleaning, exploratory analysis, and cross-country comparison of solar energy potential.

## 📁 Repository Structure

solar-challenge-week0/

├── .github/workflows/ci.yml # GitHub Actions CI/CD

├── app/dashboard.py # Streamlit dashboard

├── data/

│ ├── raw/ # Original datasets

├── notebooks/

│ ├── 1-benin-analysis.ipynb # Benin EDA

│ ├── 2-sierra-leone-analysis.ipynb # Sierra Leone EDA

│ ├── 3-togo-analysis.ipynb # Togo EDA

│ └── 4-cross-country-comparison.ipynb # Comparative analysis

├── scripts/ # Utility scripts

├── tests/ # Test files

├── .gitignore

├── requirements.txt

└── README.md

## 🚀 Setup Instructions

## Prerequisites
- Python 3.8+

- Git

## Installation

## 1. Clone the repository:


git clone https://github.com/Saronzeleke/solar-challenge-week0.git

cd solar-challenge-week0

## 2. Create and activate virtual environment:

python -m venv my_env

# Windows:

my_env\Scripts\activate

# Linux/Mac:

source my_env/bin/activate 

## 3. Install dependencies:

pip install -r requirements.txt

## 4.Launch Jupyter for analysis:

jupyter notebook

## Usage

Data Analysis

Open notebooks in order (1-4) for complete analysis

Each notebook includes data profiling, cleaning, and visualization

Cross-country comparison in notebook 4

## Dashboard

streamlit run app/dashboard.py

## 📊 Analysis Workflow

Data Profiling: Summary statistics, missing values, data types

Data Cleaning: Outlier detection (Z-score > 3), missing value handling

Exploratory Analysis: Time series, correlations, distributions

Cross-Country Comparison: Statistical tests, visual comparisons

## 🔬 Key Features

Comprehensive EDA for each country

Statistical significance testing (ANOVA/Kruskal-Wallis)

Interactive Streamlit dashboard

Automated CI/CD with GitHub Actions

Modular, reproducible analysis

## 📈 Key Findings

[Add your specific findings after running the analysis]

## 🤝 Contributing

Create feature branch: git checkout -b feature/analysis

Commit changes: git commit -m "Add feature"

Push branch: git push origin feature/analysis

Create Pull Request

## 📄 License

MIT License - see LICENSE file for details 

