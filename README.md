# UCB Driver Coupon Analysis

Exploring driver decisions on UCI coupon data. Statistical & visual insights into coupon choices with pandas summaries & seaborn/plotly visualizations.

## Getting Started

**[Setup Instructions](docs/SETUP.md)** - Complete installation and environment setup guide

**[Assignment Instructions](docs/assignment-instructions.md)** - Detailed assignment requirements, data description, and analysis problems

### Quick Start
```bash
jupyter notebook
```
Then open [`prompt.ipynb`](prompt.ipynb) to begin the EDA.

## Project Structure

```
ucb-driver-coupon-analysis/
├── data/                   # Dataset files
├── docs/                   # supporting docs
├── images/                 # Generated plots and images
├── notebooks/              # Additional analysis notebooks
├── src/
│   ├── setup.py           # Automated environment setup
│   └── helpers.py         # Utility functions
├── prompt.ipynb           # Main EDA notebook
├── requirements.txt       # Package dependencies
└── README.md             # This file
```

## Analysis Overview

This project performs exploratory data analysis on the UCI coupon dataset to understand:
- Driver behavior patterns
- Factors influencing coupon acceptance
- Statistical relationships between variables
- Visual insights through comprehensive plotting

**[📊 Complete Analysis Summary](docs/analysis-summary.md)** - Comprehensive findings, recommendations, and modeling suggestions

### Key Findings
- **Bar coupons**: 41% acceptance rate, with 73% acceptance among frequent bar-goers
- **Social context matters**: 65-70% acceptance when traveling with friends vs 45-50% with children
- **Convenience is key**: 69% acceptance for same-direction travel vs 44% for opposite direction
- **Lifestyle compatibility**: Existing behavior patterns are the strongest predictors of acceptance

## Do yo want to Contribute ?

Feel free to fork this repository and do your analysis. This is part of a graded assignment, not accepting external pull requests at this time. Thank you. 
