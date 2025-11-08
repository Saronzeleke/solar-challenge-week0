## 🌞 Solar Challenge Week 0

## 📘 Project Overview

This project focuses on analyzing solar farm data from Benin, Sierra Leone, and Togo to extract meaningful insights and identify high-potential regions for solar energy installation.
It is part of the 10 Academy Week 0 Challenge, designed to assess candidates’ skills in Data Engineering, Financial Analytics, and Machine Learning Engineering.

## 🧠 Objectives

Perform data cleaning, profiling, and exploratory data analysis (EDA).

Understand environmental and solar measurement patterns (GHI, DNI, DHI, temperature, humidity, wind, etc.).

Derive data-driven insights that support sustainable solar energy strategies.

Showcase version control, collaboration, and CI/CD setup through GitHub workflows.

## ⚙️ Setup Instructions

## 1️⃣ Clone Repository

git clone https://github.com/Saronzeleke/solar-challenge-week0.git

cd solar-challenge-week0

## 2️⃣ Create Virtual Environment

python3 -m venv venv

# Activate environment

source venv/bin/activate  # (Linux/Mac)

venv\Scripts\activate     # (Windows)


## 3️⃣ Install Dependencies

pip install -r requirements.txt

## 4️⃣ Folder Structure


solar-challenge-week0/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── notebooks/
│   ├── benin_eda.ipynb
│   ├── togo_eda.ipynb
│   ├── sierra_leone_eda.ipynb
│
├── scripts/
│   ├── cleaning.py
│   ├── eda_utils.py
│   ├── visualization.py
│
├── tests/
│   └── test_cleaning.py
│
├── requirements.txt
├── .gitignore
└── README.md

## 📊 Key Performance Indicators (KPIs)

## Category	                   KPI	                                     Description

**Environment Setup           ✅ Git & venv configured        Repository initialized with CI workflow and requirements**

**Version Control	            ✅ Frequent commits	             Clear and descriptive commit messages using Git branches**

**EDA & Cleaning	         ✅ Data profiling completed	Summary stats,  missing values, and outlier detection implemented**

**Visualization & Insights	✅ Meaningful plots	     Clear time-series, correlation heatmaps, and trend visualizations**

**Documentation	            ✅ Professional README	       Steps to reproduce, objectives, and structure well explained**

**Proactivity	            ✅ Self-learning & clarity	      Use of proper statistical and visualization techniques**

**CI/CD Workflow         ✅ GitHub Actions setup                    Automated test or installation pipeline included**



## 🧩 Tools & Technologies

Python (Pandas, NumPy, Matplotlib, Seaborn)

Git & GitHub

CI/CD using GitHub Actions

Streamlit (for dashboard creation)

Jupyter Notebooks

## 🧾 Author

**Saron Zeleke**

📧 [Sharonkuye369@gmail.com]


🔗 GitHub Profile