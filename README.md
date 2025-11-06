# Solar Challenge Week 0
## Task 1:
## Setup

1. Clone repo:

  git clone [<repo-url>](https://github.com/Saronzeleke/solar-challenge-week0.git)

  cd solar-challenge-week0

2. Create virtual environment:

  python3 -m venv venv

  venv is the name of the environment

  source venv/bin/activate # or venv\Scripts\activate on Windows

3. Install dependencies:

   pip install -r requirements.txt

## Task 2: Data Profiling, Cleaning & EDA

This section covers exploratory data analysis for solar datasets from **Benin**, **Sierra Leone**, and **Togo**.  

Each analysis was conducted on separate branches (`eda-benin`, `eda-sierra_leone`, `eda-togo`) and saved in individual 

notebooks.

### Key steps performed

- Summary statistics and missing value profiling

- Outlier detection using Z-score

- Data cleaning with median imputation

- Temporal trend analysis (GHI, DNI, DHI, Tamb)

- Cleaning impact visualization on module efficiency

- Correlation and scatter analysis

- Wind rose, distribution, and bubble plots

- Statistical measures: skewness and kurtosis

All cleaned datasets are stored locally under `/data` and excluded from Git tracking.

