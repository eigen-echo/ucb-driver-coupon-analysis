"""
UCB Driver Coupon Analysis - Interactive Dashboard

An interactive Streamlit dashboard for exploring the UCI Driver Coupon dataset.
Provides visual analytics for understanding factors that influence coupon acceptance.

Pages:
    - Overview: Key metrics, acceptance rates by coupon type, heatmaps
    - Coupon Type Analysis: Deep-dive into demographics, behavior, and context
    - Time Analysis: Time-of-day patterns and expiration impact
    - Segment Explorer: Build and compare custom driver segments
    - Custom Analysis: Create pivot tables with any variables

Run with:
    streamlit run dashboard.py

Configuration:
    Dark theme is configured via .streamlit/config.toml
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path for helper imports
sys.path.insert(0, str(Path(__file__).parent))
from src.helpers import (
    SOLARIZED,
    SOLARIZED_CATEGORICAL,
    SOLARIZED_SEQUENTIAL,
    calculate_acceptance_rate,
    compare_segments,
    create_frequency_segments,
    analyze_time_patterns,
)

# Page config
st.set_page_config(
    page_title="Driver Coupon Analysis",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme colors
DARK_THEME = {
    'bg': '#0e1117',
    'secondary_bg': '#262730',
    'text': '#fafafa',
    'accent': '#ff4b4b',
}

# Dark mode color palette for charts
DARK_CATEGORICAL = [
    '#636efa',  # blue
    '#ef553b',  # red
    '#00cc96',  # green
    '#ab63fa',  # purple
    '#ffa15a',  # orange
    '#19d3f3',  # cyan
    '#ff6692',  # pink
    '#b6e880',  # lime
]

DARK_SEQUENTIAL = [
    [0.0, '#0d0887'],
    [0.25, '#7201a8'],
    [0.5, '#bd3786'],
    [0.75, '#ed7953'],
    [1.0, '#fdca26'],
]


@st.cache_data
def load_data():
    """Load and cache the coupon dataset."""
    data_path = Path(__file__).parent / "data" / "coupons.csv"
    df = pd.read_csv(data_path)
    # Drop car column (99% missing)
    if 'car' in df.columns:
        df = df.drop(columns=['car'])
    return df


def create_plotly_template():
    """Create dark mode Plotly template."""
    return 'plotly_dark'


def main():
    # Load data
    data = load_data()

    # Sidebar
    st.sidebar.title("🎫 Coupon Analysis")
    st.sidebar.markdown("---")

    # Navigation
    page = st.sidebar.radio(
        "Navigate to:",
        ["Overview", "Coupon Type Analysis", "Time Analysis", "Segment Explorer", "Custom Analysis"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filters")

    # Global filters
    selected_coupons = st.sidebar.multiselect(
        "Coupon Types",
        options=data['coupon'].unique(),
        default=data['coupon'].unique()
    )

    selected_weather = st.sidebar.multiselect(
        "Weather",
        options=data['weather'].unique(),
        default=data['weather'].unique()
    )

    temperature_range = st.sidebar.slider(
        "Temperature (°F)",
        min_value=int(data['temperature'].min()),
        max_value=int(data['temperature'].max()),
        value=(int(data['temperature'].min()), int(data['temperature'].max()))
    )

    # Apply filters
    filtered_data = data[
        (data['coupon'].isin(selected_coupons)) &
        (data['weather'].isin(selected_weather)) &
        (data['temperature'] >= temperature_range[0]) &
        (data['temperature'] <= temperature_range[1])
    ]

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Filtered Records:** {len(filtered_data):,} / {len(data):,}")

    # Page content
    if page == "Overview":
        render_overview(filtered_data, data)
    elif page == "Coupon Type Analysis":
        render_coupon_analysis(filtered_data)
    elif page == "Time Analysis":
        render_time_analysis(filtered_data)
    elif page == "Segment Explorer":
        render_segment_explorer(filtered_data)
    elif page == "Custom Analysis":
        render_custom_analysis(filtered_data)


def render_overview(filtered_data, full_data):
    """Render the overview dashboard page."""
    st.title("📊 Driver Coupon Acceptance Analysis")
    st.markdown("Exploring factors that influence whether drivers accept mobile coupons.")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    total_records = len(filtered_data)
    acceptance_rate = (filtered_data['Y'].sum() / total_records * 100) if total_records > 0 else 0
    accepted = filtered_data['Y'].sum()
    declined = total_records - accepted

    col1.metric("Total Records", f"{total_records:,}")
    col2.metric("Acceptance Rate", f"{acceptance_rate:.1f}%")
    col3.metric("Accepted", f"{accepted:,}")
    col4.metric("Declined", f"{declined:,}")

    st.markdown("---")

    # Two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Acceptance by Coupon Type")
        coupon_stats = calculate_acceptance_rate(filtered_data, group_by='coupon')
        fig = px.bar(
            coupon_stats.sort_values('Acceptance Rate (%)', ascending=True),
            x='Acceptance Rate (%)',
            y='coupon',
            orientation='h',
            color='Acceptance Rate (%)',
            color_continuous_scale=DARK_SEQUENTIAL,
            template=create_plotly_template()
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Acceptance Distribution")
        fig = px.pie(
            filtered_data,
            names=filtered_data['Y'].map({1: 'Accepted', 0: 'Declined'}),
            color_discrete_sequence=['#00cc96', '#ef553b'],  # green, red
            template=create_plotly_template()
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    st.subheader("Acceptance Rate: Destination × Passenger Type")
    pivot = pd.crosstab(
        filtered_data['destination'],
        filtered_data['passanger'],
        filtered_data['Y'],
        aggfunc='mean'
    ) * 100

    fig = px.imshow(
        pivot,
        labels=dict(x="Passenger Type", y="Destination", color="Acceptance Rate (%)"),
        color_continuous_scale=SOLARIZED_SEQUENTIAL,
        text_auto='.1f',
        template=create_plotly_template()
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def render_coupon_analysis(data):
    """Render coupon type analysis page."""
    st.title("🎫 Coupon Type Analysis")

    # Coupon selector
    coupon_type = st.selectbox(
        "Select Coupon Type",
        options=data['coupon'].unique()
    )

    coupon_data = data[data['coupon'] == coupon_type]

    # Metrics
    col1, col2, col3 = st.columns(3)
    total = len(coupon_data)
    rate = (coupon_data['Y'].sum() / total * 100) if total > 0 else 0

    col1.metric("Total Records", f"{total:,}")
    col2.metric("Acceptance Rate", f"{rate:.1f}%")
    col3.metric("vs Overall", f"{rate - (data['Y'].mean() * 100):+.1f}%")

    st.markdown("---")

    # Analysis tabs
    tab1, tab2, tab3 = st.tabs(["Demographics", "Behavior", "Context"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("By Age Group")
            age_stats = calculate_acceptance_rate(coupon_data, group_by='age')
            age_order = ['below21', '21', '26', '31', '36', '41', '46', '50plus']
            age_stats['age'] = pd.Categorical(age_stats['age'], categories=age_order, ordered=True)
            age_stats = age_stats.sort_values('age')

            fig = px.bar(
                age_stats,
                x='age',
                y='Acceptance Rate (%)',
                color='Acceptance Rate (%)',
                color_continuous_scale=DARK_SEQUENTIAL,
                template=create_plotly_template()
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("By Gender")
            gender_stats = calculate_acceptance_rate(coupon_data, group_by='gender')
            fig = px.bar(
                gender_stats,
                x='gender',
                y='Acceptance Rate (%)',
                color='gender',
                color_discrete_sequence=DARK_CATEGORICAL,
                template=create_plotly_template()
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("By Income Level")
        income_stats = calculate_acceptance_rate(coupon_data, group_by='income')
        fig = px.bar(
            income_stats.sort_values('Acceptance Rate (%)', ascending=False),
            x='income',
            y='Acceptance Rate (%)',
            color='Acceptance Rate (%)',
            color_continuous_scale=DARK_SEQUENTIAL,
            template=create_plotly_template()
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Frequency column mapping
        freq_col_map = {
            'Bar': 'Bar',
            'Coffee House': 'CoffeeHouse',
            'Carry out & Take away': 'CarryAway',
            'Restaurant(<20)': 'RestaurantLessThan20',
            'Restaurant(20-50)': 'Restaurant20To50'
        }

        freq_col = freq_col_map.get(coupon_type)

        if freq_col and freq_col in coupon_data.columns:
            st.subheader(f"By {coupon_type} Visit Frequency")
            freq_stats = calculate_acceptance_rate(coupon_data, group_by=freq_col)
            freq_order = ['never', 'less1', '1~3', '4~8', 'gt8']
            freq_stats[freq_col] = pd.Categorical(freq_stats[freq_col], categories=freq_order, ordered=True)
            freq_stats = freq_stats.sort_values(freq_col)

            fig = px.bar(
                freq_stats,
                x=freq_col,
                y='Acceptance Rate (%)',
                color='Acceptance Rate (%)',
                color_continuous_scale=DARK_SEQUENTIAL,
                template=create_plotly_template()
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("By Passenger Type")
            pass_stats = calculate_acceptance_rate(coupon_data, group_by='passanger')
            fig = px.bar(
                pass_stats.sort_values('Acceptance Rate (%)', ascending=False),
                x='passanger',
                y='Acceptance Rate (%)',
                color='Acceptance Rate (%)',
                color_continuous_scale=DARK_SEQUENTIAL,
                template=create_plotly_template()
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("By Destination")
            dest_stats = calculate_acceptance_rate(coupon_data, group_by='destination')
            fig = px.bar(
                dest_stats.sort_values('Acceptance Rate (%)', ascending=False),
                x='destination',
                y='Acceptance Rate (%)',
                color='Acceptance Rate (%)',
                color_continuous_scale=DARK_SEQUENTIAL,
                template=create_plotly_template()
            )
            st.plotly_chart(fig, use_container_width=True)


def render_time_analysis(data):
    """Render time-based analysis page."""
    st.title("⏰ Time-Based Analysis")

    # Overall time analysis
    time_analysis = analyze_time_patterns(data)

    col1, col2 = st.columns(2)
    col1.metric("Best Time", f"{time_analysis['best_time']} ({time_analysis['best_rate']}%)")
    col2.metric("Worst Time", f"{time_analysis['worst_time']} ({time_analysis['worst_rate']}%)")

    st.markdown("---")

    # Time of day analysis
    st.subheader("Acceptance Rate by Time of Day")
    time_stats = time_analysis['by_time'].reset_index()
    time_order = ['7AM', '10AM', '2PM', '6PM', '10PM']
    time_stats['time'] = pd.Categorical(time_stats['time'], categories=time_order, ordered=True)
    time_stats = time_stats.sort_values('time')

    fig = px.line(
        time_stats,
        x='time',
        y='Rate',
        markers=True,
        template=create_plotly_template()
    )
    fig.update_traces(
        line=dict(color='#636efa', width=3),
        marker=dict(size=12, color='#ffa15a')
    )
    fig.update_layout(yaxis_title="Acceptance Rate (%)")
    st.plotly_chart(fig, use_container_width=True)

    # Expiration analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("By Expiration Duration")
        exp_stats = time_analysis['by_expiration'].reset_index()
        fig = px.bar(
            exp_stats,
            x='expiration',
            y='Rate',
            color='expiration',
            color_discrete_sequence=DARK_CATEGORICAL,
            template=create_plotly_template()
        )
        fig.update_layout(yaxis_title="Acceptance Rate (%)", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Time × Expiration Heatmap")
        pivot = pd.crosstab(
            data['time'],
            data['expiration'],
            data['Y'],
            aggfunc='mean'
        ) * 100
        pivot = pivot.reindex(time_order)

        fig = px.imshow(
            pivot,
            labels=dict(x="Expiration", y="Time", color="Rate (%)"),
            color_continuous_scale=DARK_SEQUENTIAL,
            text_auto='.1f',
            template=create_plotly_template()
        )
        st.plotly_chart(fig, use_container_width=True)

    # Time by coupon type
    st.subheader("Optimal Times by Coupon Type")
    time_by_coupon = []
    for ct in data['coupon'].unique():
        ct_analysis = analyze_time_patterns(data, coupon_type=ct)
        time_by_coupon.append({
            'Coupon Type': ct,
            'Best Time': ct_analysis['best_time'],
            'Best Rate (%)': ct_analysis['best_rate'],
            'Worst Time': ct_analysis['worst_time'],
            'Worst Rate (%)': ct_analysis['worst_rate']
        })

    st.dataframe(pd.DataFrame(time_by_coupon), use_container_width=True)


def render_segment_explorer(data):
    """Render segment comparison tool."""
    st.title("🔍 Segment Explorer")
    st.markdown("Compare acceptance rates between custom segments.")

    # Segment builder
    st.subheader("Build Your Segment")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Segment A (Target)**")

        seg_a_age = st.multiselect(
            "Age Groups (A)",
            options=data['age'].unique(),
            default=[]
        )

        seg_a_passenger = st.multiselect(
            "Passenger Types (A)",
            options=data['passanger'].unique(),
            default=[]
        )

        seg_a_destination = st.multiselect(
            "Destinations (A)",
            options=data['destination'].unique(),
            default=[]
        )

    with col2:
        st.markdown("**Additional Filters (A)**")

        seg_a_income = st.multiselect(
            "Income Levels (A)",
            options=data['income'].unique(),
            default=[]
        )

        seg_a_marital = st.multiselect(
            "Marital Status (A)",
            options=data['maritalStatus'].unique(),
            default=[]
        )

    # Build condition
    condition = pd.Series([True] * len(data), index=data.index)

    if seg_a_age:
        condition = condition & data['age'].isin(seg_a_age)
    if seg_a_passenger:
        condition = condition & data['passanger'].isin(seg_a_passenger)
    if seg_a_destination:
        condition = condition & data['destination'].isin(seg_a_destination)
    if seg_a_income:
        condition = condition & data['income'].isin(seg_a_income)
    if seg_a_marital:
        condition = condition & data['maritalStatus'].isin(seg_a_marital)

    # If no filters selected, show message
    if not any([seg_a_age, seg_a_passenger, seg_a_destination, seg_a_income, seg_a_marital]):
        st.info("Select at least one filter to define your target segment.")
        return

    # Compare segments
    comparison = compare_segments(data, condition, segment_names=('Target Segment', 'All Others'))

    st.markdown("---")
    st.subheader("Segment Comparison Results")

    # Display results
    col1, col2, col3 = st.columns(3)

    target_rate = comparison[comparison['Segment'] == 'Target Segment']['Acceptance Rate (%)'].values[0]
    others_rate = comparison[comparison['Segment'] == 'All Others']['Acceptance Rate (%)'].values[0]
    diff = target_rate - others_rate

    col1.metric("Target Segment", f"{target_rate:.1f}%", f"{comparison[comparison['Segment'] == 'Target Segment']['Total'].values[0]:,} records")
    col2.metric("All Others", f"{others_rate:.1f}%", f"{comparison[comparison['Segment'] == 'All Others']['Total'].values[0]:,} records")
    col3.metric("Difference", f"{diff:+.1f}%", "Higher" if diff > 0 else "Lower")

    # Visualization
    fig = px.bar(
        comparison,
        x='Segment',
        y='Acceptance Rate (%)',
        color='Segment',
        color_discrete_sequence=DARK_CATEGORICAL,
        template=create_plotly_template()
    )
    fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Detailed stats
    st.subheader("Detailed Statistics")
    st.dataframe(comparison, use_container_width=True)


def render_custom_analysis(data):
    """Render custom analysis page with pivot table functionality."""
    st.title("📈 Custom Analysis")
    st.markdown("Create custom pivot tables and visualizations.")

    col1, col2 = st.columns(2)

    with col1:
        row_var = st.selectbox(
            "Row Variable",
            options=['age', 'gender', 'maritalStatus', 'income', 'occupation', 'destination', 'passanger', 'weather', 'time', 'expiration', 'coupon']
        )

    with col2:
        col_var = st.selectbox(
            "Column Variable",
            options=['coupon', 'passanger', 'destination', 'time', 'expiration', 'weather', 'gender', 'age'],
            index=0
        )

    # Create pivot table
    pivot = pd.crosstab(
        data[row_var],
        data[col_var],
        data['Y'],
        aggfunc='mean'
    ) * 100

    # Visualization type
    viz_type = st.radio("Visualization Type", ["Heatmap", "Grouped Bar Chart"], horizontal=True)

    if viz_type == "Heatmap":
        fig = px.imshow(
            pivot,
            labels=dict(x=col_var, y=row_var, color="Acceptance Rate (%)"),
            color_continuous_scale=DARK_SEQUENTIAL,
            text_auto='.1f',
            template=create_plotly_template()
        )
        fig.update_layout(height=600)
    else:
        pivot_reset = pivot.reset_index().melt(id_vars=row_var, var_name=col_var, value_name='Acceptance Rate (%)')
        fig = px.bar(
            pivot_reset,
            x=row_var,
            y='Acceptance Rate (%)',
            color=col_var,
            barmode='group',
            color_discrete_sequence=DARK_CATEGORICAL,
            template=create_plotly_template()
        )
        fig.update_layout(height=600, xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)

    # Show data table
    with st.expander("View Data Table"):
        st.dataframe(pivot.round(2), use_container_width=True)


if __name__ == "__main__":
    main()
