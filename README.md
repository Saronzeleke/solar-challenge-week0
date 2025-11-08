# Solar Challenge – Week 0  
**Saron Zeleke** | Analytics Engineer Candidate  
*MoonLight Energy Solutions – Data-Driven Solar Strategy*

## Project Overview

This repository completes **Task 1: Git & Environment Setup** and lays the foundation for **Task 2: EDA & Regional Solar Ranking**. It enables **reproducible, CI-tested analysis** of solar irradiance data from **Benin, Sierra Leone, and Togo** to identify **high-potential regions** for sustainable solar investment.



## Repository Structure

```bash
solar-challenge-week0/
├── .vscode/                # IDE configuration
│   └── settings.json
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI
├── src/                    # Models & utilities
├── notebooks/              # EDA notebooks
├── tests/                  # Unit tests
├── scripts/                # Data pipelines
├── data/                   # Raw/cleaned data (gitignored)
├── .gitignore
├── requirements.txt
├── README.md               # This file
└── LICENSE

Task 1: Git & Environment Setup (Completed)
Requirement,Status,Details
Repo,Done,solar-challenge-week0
Branch,Done,setup-task → merged
3+ Commits,Done,".gitignore, requirements, CI"
.gitignore,Done,"data/, venv/, .ipynb_checkpoints"
CI Pipeline,Done,"Installs deps, runs tests"
Folder Structure,Done,As specified
PR Merged,Done,#1