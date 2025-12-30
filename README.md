# UCB Driver Coupon Analysis

Exploring driver decisions on UCI coupon data. Statistical & visual insights into coupon choices with pandas summaries & seaborn/plotly visualizations.

## Getting Started

**[Setup Instructions](docs/SETUP.md)** - Complete installation and environment setup guide

**[Assignment Instructions](docs/assignment-instructions.md)** - Detailed assignment requirements, data description, and analysis problems

### Quick Start

**Option 1: Jupyter Notebook**
```bash
pip install -r requirements.txt
jupyter notebook
```
Then open [`prompt.ipynb`](prompt.ipynb) to begin the EDA.

**Option 2: Interactive Dashboard**
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```
Opens a browser-based interactive dashboard for exploring the data.

**Option 3: View Static HTML Report**

Open [`prompt.html`](prompt.html) in your browser to view the pre-rendered analysis with all visualizations.

## Project Structure

```
ucb-driver-coupon-analysis/
├── data/                   # Dataset files (coupons.csv)
├── docs/                   # Documentation
│   ├── SETUP.md           # Installation guide
│   ├── assignment-instructions.md
│   └── analysis-summary.md # Comprehensive findings
├── images/                 # Generated plots and visualizations
├── notebooks/              # Additional analysis notebooks
├── scripts/
│   └── export_html.py     # Notebook to HTML converter with Plotly support
├── src/
│   ├── setup.py           # Automated environment setup
│   └── helpers.py         # Analysis utilities and visualization helpers
├── .streamlit/
│   └── config.toml        # Streamlit dark theme configuration
├── dashboard.py           # Interactive Streamlit dashboard
├── prompt.ipynb           # Main EDA notebook
├── prompt.html            # Rendered HTML report with interactive charts
├── requirements.txt       # Package dependencies
└── README.md              # This file
```

## Features

### Jupyter Notebook (`prompt.ipynb`)
- Complete exploratory data analysis
- Bar coupon deep-dive with segmentation analysis
- Extended analysis for Coffee House, Restaurant(<20), and Carry Away coupons
- Time-based analysis with expiration interactions
- Solarized theme for consistent visualizations

### Interactive Dashboard (`dashboard.py`)
- **Overview**: Key metrics, acceptance by coupon type, destination×passenger heatmap
- **Coupon Type Analysis**: Demographics, behavior patterns, contextual factors
- **Time Analysis**: Time-of-day patterns, expiration impact, optimal timing by coupon type
- **Segment Explorer**: Build custom segments and compare acceptance rates
- **Custom Analysis**: Create pivot tables with any variables, visualize as heatmap or bar chart

### Helper Library (`src/helpers.py`)
Reusable functions for coupon analysis:
- `calculate_acceptance_rate()` - Acceptance rates by group
- `compare_segments()` - Compare two segments with statistics
- `analyze_time_patterns()` - Time-of-day analysis
- `validate_dataframe()` - Data quality checks
- `apply_solarized_theme()` - Consistent plot styling
- Visualization helpers with Solarized/dark theme support

## Analysis Overview

This project performs exploratory data analysis on the UCI coupon dataset to understand:
- Driver behavior patterns across different coupon types
- Factors influencing coupon acceptance (demographics, context, timing)
- Statistical relationships between variables
- Visual insights through comprehensive plotting

**[📊 Complete Analysis Summary](docs/analysis-summary.md)** - Comprehensive findings, recommendations, and modeling suggestions

### Key Findings
- **Bar coupons**: 41% acceptance rate, with 73% acceptance among frequent bar-goers
- **Social context matters**: 65-70% acceptance when traveling with friends vs 45-50% with children
- **Convenience is key**: 69% acceptance for same-direction travel vs 44% for opposite direction
- **Lifestyle compatibility**: Existing behavior patterns are the strongest predictors of acceptance
- **Time sensitivity**: 2PM shows highest overall acceptance (66%), 7AM lowest (50%)
- **Expiration impact**: 1-day coupons outperform 2-hour coupons (63% vs 50%)

## Dependencies

Core packages (see `requirements.txt` for versions):
- pandas, numpy - Data manipulation
- matplotlib, seaborn, plotly - Visualization
- jupyter, nbconvert - Notebook environment
- streamlit - Interactive dashboard
- kaleido - Static image export

## Do you want to Contribute?

Feel free to fork this repository and do your analysis. This is part of a graded assignment, not accepting external pull requests at this time. Thank you. 
