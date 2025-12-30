import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, List, Optional, Union

# =============================================================================
# SOLARIZED THEME CONFIGURATION
# =============================================================================

# Solarized color palette
SOLARIZED = {
    # Base colors
    'base03': '#002b36',   # Dark background
    'base02': '#073642',   # Dark background highlight
    'base01': '#586e75',   # Light text (dark bg) / Dark text (light bg)
    'base00': '#657b83',   # Light text (dark bg) / Dark text (light bg)
    'base0': '#839496',    # Dark text (light bg) / Light text (dark bg)
    'base1': '#93a1a1',    # Dark text (light bg) / Light text (dark bg)
    'base2': '#eee8d5',    # Light background highlight
    'base3': '#fdf6e3',    # Light background
    # Accent colors
    'yellow': '#b58900',
    'orange': '#cb4b16',
    'red': '#dc322f',
    'magenta': '#d33682',
    'violet': '#6c71c4',
    'blue': '#268bd2',
    'cyan': '#2aa198',
    'green': '#859900',
}

# Categorical color sequence for plots
SOLARIZED_CATEGORICAL = [
    SOLARIZED['blue'],
    SOLARIZED['orange'],
    SOLARIZED['green'],
    SOLARIZED['red'],
    SOLARIZED['violet'],
    SOLARIZED['cyan'],
    SOLARIZED['magenta'],
    SOLARIZED['yellow'],
]

# Sequential color scale for heatmaps
SOLARIZED_SEQUENTIAL = [
    [0.0, SOLARIZED['base2']],
    [0.25, SOLARIZED['yellow']],
    [0.5, SOLARIZED['orange']],
    [0.75, SOLARIZED['red']],
    [1.0, SOLARIZED['magenta']],
]

# Diverging color scale
SOLARIZED_DIVERGING = [
    [0.0, SOLARIZED['blue']],
    [0.5, SOLARIZED['base2']],
    [1.0, SOLARIZED['red']],
]


def apply_solarized_theme():
    """
    Apply Solarized theme to matplotlib, seaborn, and plotly.
    Call this function at the start of your notebook/script.
    """
    # Matplotlib configuration
    plt.rcParams.update({
        'figure.facecolor': SOLARIZED['base3'],
        'axes.facecolor': SOLARIZED['base3'],
        'axes.edgecolor': SOLARIZED['base01'],
        'axes.labelcolor': SOLARIZED['base01'],
        'text.color': SOLARIZED['base01'],
        'xtick.color': SOLARIZED['base01'],
        'ytick.color': SOLARIZED['base01'],
        'grid.color': SOLARIZED['base2'],
        'axes.prop_cycle': plt.cycler(color=SOLARIZED_CATEGORICAL),
        'figure.figsize': (10, 6),
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
    })

    # Seaborn configuration
    sns.set_theme(style="whitegrid")
    sns.set_palette(SOLARIZED_CATEGORICAL)

    # Plotly template
    pio.templates["solarized"] = go.layout.Template(
        layout=go.Layout(
            font=dict(color=SOLARIZED['base01']),
            paper_bgcolor=SOLARIZED['base3'],
            plot_bgcolor=SOLARIZED['base3'],
            colorway=SOLARIZED_CATEGORICAL,
            title=dict(font=dict(color=SOLARIZED['base01'], size=16)),
            xaxis=dict(
                gridcolor=SOLARIZED['base2'],
                linecolor=SOLARIZED['base01'],
                tickcolor=SOLARIZED['base01'],
            ),
            yaxis=dict(
                gridcolor=SOLARIZED['base2'],
                linecolor=SOLARIZED['base01'],
                tickcolor=SOLARIZED['base01'],
            ),
        )
    )
    pio.templates.default = "solarized"


def get_plotly_colorscale(scale_type: str = 'sequential') -> List:
    """
    Get Solarized color scale for Plotly.

    Args:
        scale_type: 'sequential' or 'diverging'

    Returns:
        Color scale list for Plotly
    """
    if scale_type == 'diverging':
        return SOLARIZED_DIVERGING
    return SOLARIZED_SEQUENTIAL


# =============================================================================
# DATA VALIDATION
# =============================================================================

