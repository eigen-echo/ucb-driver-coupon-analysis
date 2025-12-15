import pandas as pd
import plotly.express as px
import numpy as np
from typing import Dict, Tuple

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