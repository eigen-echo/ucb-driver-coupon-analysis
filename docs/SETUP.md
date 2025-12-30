# Setup Instructions

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer) OR Anaconda/Miniconda

## Setup Instructions

Choose one of the following setup methods:

### Option 1: Automated Setup (Recommended for pip users)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ucb-driver-coupon-analysis
   ```

2. **Create and activate a virtual environment (Recommended)**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Run the automated setup**
   ```bash
   python src/setup.py
   ```
   
   The setup script will:
   - Check your Python version
   - Verify virtual environment setup
   - Check for required packages (pandas, numpy, seaborn, plotly, jupyter, matplotlib)
   - Install missing packages automatically
   - Offer to start Jupyter Notebook

### Option 2: Conda Users (Anaconda/Miniconda)

If you have Anaconda or Miniconda installed, most required packages should already be available:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ucb-driver-coupon-analysis
   ```

2. **Create a conda environment (Optional but recommended)**
   ```bash
   conda create -n coupon-analysis python=3.9
   conda activate coupon-analysis
   ```

3. **Install any missing packages**
   ```bash
   conda install pandas numpy seaborn matplotlib jupyter
   conda install -c plotly plotly
   ```
   
   Or use pip for plotly:
   ```bash
   pip install plotly
   ```

4. **Verify setup (Optional)**
   ```bash
   python src/setup.py
   ```

### Option 3: Manual Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ucb-driver-coupon-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Start the Analysis

```bash
jupyter notebook
```
Then open [`prompt.ipynb`](../prompt.ipynb) to begin the EDA.

## Dependencies

### Core Analysis
- **pandas** (≥1.3.0) - Data manipulation and analysis
- **numpy** (≥1.21.0) - Numerical computing
- **seaborn** (≥0.11.0) - Statistical data visualization
- **plotly** (≥5.0.0) - Interactive visualizations
- **matplotlib** (≥3.3.0) - Plotting library

### Notebook Environment
- **jupyter** (≥1.0.0) - Notebook environment
- **nbconvert** (≥7.0.0) - Notebook to HTML conversion
- **ipykernel** (≥6.0.0) - Jupyter kernel support
- **kaleido** (≥0.2.0) - Static image export for Plotly

### Interactive Dashboard
- **streamlit** (≥1.28.0) - Web-based dashboard framework

## Running the Dashboard

After installation, you can run the interactive Streamlit dashboard:

```bash
streamlit run dashboard.py
```

This opens a browser-based dashboard with:
- Overview metrics and visualizations
- Coupon type deep-dive analysis
- Time-based pattern exploration
- Custom segment comparison tools
- Pivot table builder

## 🔧 Troubleshooting

If you encounter issues:

1. **Package installation fails**: Ensure you have the latest pip version
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Virtual environment issues**: Make sure you've activated your virtual environment before running the setup

3. **Jupyter not starting**: Try installing jupyter explicitly
   ```bash
   pip install jupyter
   ```

4. **Import errors**: Run the setup script again to verify all packages are properly installed
   ```bash
   python src/setup.py