def validate_dataframe(df: pd.DataFrame, required_columns: Optional[List[str]] = None) -> Dict:
    """
    Validate a DataFrame and return a comprehensive quality report.

    Args:
        df: DataFrame to validate
        required_columns: List of columns that must be present

    Returns:
        Dictionary containing validation results and data quality metrics
    """
    if df is None:
        raise ValueError("DataFrame cannot be None")

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    report = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'summary': {},
        'missing_data': {},
        'column_types': {},
    }

    # Basic info
    report['summary'] = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
        'duplicate_rows': df.duplicated().sum(),
    }

    # Check required columns
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            report['is_valid'] = False
            report['errors'].append(f"Missing required columns: {missing_cols}")

    # Analyze missing data
    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        report['missing_data'][col] = {
            'null_count': int(null_count),
            'null_percentage': round(null_pct, 2),
        }

        # Flag columns with high missing data
        if null_pct > 50:
            report['warnings'].append(f"Column '{col}' has {null_pct:.1f}% missing values")
        elif null_pct > 90:
            report['errors'].append(f"Column '{col}' has {null_pct:.1f}% missing values - consider dropping")

    # Column type analysis
    for col in df.columns:
        report['column_types'][col] = str(df[col].dtype)

    return report


def get_data_quality_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary DataFrame of data quality metrics for each column.

    Args:
        df: DataFrame to analyze

    Returns:
        DataFrame with quality metrics per column
    """
    quality_data = []

    for col in df.columns:
        col_data = df[col]
        null_count = col_data.isnull().sum()

        quality_data.append({
            'Column': col,
            'Data Type': str(col_data.dtype),
            'Non-Null Count': len(col_data) - null_count,
            'Null Count': null_count,
            'Null %': round((null_count / len(df)) * 100, 2),
            'Unique Values': col_data.nunique(),
            'Sample Value': col_data.dropna().iloc[0] if len(col_data.dropna()) > 0 else None,
        })

    return pd.DataFrame(quality_data)


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = 'report',
    threshold: float = 0.5,
    fill_values: Optional[Dict] = None
) -> Union[pd.DataFrame, Dict]:
    """
    Handle missing values in a DataFrame with various strategies.

    Args:
        df: DataFrame to process
        strategy: 'report' | 'drop_columns' | 'drop_rows' | 'fill'
        threshold: For drop strategies, columns/rows with null % above this are dropped
        fill_values: Dict mapping column names to fill values (for 'fill' strategy)

    Returns:
        Processed DataFrame or report dict (for 'report' strategy)
    """
    if strategy == 'report':
        return {col: df[col].isnull().sum() for col in df.columns}

    df_clean = df.copy()

    if strategy == 'drop_columns':
        cols_to_drop = [
            col for col in df.columns
            if df[col].isnull().sum() / len(df) > threshold
        ]
        df_clean = df_clean.drop(columns=cols_to_drop)

    elif strategy == 'drop_rows':
        df_clean = df_clean.dropna(thresh=int(len(df.columns) * (1 - threshold)))

    elif strategy == 'fill' and fill_values:
        for col, value in fill_values.items():
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna(value)

    return df_clean


# =============================================================================
# SEGMENTATION ANALYSIS (Modularized from notebook)
# =============================================================================

def calculate_acceptance_rate(
    df: pd.DataFrame,
    target_col: str = 'Y',
    group_by: Optional[Union[str, List[str]]] = None
) -> pd.DataFrame:
    """
    Calculate acceptance rate overall or by group.

    Args:
        df: DataFrame with coupon data
        target_col: Column containing acceptance indicator (0/1)
        group_by: Column(s) to group by, or None for overall rate

    Returns:
        DataFrame with acceptance statistics
    """
    if group_by is None:
        total = len(df)
        accepted = df[target_col].sum()
        return pd.DataFrame([{
            'Total': total,
            'Accepted': accepted,
            'Declined': total - accepted,
            'Acceptance Rate (%)': round((accepted / total) * 100, 2)
        }])

    if isinstance(group_by, str):
        group_by = [group_by]

    stats = df.groupby(group_by)[target_col].agg(['sum', 'count', 'mean'])
    stats.columns = ['Accepted', 'Total', 'Acceptance Rate']
    stats['Declined'] = stats['Total'] - stats['Accepted']
    stats['Acceptance Rate (%)'] = (stats['Acceptance Rate'] * 100).round(2)
    stats = stats.drop(columns=['Acceptance Rate'])
    stats = stats[['Total', 'Accepted', 'Declined', 'Acceptance Rate (%)']]

    return stats.reset_index()


def compare_segments(
    df: pd.DataFrame,
    condition: pd.Series,
    target_col: str = 'Y',
    segment_names: Tuple[str, str] = ('Target Group', 'All Others')
) -> pd.DataFrame:
    """
    Compare acceptance rates between a target segment and all others.

    Args:
        df: DataFrame with coupon data
        condition: Boolean Series defining the target segment
        target_col: Column containing acceptance indicator
        segment_names: Tuple of (target_name, others_name)

    Returns:
        DataFrame with comparison statistics
    """
    results = []

    for is_target, name in [(True, segment_names[0]), (False, segment_names[1])]:
        segment = df[condition] if is_target else df[~condition]
        total = len(segment)
        accepted = segment[target_col].sum()

        results.append({
            'Segment': name,
            'Total': total,
            'Accepted': accepted,
            'Declined': total - accepted,
            'Acceptance Rate (%)': round((accepted / total) * 100, 2) if total > 0 else 0
        })

    result_df = pd.DataFrame(results)

    # Calculate difference
    rate_diff = result_df.iloc[0]['Acceptance Rate (%)'] - result_df.iloc[1]['Acceptance Rate (%)']
    result_df['Rate Difference (pp)'] = [rate_diff, -rate_diff]

    return result_df


def create_frequency_segments(
    df: pd.DataFrame,
    column: str,
    thresholds: Dict[str, List[str]]
) -> pd.Series:
    """
    Create frequency-based segments from categorical frequency columns.

    Args:
        df: DataFrame
        column: Column name with frequency values (e.g., 'never', 'less1', '1~3', '4~8', 'gt8')
        thresholds: Dict mapping segment names to lists of values
                   e.g., {'Low': ['never', 'less1'], 'High': ['1~3', '4~8', 'gt8']}

    Returns:
        Series with segment labels
    """
    def map_value(val):
        for segment, values in thresholds.items():
            if val in values:
                return segment
        return 'Unknown'

    return df[column].apply(map_value)


def analyze_coupon_type(
    df: pd.DataFrame,
    coupon_type: str,
    analysis_columns: Optional[List[str]] = None
) -> Dict:
    """
    Perform comprehensive analysis for a specific coupon type.

    Args:
        df: Full DataFrame with all coupon data
        coupon_type: Type of coupon to analyze (e.g., 'Bar', 'Coffee House')
        analysis_columns: Columns to analyze for acceptance patterns

    Returns:
        Dictionary with analysis results
    """
    if analysis_columns is None:
        analysis_columns = ['age', 'gender', 'maritalStatus', 'income', 'passanger', 'destination']

    # Filter to specific coupon type
    coupon_df = df[df['coupon'] == coupon_type].copy()

    results = {
        'coupon_type': coupon_type,
        'total_records': len(coupon_df),
        'overall_acceptance': calculate_acceptance_rate(coupon_df),
        'by_dimension': {}
    }

    for col in analysis_columns:
        if col in coupon_df.columns:
            results['by_dimension'][col] = calculate_acceptance_rate(coupon_df, group_by=col)

    return results


# =============================================================================
# TIME-BASED ANALYSIS
# =============================================================================

def analyze_time_expiration(
    df: pd.DataFrame,
    target_col: str = 'Y'
) -> Dict[str, pd.DataFrame]:
    """
    Analyze coupon acceptance by time of day and expiration combinations.

    Args:
        df: DataFrame with 'time' and 'expiration' columns
        target_col: Acceptance indicator column

    Returns:
        Dictionary with various time-based analyses
    """
    results = {}

    # Acceptance by time of day
    results['by_time'] = calculate_acceptance_rate(df, target_col, 'time')

    # Acceptance by expiration
    results['by_expiration'] = calculate_acceptance_rate(df, target_col, 'expiration')

    # Cross-tabulation: time x expiration
    pivot = pd.crosstab(
        df['time'],
        df['expiration'],
        df[target_col],
        aggfunc='mean'
    ) * 100
    results['time_expiration_heatmap'] = pivot.round(2)

    # Time ordering for proper display
    time_order = ['7AM', '10AM', '2PM', '6PM', '10PM']
    if 'by_time' in results:
        results['by_time']['time'] = pd.Categorical(
            results['by_time']['time'],
            categories=time_order,
            ordered=True
        )
        results['by_time'] = results['by_time'].sort_values('time')

    return results


def analyze_time_patterns(
    df: pd.DataFrame,
    coupon_type: Optional[str] = None,
    target_col: str = 'Y'
) -> Dict:
    """
    Comprehensive time pattern analysis for coupon acceptance.

    Args:
        df: DataFrame with coupon data
        coupon_type: Optional filter for specific coupon type
        target_col: Acceptance indicator column

    Returns:
        Dictionary with time pattern insights
    """
    if coupon_type:
        df = df[df['coupon'] == coupon_type].copy()

    time_order = ['7AM', '10AM', '2PM', '6PM', '10PM']

    results = {
        'coupon_type': coupon_type or 'All',
        'total_records': len(df),
    }

    # Time analysis
    time_stats = df.groupby('time')[target_col].agg(['sum', 'count', 'mean'])
    time_stats.columns = ['Accepted', 'Total', 'Rate']
    time_stats['Rate'] = (time_stats['Rate'] * 100).round(2)
    time_stats = time_stats.reindex(time_order)
    results['by_time'] = time_stats

    # Best/worst times
    results['best_time'] = time_stats['Rate'].idxmax()
    results['worst_time'] = time_stats['Rate'].idxmin()
    results['best_rate'] = time_stats['Rate'].max()
    results['worst_rate'] = time_stats['Rate'].min()

    # Expiration analysis
    exp_stats = df.groupby('expiration')[target_col].agg(['sum', 'count', 'mean'])
    exp_stats.columns = ['Accepted', 'Total', 'Rate']
    exp_stats['Rate'] = (exp_stats['Rate'] * 100).round(2)
    results['by_expiration'] = exp_stats

    # Time x Expiration interaction
    interaction = pd.crosstab(
        df['time'],
        df['expiration'],
        df[target_col],
        aggfunc='mean'
    ) * 100
    interaction = interaction.reindex(time_order)
    results['time_expiration_matrix'] = interaction.round(2)

    return results


# =============================================================================
# VISUALIZATION HELPERS (with Solarized theme)
# =============================================================================

def plot_acceptance_by_category(
    df: pd.DataFrame,
    category_col: str,
    target_col: str = 'Y',
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    order: Optional[List[str]] = None
) -> go.Figure:
    """
    Create a bar plot showing acceptance rates by category with Solarized theme.

    Args:
        df: DataFrame with data
        category_col: Column to group by
        target_col: Acceptance indicator column
        title: Plot title
        save_path: Path to save the image
        order: Optional list specifying category order

    Returns:
        Plotly figure
    """
    stats = calculate_acceptance_rate(df, target_col, category_col)

    if order:
        stats[category_col] = pd.Categorical(stats[category_col], categories=order, ordered=True)
        stats = stats.sort_values(category_col)

    fig = px.bar(
        stats,
        x=category_col,
        y='Acceptance Rate (%)',
        title=title or f'Acceptance Rate by {category_col}',
        color='Acceptance Rate (%)',
        color_continuous_scale=get_plotly_colorscale('sequential'),
    )

    fig.update_layout(
        xaxis_title=category_col,
        yaxis_title='Acceptance Rate (%)',
    )

    if save_path:
        fig.write_image(save_path)

    return fig


def plot_acceptance_heatmap(
    df: pd.DataFrame,
    row_col: str,
    col_col: str,
    target_col: str = 'Y',
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> go.Figure:
    """
    Create a heatmap showing acceptance rates by two dimensions.

    Args:
        df: DataFrame with data
        row_col: Column for heatmap rows
        col_col: Column for heatmap columns
        target_col: Acceptance indicator column
        title: Plot title
        save_path: Path to save image

    Returns:
        Plotly figure
    """
    pivot = pd.crosstab(
        df[row_col],
        df[col_col],
        df[target_col],
        aggfunc='mean'
    ) * 100

    fig = px.imshow(
        pivot,
        labels=dict(x=col_col, y=row_col, color="Acceptance Rate (%)"),
        title=title or f'Acceptance Rate: {row_col} × {col_col}',
        color_continuous_scale=get_plotly_colorscale('sequential'),
        text_auto='.1f'
    )

    if save_path:
        fig.write_image(save_path)

    return fig


def plot_segment_comparison(
    comparison_df: pd.DataFrame,
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> go.Figure:
    """
    Create a bar plot comparing segment acceptance rates.

    Args:
        comparison_df: DataFrame from compare_segments function
        title: Plot title
        save_path: Path to save image

    Returns:
        Plotly figure
    """
    fig = px.bar(
        comparison_df,
        x='Segment',
        y='Acceptance Rate (%)',
        color='Segment',
        title=title or 'Segment Comparison',
        color_discrete_sequence=SOLARIZED_CATEGORICAL,
    )

    # Add value labels
    fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')

    if save_path:
        fig.write_image(save_path)

    return fig


def plot_time_analysis(
    time_results: Dict,
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> go.Figure:
    """
    Create visualization for time-based analysis results.

    Args:
        time_results: Results from analyze_time_patterns
        title: Plot title
        save_path: Path to save image

    Returns:
        Plotly figure with time analysis
    """
    time_data = time_results['by_time'].reset_index()

    fig = px.line(
        time_data,
        x='time',
        y='Rate',
        markers=True,
        title=title or f"Acceptance Rate by Time of Day ({time_results['coupon_type']})",
    )

    fig.update_traces(
        line=dict(color=SOLARIZED['blue'], width=3),
        marker=dict(size=10, color=SOLARIZED['orange'])
    )

    fig.update_layout(
        xaxis_title='Time of Day',
        yaxis_title='Acceptance Rate (%)',
    )

    if save_path:
        fig.write_image(save_path)

    return fig

def draw_bar_plot_column_null_values(data_frame: pd.DataFrame, save_path: str = ""):
    
    if data_frame is None:
        raise ValueError("Data parameter is required")
    
    if data_frame is None or not isinstance(data_frame, pd.DataFrame):
        raise ValueError("Data parameter must be a pandas DataFrame")
    
    rows = data_frame.shape[0]
    summary = data_frame.isnull().sum()
    fig = px.bar(x=summary.index, y=summary.values, labels={'x':'Data Set Column Names', 'y':'Number of Missing Values'}, title='Missing Values per Column')
    fig.add_hline(y=rows, line_dash="dash", line_color="red", annotation_text="Total Rows in Data Set", annotation_position="top left")
    fig.show()

    if save_path != "":
        fig.write_image(save_path) #requires kaleido package
        #plt.savefig(save_path)


def convert_categorical_to_numeric(data_frame: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Dict]]:
    """
    Convert non-numeric and non-boolean columns to numeric values using value counts.
    Returns the modified DataFrame and a dictionary mapping original values to numeric codes.
    """
    
    if data_frame is None:
        raise ValueError("Data parameter is required")
    
    if not isinstance(data_frame, pd.DataFrame):
        raise ValueError("Data parameter must be a pandas DataFrame")
    
    # Create a copy of the dataframe to avoid modifying the original
    df_numeric = data_frame.copy()
    
    # Dictionary to store the mapping of original values to numeric codes
    value_mappings = {}
    
    # Iterate through each column
    for column in df_numeric.columns:
        col_data = df_numeric[column]
        
        # Check if column is already numeric or boolean
        if pd.api.types.is_numeric_dtype(col_data) or pd.api.types.is_bool_dtype(col_data):
            continue
            
        # Get value counts for the column (excluding NaN values)
        value_counts = col_data.value_counts()
        
        # Create mapping from unique values to positive integers
        unique_values = value_counts.index.tolist()
        value_to_numeric = {value: idx + 1 for idx, value in enumerate(unique_values)}
        
        # Store the mapping for reference
        value_mappings[column] = value_to_numeric
        
        # Apply the mapping to convert categorical values to numeric
        df_numeric[column] = col_data.map(value_to_numeric)
        
        # Convert the column to numeric type (handles NaN values properly)
        df_numeric[column] = pd.to_numeric(df_numeric[column], errors='coerce')
    
    return df_numeric, value_mappings


def get_column_mapping_info(value_mappings: Dict[str, Dict]) -> pd.DataFrame:
    """
    Convert the value mappings dictionary to a readable DataFrame for inspection.

    """
    
    mapping_data = []
    
    for column, mapping in value_mappings.items():
        for original_value, numeric_code in mapping.items():
            mapping_data.append({
                'Column': column,
                'Original_Value': original_value,
                'Numeric_Code': numeric_code
            })
    
    return pd.DataFrame(mapping_data)