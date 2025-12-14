import pandas as pd
import plotly.express as px

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