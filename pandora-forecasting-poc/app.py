"""
Pandora AI Store Traffic & Staffing Optimizer
A premium Streamlit application for demonstrating AI-driven forecasting
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, date
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Pandora AI Traffic Optimizer",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING - Minimalist Design
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #FAFAFA 0%, #F5F5F5 100%);
        padding: 1.5rem;
    }

    .stApp {
        background: linear-gradient(135deg, #FAFAFA 0%, #F5F5F5 100%);
    }

    h1, h2, h3, h4 {
        color: #1A1A1A;
        font-weight: 600;
    }

    /* Grid Container */
    .grid-container {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }

    /* KPI Cards - Minimalist */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E8E8E8;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.2s ease;
    }

    .kpi-card:hover {
        box-shadow: 0 4px 12px rgba(242, 184, 198, 0.1);
        border-color: #F2B8C6;
    }

    .kpi-card[title] {
        cursor: help;
    }

    /* Tooltip styling */
    .kpi-card-with-tooltip {
        position: relative;
    }

    .kpi-card-with-tooltip .tooltip-text {
        visibility: hidden;
        width: 320px;
        background-color: #2C2C2C;
        color: #FFFFFF;
        text-align: left;
        border-radius: 8px;
        padding: 12px 16px;
        position: absolute;
        z-index: 1000;
        top: 125%;
        left: 50%;
        margin-left: -160px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        line-height: 1.5;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .kpi-card-with-tooltip .tooltip-text::after {
        content: "";
        position: absolute;
        bottom: 100%;
        left: 50%;
        margin-left: -8px;
        border-width: 8px;
        border-style: solid;
        border-color: transparent transparent #2C2C2C transparent;
    }

    .kpi-card-with-tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }

    .kpi-title {
        color: #6B6B6B;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
    }

    .kpi-value {
        color: #F2B8C6;
        font-size: 40px;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 8px;
    }

    .kpi-subtitle {
        color: #999999;
        font-size: 11px;
        font-weight: 400;
    }

    /* Status Badges */
    .status-badge {
        background-color: #FAFAFA;
        border: 1px solid #E8E8E8;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .status-title {
        color: #6B6B6B;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }

    .status-value {
        color: #1A1A1A;
        font-size: 14px;
        font-weight: 600;
    }

    /* Buttons */
    .stButton > button {
        background-color: #F2B8C6;
        color: #1A1A1A;
        border: none;
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 600;
        font-size: 13px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 6px rgba(242, 184, 198, 0.2);
        white-space: nowrap;
    }

    .stButton > button:hover {
        background-color: #E8A5B5;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(242, 184, 198, 0.3);
    }

    /* Section Headers */
    .section-header {
        background: #FFFFFF;
        padding: 16px 20px;
        border-radius: 10px;
        border-left: 4px solid #F2B8C6;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
    }

    /* Remove extra padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
        max-width: 1400px;
    }

    /* Metric styling - ensure text is dark */
    [data-testid="stMetricLabel"] {
        color: #1A1A1A !important;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #1A1A1A !important;
        font-weight: 700;
    }

    [data-testid="stMetricDelta"] {
        color: #1A1A1A !important;
    }

    /* Adjustment preview container */
    .adjustment-preview {
        background: #FFFFFF;
        border: 1px solid #E8E8E8;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
    }

    .adjustment-preview [data-testid="stMetricLabel"],
    .adjustment-preview [data-testid="stMetricValue"],
    .adjustment-preview [data-testid="stMetricDelta"] {
        color: #1A1A1A !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

@st.cache_data
def generate_store_hourly_data(store_name, date):
    """
    Generate hourly synthetic data for a specific store

    Args:
        store_name: Name of the store
        date: Date for the forecast

    Returns:
        DataFrame with hourly traffic and staffing data
    """
    np.random.seed(hash(store_name) % 10000)

    # Operating hours: 9 AM to 9 PM
    hours = [f"{h:02d}:00" for h in range(9, 21)]

    # Store-specific parameters
    store_params = {
        "London": {"base": 110, "peak_boost": 45, "peak_hours": [12, 13, 17, 18, 19]},
        "Copenhagen": {"base": 80, "peak_boost": 35, "peak_hours": [11, 14, 16, 18]},
        "Paris": {"base": 90, "peak_boost": 40, "peak_hours": [13, 15, 17, 18]}
    }

    params = store_params.get(store_name, {"base": 100, "peak_boost": 35, "peak_hours": [12, 18]})

    # Check if selected date is today or in the past
    today = datetime.now().date()
    selected_date_obj = date.date() if isinstance(date, datetime) else date
    is_today = selected_date_obj == today
    is_past = selected_date_obj < today
    current_hour = datetime.now().hour

    # Generate hourly data
    data = []
    for i, hour in enumerate(hours):
        hour_num = int(hour.split(':')[0])

        # Base traffic with random variation
        traffic = params["base"] + np.random.randint(-8, 12)

        # Peak hour boost
        if hour_num in params["peak_hours"]:
            traffic += params["peak_boost"]

        # Gradual increase throughout the day
        traffic += int(i * 4.5)

        # Generate actual traffic (with slight variance from predicted)
        actual_traffic = None
        if is_past:
            # Past date: show actual traffic for all hours
            variance = np.random.uniform(-0.08, 0.08)
            actual_traffic = int(traffic * (1 + variance))
        elif is_today and hour_num < current_hour:
            # Today: show actual traffic only for hours that have passed
            variance = np.random.uniform(-0.08, 0.08)
            actual_traffic = int(traffic * (1 + variance))
        # Future dates or future hours: actual_traffic remains None

        # Baseline staffing (legacy - flat)
        baseline_staff = params["base"] - 15

        # AI recommended (matches traffic)
        ai_staff = int(traffic * 0.93)

        data.append({
            'Hour': hour,
            'Predicted_Traffic': traffic,
            'Actual_Traffic': actual_traffic,
            'Baseline_Staffing': baseline_staff,
            'AI_Recommended_Staffing': ai_staff
        })

    return pd.DataFrame(data)

@st.cache_data
def generate_store_daily_data(store_name, date):
    """
    Generate daily synthetic data for a specific store (7 days)

    Args:
        store_name: Name of the store
        date: Starting date for the forecast

    Returns:
        DataFrame with daily traffic and staffing data
    """
    np.random.seed(hash(store_name) % 10000)

    # Days of the week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Store-specific parameters
    store_params = {
        "London": {"base": 950, "weekend_boost": 450, "peak_days": [4, 5, 6]},  # Fri, Sat, Sun
        "Copenhagen": {"base": 720, "weekend_boost": 320, "peak_days": [3, 5, 6]},  # Thu, Sat, Sun
        "Paris": {"base": 810, "weekend_boost": 380, "peak_days": [4, 5, 6]}   # Fri, Sat, Sun
    }

    params = store_params.get(store_name, {"base": 850, "weekend_boost": 350, "peak_days": [5, 6]})

    # Determine which days should show actual traffic based on selected date
    today = datetime.now().date()
    selected_date_obj = date.date() if isinstance(date, datetime) else date

    # For weekly view, we show the current week starting from Monday
    # Calculate which day of the week today is (0=Monday, 6=Sunday)
    today_day_index = datetime.now().weekday()

    # Check if selected date is past, present, or future
    is_past_week = selected_date_obj < today
    is_current_week = selected_date_obj == today
    is_future_week = selected_date_obj > today

    # Generate daily data
    data = []
    for i, day in enumerate(days):
        # Base traffic with random variation
        traffic = params["base"] + np.random.randint(-50, 80)

        # Weekend/peak day boost
        if i in params["peak_days"]:
            traffic += params["weekend_boost"]

        # Generate actual traffic (with slight variance from predicted)
        actual_traffic = None
        if is_past_week:
            # Past week: show actual for all days
            variance = np.random.uniform(-0.08, 0.08)
            actual_traffic = int(traffic * (1 + variance))
        elif is_current_week:
            # Current week: show actual only up to today
            if i < today_day_index:  # Days before today
                variance = np.random.uniform(-0.08, 0.08)
                actual_traffic = int(traffic * (1 + variance))
            elif i == today_day_index:  # Today
                variance = np.random.uniform(-0.08, 0.08)
                actual_traffic = int(traffic * (1 + variance))
        # Future week: actual_traffic remains None

        # Baseline staffing (legacy - flat)
        baseline_staff = params["base"] - 120

        # AI recommended (matches traffic)
        ai_staff = int(traffic * 0.93)

        data.append({
            'Day': day,
            'Predicted_Traffic': traffic,
            'Actual_Traffic': actual_traffic,
            'Baseline_Staffing': baseline_staff,
            'AI_Recommended_Staffing': ai_staff
        })

    return pd.DataFrame(data)

@st.cache_data
def generate_all_stores_data(date, view_mode='hourly'):
    """Generate data for all stores"""
    stores = ["London", "Copenhagen", "Paris"]
    stores_data = {}

    for store in stores:
        if view_mode == 'hourly':
            stores_data[store] = generate_store_hourly_data(store, date)
        else:  # daily
            stores_data[store] = generate_store_daily_data(store, date)

    return stores_data

@st.cache_data
def calculate_aggregate_data(stores_data, view_mode='hourly'):
    """Calculate aggregate data across all stores"""
    # Determine the time column name based on view mode
    time_col = 'Hour' if view_mode == 'hourly' else 'Day'
    time_values = stores_data["London"][time_col].tolist()

    aggregate = pd.DataFrame({time_col: time_values})

    # Sum traffic across stores
    for store_name, df in stores_data.items():
        aggregate[store_name] = df['Predicted_Traffic'].values

    aggregate['Total_Traffic'] = aggregate[["London", "Copenhagen", "Paris"]].sum(axis=1)

    return aggregate

def calculate_kpis(scope, stores_data, aggregate_data):
    """Calculate KPIs based on selected scope"""
    view_mode = st.session_state.view_mode

    if scope == "All Stores (Aggregate)":
        total_traffic = int(aggregate_data['Total_Traffic'].sum())
        # Potential Sales: 20% conversion rate * $125 avg ticket * 7.45 DKK/USD = 931.25 DKK per sale
        revenue = int(total_traffic * 0.20 * 931.25)

        # Calculate efficiency across all stores
        forecasted_fte = 0
        realized_fte = 0

        for store_name, df in stores_data.items():
            store_history = st.session_state.implementation_history.get(store_name, {})

            for idx, row in df.iterrows():
                # Calculate the actual date for this row
                if view_mode == 'hourly':
                    # All hours are from selected_date
                    row_date = selected_date
                else:  # daily
                    # Calculate which date this day represents
                    # Get the Monday of the week containing selected_date
                    selected_weekday = selected_date.weekday()  # 0=Monday, 6=Sunday
                    week_start = selected_date - timedelta(days=selected_weekday)

                    # Map day name to date
                    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    day_index = day_names.index(row['Day'])
                    row_date = week_start + timedelta(days=day_index)

                date_key = row_date.strftime('%Y-%m-%d')

                # Forecasted FTE (AI recommendation based on predicted traffic)
                forecasted_fte += row['Predicted_Traffic'] / 50

                # Realized FTE based on implementation decision
                decision = store_history.get(date_key, {}).get('decision', None)

                if decision == 1:  # Following AI
                    realized_fte += row['AI_Recommended_Staffing'] / 50
                elif decision == 0:  # Using Legacy
                    realized_fte += row['Baseline_Staffing'] / 50
                else:  # No decision yet, assume AI
                    realized_fte += row['AI_Recommended_Staffing'] / 50

        efficiency = int((realized_fte / forecasted_fte * 100)) if forecasted_fte > 0 else 100
    else:
        df = stores_data[scope]
        total_traffic = int(df['Predicted_Traffic'].sum())
        # Potential Sales: 20% conversion rate * $125 avg ticket * 7.45 DKK/USD = 931.25 DKK per sale
        revenue = int(total_traffic * 0.20 * 931.25)

        # Calculate efficiency for individual store
        forecasted_fte = 0
        realized_fte = 0

        store_history = st.session_state.implementation_history.get(scope, {})

        for idx, row in df.iterrows():
            # Calculate the actual date for this row
            if view_mode == 'hourly':
                # All hours are from selected_date
                row_date = selected_date
            else:  # daily
                # Calculate which date this day represents
                selected_weekday = selected_date.weekday()  # 0=Monday, 6=Sunday
                week_start = selected_date - timedelta(days=selected_weekday)

                # Map day name to date
                day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_index = day_names.index(row['Day'])
                row_date = week_start + timedelta(days=day_index)

            date_key = row_date.strftime('%Y-%m-%d')

            # Forecasted FTE (AI recommendation based on predicted traffic)
            forecasted_fte += row['Predicted_Traffic'] / 50

            # Realized FTE based on implementation decision
            decision = store_history.get(date_key, {}).get('decision', None)

            if decision == 1:  # Following AI
                realized_fte += row['AI_Recommended_Staffing'] / 50
            elif decision == 0:  # Using Legacy
                realized_fte += row['Baseline_Staffing'] / 50
            else:  # No decision yet, assume AI
                realized_fte += row['AI_Recommended_Staffing'] / 50

        efficiency = int((realized_fte / forecasted_fte * 100)) if forecasted_fte > 0 else 100

    return total_traffic, revenue, efficiency

def calculate_forecast_accuracy(scope, stores_data, aggregate_data, selected_date):
    """
    Calculate forecast accuracy by comparing actual vs predicted traffic
    Returns accuracy for today, 3-day average, and weekly average

    Uses current stores_data to calculate accuracy efficiently
    """
    today = datetime.now().date()

    # Convert selected_date to date object if needed
    # Check datetime first since it's a subclass of date
    if hasattr(selected_date, 'date') and callable(selected_date.date):
        selected_date_obj = selected_date.date()
    else:
        selected_date_obj = selected_date

    # Check if we have actual data (past dates only)
    has_actual_data = selected_date_obj <= today

    if not has_actual_data:
        # Future dates - no actual data, return N/A or default values
        return 0.0, 0.0, 0.0

    # Calculate accuracy from current data (has actual traffic where available)
    accuracy_values = []

    if scope == "All Stores (Aggregate)":
        # Calculate across all stores
        for store_name, df in stores_data.items():
            for _, row in df.iterrows():
                if row['Actual_Traffic'] is not None and row['Actual_Traffic'] > 0:
                    predicted = row['Predicted_Traffic']
                    actual = row['Actual_Traffic']
                    # Accuracy = 1 - (absolute error / predicted)
                    accuracy = max(0, 1 - abs(predicted - actual) / predicted)
                    accuracy_values.append(accuracy * 100)
    else:
        # Individual store
        df = stores_data[scope]
        for _, row in df.iterrows():
            if row['Actual_Traffic'] is not None and row['Actual_Traffic'] > 0:
                predicted = row['Predicted_Traffic']
                actual = row['Actual_Traffic']
                accuracy = max(0, 1 - abs(predicted - actual) / predicted)
                accuracy_values.append(accuracy * 100)

    # Base accuracy from current data
    base_accuracy = np.mean(accuracy_values) if accuracy_values else 92.0

    # Create a unique seed based on selected_date AND scope
    # This ensures different dates and different stores have different accuracy values
    seed_value = selected_date_obj.toordinal() + hash(scope) % 1000
    np.random.seed(seed_value)

    # Add slight variations for different time periods
    # Today: Base accuracy with small random variance
    accuracy_today = base_accuracy + np.random.uniform(-0.5, 0.5)

    # 3 Days: Slightly smoother (less variance)
    accuracy_3days = base_accuracy + np.random.uniform(-0.3, 0.3)

    # Week: Even smoother (rolling average effect)
    accuracy_week = base_accuracy + np.random.uniform(-0.2, 0.2)

    # Ensure values are within reasonable bounds
    accuracy_today = np.clip(accuracy_today, 88.0, 98.0)
    accuracy_3days = np.clip(accuracy_3days, 88.0, 98.0)
    accuracy_week = np.clip(accuracy_week, 88.0, 98.0)

    return accuracy_today, accuracy_3days, accuracy_week

def apply_traffic_adjustments(stores_data, adjustments_dict, view_mode='hourly'):
    """
    Apply manual traffic adjustments and recalculate AI staffing recommendations

    Args:
        stores_data: Dictionary of store dataframes
        adjustments_dict: Dictionary of adjustments per store
        view_mode: 'hourly' or 'daily'

    Returns:
        Updated stores_data with adjusted predictions
    """
    adjusted_data = {}
    time_col = 'Hour' if view_mode == 'hourly' else 'Day'

    for store_name, df in stores_data.items():
        df_copy = df.copy()

        # Apply adjustments if any exist for this store
        if store_name in adjustments_dict and adjustments_dict[store_name]:
            for time_value, adjustment in adjustments_dict[store_name].items():
                # Find the row for this time period
                mask = df_copy[time_col] == time_value
                if mask.any():
                    # Apply percentage adjustment
                    original_value = df_copy.loc[mask, 'Predicted_Traffic'].values[0]
                    adjusted_value = int(original_value * (1 + adjustment / 100))
                    df_copy.loc[mask, 'Predicted_Traffic'] = adjusted_value

                    # Recalculate AI recommended staffing based on new traffic
                    df_copy.loc[mask, 'AI_Recommended_Staffing'] = int(adjusted_value * 0.93)

        adjusted_data[store_name] = df_copy

    return adjusted_data

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'traffic_adjustments' not in st.session_state:
    st.session_state.traffic_adjustments = {
        "London": {},
        "Copenhagen": {},
        "Paris": {}
    }
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'hourly'
if 'implementation_history' not in st.session_state:
    # Generate mock historical implementation data per store (last 29 days, excluding today)
    import random
    np.random.seed(42)

    stores = ["London", "Copenhagen", "Paris"]
    history = {}

    for store in stores:
        history[store] = {}
        # Generate 29 days of mock data (excluding today so user can make today's choice)
        for i in range(1, 30):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            # Simulate historical implementation decisions - different adoption rates per store
            # 1 = Following AI, 0 = Using Legacy
            if store == "London":
                # London has high adoption (85%)
                decision = 1 if random.random() < 0.85 else 0
            elif store == "Copenhagen":
                # Copenhagen has medium adoption (70%)
                decision = 1 if random.random() < 0.70 else 0
            else:  # Paris
                # Paris has high adoption (90%)
                decision = 1 if random.random() < 0.90 else 0

            history[store][date] = {'decision': decision}

    st.session_state.implementation_history = history

# ============================================================================
# HELPER FUNCTIONS FOR FEEDBACK
# ============================================================================

@st.cache_data
def generate_implementation_calendar(store_name):
    """Generate a calendar heatmap of AI adoption for a specific store"""
    # Get last 30 days including today
    dates = []
    decisions = []

    for i in range(30):
        date = datetime.now() - timedelta(days=29-i)
        date_str = date.strftime('%Y-%m-%d')

        if store_name in st.session_state.implementation_history and date_str in st.session_state.implementation_history[store_name]:
            implementation = st.session_state.implementation_history[store_name][date_str]
            decision = implementation['decision']  # 1 = AI, 0 = Legacy
        else:
            decision = None

        dates.append(date)
        decisions.append(decision)

    # Create calendar grid data
    df_calendar = pd.DataFrame({
        'Date': dates,
        'Decision': decisions,  # 1 = Following AI, 0 = Using Legacy, None = No decision yet
        'Day': [d.strftime('%a') for d in dates],
        'Week': [(d - dates[0]).days // 7 for d in dates]
    })

    return df_calendar

@st.cache_data
def get_store_adoption_summary():
    """Get AI adoption rate for all stores (for regional manager view)"""
    stores = ["London", "Copenhagen", "Paris"]
    summary = []

    for store in stores:
        if store in st.session_state.implementation_history:
            total_days = 0
            ai_days = 0

            for date_str, implementation in st.session_state.implementation_history[store].items():
                total_days += 1
                if implementation['decision'] == 1:  # Following AI
                    ai_days += 1

            if total_days > 0:
                adoption_rate = (ai_days / total_days) * 100
            else:
                adoption_rate = 0

            summary.append({
                'Store': store,
                'Adoption_Rate': adoption_rate,
                'Total_Days': total_days,
                'AI_Days': ai_days
            })

    return pd.DataFrame(summary)

# ============================================================================
# SIDEBAR
# ============================================================================
today = datetime.now()
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # View Mode Selector
    view_mode_display = st.radio(
        "📊 View Mode",
        options=["Hourly (Time of Day)", "Daily (Days of Week)"],
        index=0 if st.session_state.view_mode == 'hourly' else 1,
        horizontal=False
    )

    # Update view mode and trigger rerun if changed
    new_view_mode = 'hourly' if view_mode_display == "Hourly (Time of Day)" else 'daily'
    if new_view_mode != st.session_state.view_mode:
        st.session_state.view_mode = new_view_mode
        # Clear adjustments when switching views
        st.session_state.traffic_adjustments = {
            "London": {},
            "Copenhagen": {},
            "Paris": {}
        }
        st.rerun()

    st.markdown("---")

    # Scope Selector
    scope = st.selectbox(
        "📍 Scope Selector",
        ["All Stores (Aggregate)", "London", "Copenhagen", "Paris"]
    )

    # Date Picker
    selected_date = st.date_input("📅 Forecast Date", value=today)

# ============================================================================
# DATA GENERATION (needs to happen here before traffic adjustment tool uses it)
# ============================================================================
stores_data = generate_all_stores_data(selected_date, st.session_state.view_mode)

# Apply any manual traffic adjustments
stores_data = apply_traffic_adjustments(stores_data, st.session_state.traffic_adjustments, st.session_state.view_mode)

aggregate_data = calculate_aggregate_data(stores_data, st.session_state.view_mode)

# ============================================================================
# SIDEBAR CONTINUED
# ============================================================================
with st.sidebar:
    st.markdown("---")

    # Traffic Adjustment Tool (only for specific stores)
    st.markdown("### 🎯 Adjust Traffic Forecast")
    if scope != "All Stores (Aggregate)":
        st.caption("Fine-tune predictions based on your insights")

        # Time selector for adjustment (hourly or daily)
        if st.session_state.view_mode == 'hourly':
            time_options = [f"{h:02d}:00" for h in range(9, 21)]
            time_label = "Select Hour"
            time_col = 'Hour'
        else:
            time_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            time_label = "Select Day"
            time_col = 'Day'

        selected_time = st.selectbox(time_label, time_options, key="adj_time")

        # Get current value for this time period
        current_df = stores_data[scope]
        current_value = current_df[current_df[time_col] == selected_time]['Predicted_Traffic'].values[0]

        # Get current adjustment if exists
        current_adjustment = st.session_state.traffic_adjustments[scope].get(selected_time, 0)

        # Adjustment slider
        adjustment = st.slider(
            "Adjust Traffic (%)",
            min_value=-50,
            max_value=50,
            value=current_adjustment,
            step=5,
            help="Adjust predicted traffic up or down by percentage"
        )

        # Show preview
        adjusted_value = int(current_value * (1 + adjustment / 100))

        # Display as custom HTML with white background
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E8E8E8; border-radius: 8px; padding: 20px; margin: 12px 0; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);">
            <div style="display: flex; justify-content: space-around; gap: 20px;">
                <div style="text-align: center; flex: 1;">
                    <div style="color: #6B6B6B; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">Original</div>
                    <div style="color: #1A1A1A; font-size: 32px; font-weight: 700;">{int(current_value / (1 + current_adjustment / 100)):,}</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="color: #6B6B6B; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">Adjusted</div>
                    <div style="color: #1A1A1A; font-size: 32px; font-weight: 700;">{adjusted_value:,}</div>
                    <div style="color: {'#34C759' if adjustment > 0 else '#E74C3C' if adjustment < 0 else '#6B6B6B'}; font-size: 14px; font-weight: 600; margin-top: 4px;">{adjustment:+d}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Apply button
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✓ Apply", use_container_width=True):
                if adjustment != 0:
                    st.session_state.traffic_adjustments[scope][selected_time] = adjustment
                    st.success(f"✅ Applied to {selected_time}")
                    st.rerun()
                else:
                    # Remove adjustment if set to 0
                    if selected_time in st.session_state.traffic_adjustments[scope]:
                        del st.session_state.traffic_adjustments[scope][selected_time]
                    st.rerun()

        with col_b:
            if st.button("↺ Reset All", use_container_width=True):
                st.session_state.traffic_adjustments[scope] = {}
                st.success("✅ All adjustments cleared")
                st.rerun()

        # Show active adjustments
        if st.session_state.traffic_adjustments[scope]:
            st.caption(f"**Active Adjustments ({len(st.session_state.traffic_adjustments[scope])}):**")
            time_emoji = "🕐" if st.session_state.view_mode == 'hourly' else "📅"
            for time_period, adj in st.session_state.traffic_adjustments[scope].items():
                st.caption(f"{time_emoji} {time_period}: {adj:+d}%")
    else:
        st.info("🔒 Select a store to adjust forecasts")

    st.markdown("---")
    st.markdown("---")
    st.markdown("### 🤖 Model Info")
    st.caption("**Type:** XGBoost + LSTM")
    st.caption("**Accuracy:** 94.7%")
    st.caption("**Updated:** 4h ago")

    # Accuracy explanation
    with st.expander("ℹ️ What does accuracy mean?"):
        st.markdown("""
        **Model Accuracy: 94.7%**

        This represents how accurately the AI model predicts customer traffic compared to actual historical data.

        **Calculation:**
        - Measures predicted customer visits vs. actual customer visits
        - Based on 30 days of historical performance across all stores
        - Uses Mean Absolute Percentage Error (MAPE)
        - 94.7% means the model is typically within ±5.3% of actual traffic

        **What it includes:**
        - Foot traffic patterns (day of week, time of day)
        - Seasonal trends and holidays
        - Store-specific patterns (London peaks differ from Paris)
        - Weather impact (synthetic in this PoC)

        **Real-world context:**
        - 90%+ accuracy is considered excellent for retail forecasting
        - This model outperforms traditional flat-staffing approaches
        - Continuously improves as more data is collected
        """)

# ============================================================================
# MAIN HEADER
# ============================================================================
st.markdown(f"""
<div style="background: #FFFFFF;
            padding: 24px 28px; border-radius: 14px; margin-bottom: 20px;
            border: 1px solid #E8E8E8;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);">
    <h1 style="color: #1A1A1A; font-size: 26px; margin: 0; font-weight: 600;">
        💎 Pandora AI Traffic & Staffing Optimizer
    </h1>
    <p style="color: #6B6B6B; font-size: 13px; margin: 8px 0 0 0; font-weight: 500;">
        {scope} • {selected_date.strftime('%B %d, %Y')}
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# KPI ROW
# ============================================================================
traffic, revenue, efficiency = calculate_kpis(scope, stores_data, aggregate_data)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Predicted Traffic</div>
        <div class="kpi-value">{traffic:,}</div>
        <div class="kpi-subtitle">Customer Visits</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card kpi-card-with-tooltip">
        <span class="tooltip-text"><strong>Potential Sales Revenue</strong><br><br>Calculation: Total Visits × 20% Conversion Rate × $125 Avg Ticket Price<br><br>Of all predicted customer visits, approximately 20% convert into actual sales. With an average transaction value of $125 USD (931 kr), this represents the total potential sales revenue. Better staffing ensures we capture more of these conversion opportunities by reducing wait times and improving customer experience.</span>
        <div class="kpi-title">Revenue Recovery 💡</div>
        <div class="kpi-value">{revenue:,} kr</div>
        <div class="kpi-subtitle">Potential Sales</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card kpi-card-with-tooltip">
        <span class="tooltip-text"><strong>Staffing Efficiency</strong><br><br>Compares forecasted staffing needs (based on predicted traffic) versus realized staffing (what was actually implemented based on manager decisions).<br><br>Calculation: (Realized FTE / Forecasted FTE) × 100<br><br>100% = Perfect match between forecast and reality<br>&gt;100% = Overstaffing (used more staff than forecasted)<br>&lt;100% = Understaffing (used fewer staff than forecasted)<br><br>This metric helps identify if implementation decisions align with traffic predictions.</span>
        <div class="kpi-title">Staffing Efficiency</div>
        <div class="kpi-value">{efficiency}%</div>
        <div class="kpi-subtitle">Forecast vs Realized</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT GRID - 2 COLUMN LAYOUT
# ============================================================================

# Create 2-column layout for main content
col_left, col_right = st.columns([1.2, 1], gap="large")

# ============================================================================
# LEFT COLUMN: VISUALIZATION
# ============================================================================
with col_left:
    st.markdown("""
    <div style="background: #FFFFFF; padding: 12px 16px; border-radius: 8px; border-left: 3px solid #F2B8C6; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
        <div style="color: #1A1A1A; font-size: 13px; font-weight: 600; margin-bottom: 2px;">📈 Traffic & Staffing Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    if scope == "All Stores (Aggregate)":
        # STACKED AREA CHART
        fig = go.Figure()

        colors = {
            "London": "#F2B8C6",
            "Copenhagen": "#E5A0B1",
            "Paris": "#D88D9C"
        }

        # Determine time column and axis label
        time_col = 'Hour' if st.session_state.view_mode == 'hourly' else 'Day'
        x_axis_title = 'Hour of Day' if st.session_state.view_mode == 'hourly' else 'Day of Week'

        for store in ["London", "Copenhagen", "Paris"]:
            fig.add_trace(go.Scatter(
                x=aggregate_data[time_col],
                y=aggregate_data[store],
                name=store,
                mode='lines',
                stackgroup='one',
                fillcolor=colors[store],
                line=dict(width=0.5, color=colors[store])
            ))

        fig.update_layout(
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font=dict(family='Inter', color='#1A1A1A', size=13),
            xaxis=dict(
                title=dict(text=x_axis_title, font=dict(size=14, color='#1A1A1A', family='Inter')),
                showgrid=True,
                gridcolor='#F0F0F0',
                showline=True,
                linewidth=2,
                linecolor='#4A4A4A',
                tickfont=dict(size=12, color='#1A1A1A')
            ),
            yaxis=dict(
                title=dict(text='Customer Traffic', font=dict(size=14, color='#1A1A1A', family='Inter')),
                showgrid=True,
                gridcolor='#F0F0F0',
                showline=True,
                linewidth=2,
                linecolor='#4A4A4A',
                tickfont=dict(size=12, color='#1A1A1A')
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#D0D0D0',
                borderwidth=1,
                font=dict(size=12, color='#1A1A1A')
            ),
            hovermode='x unified',
            height=450,
            margin=dict(l=60, r=40, t=60, b=60)
        )

    else:
        # LINE CHART FOR SPECIFIC STORE
        df = stores_data[scope]

        # Determine time column and axis label
        time_col = 'Hour' if st.session_state.view_mode == 'hourly' else 'Day'
        x_axis_title = 'Hour of Day' if st.session_state.view_mode == 'hourly' else 'Day of Week'

        # Convert staffing to FTE (1 FTE per 50 visits)
        df['Baseline_FTE'] = df['Baseline_Staffing'] / 50
        df['AI_FTE'] = df['AI_Recommended_Staffing'] / 50

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Baseline Staffing as Grey Bars (Right Y-axis) - Add first (back layer)
        fig.add_trace(go.Bar(
            x=df[time_col],
            y=df['Baseline_FTE'],
            name='Baseline Staffing (Legacy)',
            marker=dict(color='#D0D0D0', opacity=0.6)
        ), secondary_y=True)

        # AI Recommended Staffing as Green Bars (Right Y-axis) - Add second
        fig.add_trace(go.Bar(
            x=df[time_col],
            y=df['AI_FTE'],
            name='AI Recommended Staffing',
            marker=dict(color='#34C759', opacity=0.8)
        ), secondary_y=True)

        # Actual Traffic (Left Y-axis) - Add third (show historical data up to today)
        # Filter to only show actual traffic where it exists (not None)
        actual_df = df[df['Actual_Traffic'].notna()].copy()
        if not actual_df.empty:
            fig.add_trace(go.Scatter(
                x=actual_df[time_col],
                y=actual_df['Actual_Traffic'],
                name='Actual Traffic',
                mode='lines+markers',
                line=dict(color='#2C2C2C', width=2, dash='solid'),
                marker=dict(size=7, color='#2C2C2C', symbol='circle')
            ), secondary_y=False)

        # Highlight manually adjusted points - Add fourth
        if st.session_state.traffic_adjustments[scope]:
            adjusted_times = []
            adjusted_values = []

            for time_value, adjustment in st.session_state.traffic_adjustments[scope].items():
                adjusted_times.append(time_value)
                adjusted_values.append(df[df[time_col] == time_value]['Predicted_Traffic'].values[0])

            fig.add_trace(go.Scatter(
                x=adjusted_times,
                y=adjusted_values,
                name='Manual Adjustments',
                mode='markers',
                marker=dict(
                    size=12,
                    color='#FF9500',
                    symbol='star',
                    line=dict(color='#2C2C2C', width=2)
                ),
                showlegend=True
            ), secondary_y=False)

        # Predicted Traffic (Left Y-axis) - Add LAST (front layer)
        fig.add_trace(go.Scatter(
            x=df[time_col],
            y=df['Predicted_Traffic'],
            name='Predicted Traffic',
            mode='lines+markers',
            line=dict(color='#F2B8C6', width=3),
            marker=dict(size=8, color='#F2B8C6', line=dict(color='#FFFFFF', width=1))
        ), secondary_y=False)

        # Set axis titles and layer to render axes below traces
        fig.update_xaxes(
            title_text=x_axis_title,
            title_font=dict(size=14, color='#1A1A1A', family='Inter'),
            showgrid=True,
            gridcolor='#F0F0F0',
            showline=True,
            linewidth=2,
            linecolor='#4A4A4A',
            tickfont=dict(size=12, color='#1A1A1A'),
            layer='below traces'
        )

        fig.update_yaxes(
            title_text='Customer Traffic',
            title_font=dict(size=14, color='#1A1A1A', family='Inter'),
            showgrid=True,
            gridcolor='#F0F0F0',
            showline=True,
            linewidth=2,
            linecolor='#4A4A4A',
            tickfont=dict(size=12, color='#1A1A1A'),
            layer='below traces',
            secondary_y=False
        )

        fig.update_yaxes(
            title_text='Staffing (FTE)',
            title_font=dict(size=14, color='#1A1A1A', family='Inter'),
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='#4A4A4A',
            tickfont=dict(size=12, color='#1A1A1A'),
            layer='below traces',
            secondary_y=True
        )

        fig.update_layout(
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font=dict(family='Inter', color='#1A1A1A', size=13),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#D0D0D0',
                borderwidth=1,
                font=dict(size=12, color='#1A1A1A')
            ),
            barmode='group',
            hovermode='x unified',
            height=450,
            margin=dict(l=60, r=80, t=60, b=60)
        )

    st.plotly_chart(fig, width='stretch')

    # Info messages for individual stores
    if scope != "All Stores (Aggregate)":
        # Show info about actual vs predicted traffic
        df = stores_data[scope]
        has_actual = df['Actual_Traffic'].notna().any()
        if has_actual:
            st.info("📊 **Actual Traffic** (dark line) shows real customer visits up to today. Compare with **Predicted Traffic** (pink line) to assess forecast accuracy.")

        # Show info about manual adjustments
        if st.session_state.traffic_adjustments[scope]:
            st.info(f"⭐ **{len(st.session_state.traffic_adjustments[scope])} manual adjustment(s) applied** — Orange stars indicate adjusted predictions. AI staffing recommendations have been recalculated automatically.")

    # ============================================================================
    # IMPLEMENTATION TRACKING SECTION (moved to left column below chart)
    # ============================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #FFFFFF; padding: 12px 16px; border-radius: 8px; border-left: 3px solid #F2B8C6; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
        <div style="color: #1A1A1A; font-size: 13px; font-weight: 600; margin-bottom: 2px;">🎯 AI Recommendation Adoption</div>
    </div>
    """, unsafe_allow_html=True)

    # Generate and display implementation tracking visualizations
    if scope != "All Stores (Aggregate)":
        # STORE-SPECIFIC: Show 30-day calendar for this store
        df_calendar = generate_implementation_calendar(scope)

        # Create calendar heatmap
        fig_calendar = go.Figure()

        # Group by week and day of week
        weeks = sorted(df_calendar['Week'].unique())
        days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        # Prepare data for heatmap
        heatmap_data = []
        for week in weeks:
            week_data = []
            for day in days_order:
                mask = (df_calendar['Week'] == week) & (df_calendar['Day'] == day)
                if mask.any():
                    decision = df_calendar[mask]['Decision'].values[0]
                    # 1 = AI (green), 0 = Legacy (grey), None = No decision (white)
                    if decision == 1:
                        week_data.append(100)  # AI recommendation
                    elif decision == 0:
                        week_data.append(50)   # Legacy system
                    else:
                        week_data.append(0)    # No decision yet
                else:
                    week_data.append(0)
            heatmap_data.append(week_data)

        # Transpose for correct orientation
        heatmap_data = list(map(list, zip(*heatmap_data)))

        # Custom hover text
        hover_text = []
        for day_idx, day in enumerate(days_order):
            day_hover = []
            for week in weeks:
                mask = (df_calendar['Week'] == week) & (df_calendar['Day'] == day)
                if mask.any():
                    row = df_calendar[mask].iloc[0]
                    date_str = row['Date'].strftime('%b %d')
                    if row['Decision'] == 1:
                        day_hover.append(f"{date_str}<br>✓ Following AI")
                    elif row['Decision'] == 0:
                        day_hover.append(f"{date_str}<br>⊗ Using Legacy")
                    else:
                        day_hover.append(f"{date_str}<br>No decision")
                else:
                    day_hover.append("")
            hover_text.append(day_hover)

        fig_calendar.add_trace(go.Heatmap(
            z=heatmap_data,
            x=[f'Week {w+1}' for w in weeks],
            y=days_order,
            colorscale=[
                [0, '#F5F5F5'],      # Light grey (no decision)
                [0.5, '#D0D0D0'],    # Grey (legacy system)
                [1, '#34C759']       # Green (AI recommendation)
            ],
            text=hover_text,
            hovertemplate='%{text}<extra></extra>',
            showscale=True,
            colorbar=dict(
                title="Decision",
                tickvals=[25, 75],
                ticktext=["Legacy", "AI"],
                thickness=15,
                len=0.7
            ),
            zmin=0,
            zmax=100
        ))

        fig_calendar.update_layout(
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font=dict(family='Inter', color='#1A1A1A', size=12),
            xaxis=dict(
                title='',
                showgrid=False,
                side='top',
                tickfont=dict(size=12, color='#1A1A1A')
            ),
            yaxis=dict(
                title='',
                showgrid=False,
                tickfont=dict(size=12, color='#1A1A1A')
            ),
            height=280,
            margin=dict(l=60, r=40, t=60, b=30)
        )

        st.plotly_chart(fig_calendar, width='stretch')

        # Get AI recommendation for display
        if scope in stores_data:
            df_store = stores_data[scope]
            ai_fte_avg = (df_store['AI_Recommended_Staffing'] / 50).mean()
            baseline_fte_avg = (df_store['Baseline_Staffing'] / 50).mean()
        else:
            ai_fte_avg = 0
            baseline_fte_avg = 0

        # Implementation decision buttons
        st.markdown(f"""
        <div style="background: #F0F9FF; padding: 12px; border-radius: 8px; margin: 12px 0; border-left: 3px solid #34C759;">
            <div style="color: #1A1A1A; font-size: 12px; font-weight: 600; margin-bottom: 4px;">Today's Staffing Decision for {scope}</div>
            <div style="color: #4A4A4A; font-size: 11px;">AI Recommendation: <strong>{ai_fte_avg:.1f} FTE/Day</strong> | Legacy System: <strong>{baseline_fte_avg:.1f} FTE/Day</strong></div>
        </div>
        """, unsafe_allow_html=True)

        col_fb1, col_fb2 = st.columns(2)

        with col_fb1:
            if st.button("✓ Following AI", use_container_width=True, key=f"ai_{scope}", type="primary"):
                # Store implementation decision
                today_str = datetime.now().strftime('%Y-%m-%d')
                if scope not in st.session_state.implementation_history:
                    st.session_state.implementation_history[scope] = {}
                st.session_state.implementation_history[scope][today_str] = {'decision': 1}
                st.success("✅ Confirmed: Following AI recommendation")
                st.rerun()

        with col_fb2:
            if st.button("⊗ Using Legacy", use_container_width=True, key=f"legacy_{scope}"):
                # Store implementation decision
                today_str = datetime.now().strftime('%Y-%m-%d')
                if scope not in st.session_state.implementation_history:
                    st.session_state.implementation_history[scope] = {}
                st.session_state.implementation_history[scope][today_str] = {'decision': 0}
                st.success("✅ Confirmed: Using legacy system")
                st.rerun()

        # Show today's decision
        today_str = datetime.now().strftime('%Y-%m-%d')
        if scope in st.session_state.implementation_history and today_str in st.session_state.implementation_history[scope]:
            decision = st.session_state.implementation_history[scope][today_str]['decision']
            if decision == 1:
                st.info("🎯 **Today's Decision**: Following AI Recommendation")
            else:
                st.info("📋 **Today's Decision**: Using Legacy System")

    else:
        # REGIONAL MANAGER VIEW: Show AI adoption comparison across all stores
        df_summary = get_store_adoption_summary()

        # Create bar chart comparing stores
        fig_comparison = go.Figure()

        colors_map = {
            "London": "#F2B8C6",
            "Copenhagen": "#E5A0B1",
            "Paris": "#D88D9C"
        }

        fig_comparison.add_trace(go.Bar(
            x=df_summary['Store'],
            y=df_summary['Adoption_Rate'],
            marker=dict(
                color=[colors_map[store] for store in df_summary['Store']],
                line=dict(color='#2C2C2C', width=1)
            ),
            text=[f"{rate:.1f}%" for rate in df_summary['Adoption_Rate']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>AI Adoption: %{y:.1f}%<br>Days Tracked: %{customdata}<extra></extra>',
            customdata=df_summary['Total_Days']
        ))

        # Add threshold line at 80% (target adoption)
        fig_comparison.add_hline(
            y=80,
            line_dash="dash",
            line_color="#34C759",
            annotation_text="Target (80%)",
            annotation_position="right"
        )


        fig_comparison.update_layout(
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font=dict(family='Inter', color='#1A1A1A', size=12),
            xaxis=dict(
                title='',
                showgrid=False,
                showline=True,
                linewidth=2,
                linecolor='#4A4A4A',
                tickfont=dict(size=12, color='#1A1A1A')
            ),
            yaxis=dict(
                title=dict(text='AI Adoption Rate (%)', font=dict(size=14, color='#1A1A1A', family='Inter')),
                showgrid=True,
                gridcolor='#F0F0F0',
                range=[0, 100],
                showline=True,
                linewidth=2,
                linecolor='#4A4A4A',
                tickfont=dict(size=12, color='#1A1A1A')
            ),
            height=450,
            margin=dict(l=60, r=100, t=60, b=60)
        )

        st.plotly_chart(fig_comparison, width='stretch')

        # Regional summary
        col_r1, col_r2, col_r3 = st.columns(3)
        avg_adoption = df_summary['Adoption_Rate'].mean()
        best_store = df_summary.loc[df_summary['Adoption_Rate'].idxmax(), 'Store']
        # Use 80% threshold to match the target line on the chart
        low_adoption = df_summary[df_summary['Adoption_Rate'] < 80]

        with col_r1:
            st.metric("Regional Avg", f"{avg_adoption:.1f}%", delta="AI Adoption")
        with col_r2:
            st.metric("Top Adopter", best_store)
        with col_r3:
            if len(low_adoption) > 0:
                stores_list = ", ".join(low_adoption['Store'].tolist())
                st.metric("Needs Support", len(low_adoption), delta=stores_list, delta_color="off")
            else:
                st.metric("Needs Support", "None ✓")

# ============================================================================
# RIGHT COLUMN: STAFFING RECOMMENDATION
# ============================================================================
with col_right:
    st.markdown("""
    <div style="background: #FFFFFF; padding: 12px 16px; border-radius: 8px; border-left: 3px solid #F2B8C6; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
        <div style="color: #1A1A1A; font-size: 13px; font-weight: 600; margin-bottom: 2px;">🎯 Staffing Recommendation</div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================================
    # STAFFING RECOMMENDATION & REVENUE IMPACT (all views)
    # ============================================================================
    if scope != "All Stores (Aggregate)":
        # Individual store
        df = stores_data[scope].copy()

        # Calculate FTE from adjusted staffing values (1 FTE per 50 customer visits)
        df['Baseline_FTE'] = df['Baseline_Staffing'] / 50
        df['AI_FTE'] = df['AI_Recommended_Staffing'] / 50

        # Calculate averages for the current view period
        # For hourly: average FTE across the operating day
        # For daily: average FTE per day across the week
        baseline_fte = df['Baseline_FTE'].mean()
        ai_fte = df['AI_FTE'].mean()
        total_traffic = df['Predicted_Traffic'].sum()
    else:
        # Aggregate across all stores
        baseline_fte_sum = 0
        ai_fte_sum = 0
        total_traffic = 0

        for store_name, df in stores_data.items():
            df = df.copy()
            df['Baseline_FTE'] = df['Baseline_Staffing'] / 50
            df['AI_FTE'] = df['AI_Recommended_Staffing'] / 50

            baseline_fte_sum += df['Baseline_FTE'].mean()
            ai_fte_sum += df['AI_FTE'].mean()
            total_traffic += df['Predicted_Traffic'].sum()

        baseline_fte = baseline_fte_sum
        ai_fte = ai_fte_sum

    # Calculate difference (runs for both individual and aggregate)
    fte_difference = baseline_fte - ai_fte

    # Revenue impact calculation (per day or per week based on view)
    # The AI system optimally staffs to match traffic patterns, improving service quality
    # Better staffing during peaks = better customer experience = higher conversion rates
    conversion_rate = 0.20  # 20% baseline conversion
    avg_ticket_dkk = 931.25  # $125 × 7.45 DKK/USD

    # Calculate potential revenue from optimal staffing
    # Optimal staffing improves conversion by ~5-8% through reduced wait times and better service
    conversion_improvement = 0.05  # 5% improvement in conversion rate
    revenue_impact = int(total_traffic * conversion_improvement * conversion_rate * avg_ticket_dkk)

    # For hourly view, this is per day. For daily view, this is per week
    if st.session_state.view_mode == 'hourly':
        revenue_per_day = revenue_impact
        revenue_weekly = None
    else:
        revenue_weekly = revenue_impact
        revenue_per_day = revenue_impact // 7

    # Create a styled recommendation box
    if fte_difference > 0:
        # Legacy system is overstaffed - but still show revenue opportunity from better allocation
        recommendation_color = "#E8F5E9"  # Light green
        recommendation_text = f"The AI system recommends an average of <strong>{ai_fte:.1f} FTE per day</strong> compared to the legacy system's <strong>{baseline_fte:.1f} FTE per day</strong> (a reduction of {abs(fte_difference):.1f} FTE). The legacy system maintains flat staffing levels, while AI dynamically allocates staff to peak periods."
        if st.session_state.view_mode == 'hourly':
            impact_text = f"By reallocating staff to match traffic patterns (more staff during peaks, fewer during slow periods), you can <strong>capture an estimated {revenue_per_day:,} kr per day</strong> in additional revenue through improved customer service during high-traffic hours."
        else:
            impact_text = f"By reallocating staff to match traffic patterns (more staff during peaks, fewer during slow periods), you can <strong>capture an estimated {revenue_per_day:,} kr per day</strong> ({revenue_weekly:,} kr per week) in additional revenue through improved customer service during high-traffic hours."
    elif fte_difference < 0:
        # Legacy system is understaffed
        recommendation_color = "#FFF3E0"  # Light orange
        recommendation_text = f"The AI system recommends an average of <strong>{ai_fte:.1f} FTE per day</strong> compared to the legacy system's <strong>{baseline_fte:.1f} FTE per day</strong> (an increase of {abs(fte_difference):.1f} FTE). The legacy system under-allocates staff during peak traffic periods, leading to missed sales opportunities."
        if st.session_state.view_mode == 'hourly':
            impact_text = f"By adding staff during high-traffic periods, you can <strong>capture an estimated {revenue_per_day:,} kr per day</strong> in additional revenue from improved customer service and reduced wait times."
        else:
            impact_text = f"By adding staff during high-traffic periods, you can <strong>capture an estimated {revenue_per_day:,} kr per day</strong> ({revenue_weekly:,} kr per week) in additional revenue from improved customer service and reduced wait times."
    else:
        # Equal staffing
        recommendation_color = "#E3F2FD"  # Light blue
        recommendation_text = f"The AI system's average staffing recommendation ({ai_fte:.1f} FTE per day) closely matches the legacy system."
        if st.session_state.view_mode == 'hourly':
            impact_text = f"However, the AI system dynamically adjusts staffing to match traffic patterns throughout the day. This optimal allocation can still <strong>generate an estimated {revenue_per_day:,} kr per day</strong> through better peak coverage and improved customer experience."
        else:
            impact_text = f"However, the AI system dynamically adjusts staffing to match traffic patterns throughout the week. This optimal allocation can still <strong>generate an estimated {revenue_per_day:,} kr per day</strong> ({revenue_weekly:,} kr per week) through better peak coverage and improved customer experience."

    st.markdown(f"""
        <div style="background: {recommendation_color}; border-radius: 12px; padding: 24px; margin-bottom: 20px; border-left: 4px solid #F2B8C6;">
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px;">
                <div style="text-align: center;">
                    <div style="color: #6B6B6B; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Legacy System</div>
                    <div style="color: #1A1A1A; font-size: 32px; font-weight: 700;">{baseline_fte:.1f}</div>
                    <div style="color: #999999; font-size: 12px; margin-top: 4px;">Avg FTE/Day</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #6B6B6B; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">AI Recommended</div>
                    <div style="color: #34C759; font-size: 32px; font-weight: 700;">{ai_fte:.1f}</div>
                    <div style="color: #999999; font-size: 12px; margin-top: 4px;">Avg FTE/Day</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #6B6B6B; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Difference</div>
                    <div style="color: {'#E74C3C' if fte_difference > 0 else '#34C759' if fte_difference < 0 else '#6B6B6B'}; font-size: 32px; font-weight: 700;">{fte_difference:+.1f}</div>
                    <div style="color: #999999; font-size: 12px; margin-top: 4px;">FTE/Day</div>
                </div>
            </div>
            <div style="padding: 16px; background: #FFFFFF; border-radius: 8px; margin-bottom: 12px;">
                <div style="color: #1A1A1A; font-size: 14px; font-weight: 600; margin-bottom: 8px;">📊 Analysis</div>
                <div style="color: #4A4A4A; font-size: 13px; line-height: 1.6;">{recommendation_text}</div>
            </div>
            <div style="padding: 16px; background: #FFFFFF; border-radius: 8px;">
                <div style="color: #1A1A1A; font-size: 14px; font-weight: 600; margin-bottom: 8px;">💰 Revenue Impact</div>
                <div style="color: #4A4A4A; font-size: 13px; line-height: 1.6;">{impact_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Add explanation note
    if st.session_state.view_mode == 'hourly':
        st.caption("Note: Average FTE/Day shows the average number of full-time employees needed during the operating day (9:00-21:00). Revenue impact calculated from 5% conversion improvement due to optimal staffing (20% baseline conversion × 931 kr average ticket).")
    else:
        st.caption("Note: Average FTE/Day shows the average number of full-time employees needed per day, averaged across the 7-day week. Revenue impact calculated from 5% conversion improvement due to optimal staffing (20% baseline conversion × 931 kr average ticket).")

    # ============================================================================
    # KPI OVERVIEW CARDS - COMPACT VERSION
    # ============================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #FFFFFF; padding: 12px 16px; border-radius: 8px; border-left: 3px solid #F2B8C6; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
        <div style="color: #1A1A1A; font-size: 13px; font-weight: 600; margin-bottom: 2px;">📊 Performance Metrics</div>
    </div>
    """, unsafe_allow_html=True)

    # Generate mock performance data (in production, this would come from real metrics)
    np.random.seed(42)

    # Calculate actual AI adoption rates from implementation history
    if scope != "All Stores (Aggregate)":
        # Individual store adoption
        store_history = st.session_state.implementation_history.get(scope, {})
        today_str = datetime.now().strftime('%Y-%m-%d')

        # Check if following AI today
        adoption_today = 100 if store_history.get(today_str, {}).get('decision') == 1 else 0

        # Last 3 days
        days_3 = [store_history.get((datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'), {}).get('decision', 0) for i in range(3)]
        adoption_3days = (sum([1 for d in days_3 if d == 1]) / len([d for d in days_3 if d is not None]) * 100) if any(d is not None for d in days_3) else 0

        # Last week
        days_7 = [store_history.get((datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'), {}).get('decision', 0) for i in range(7)]
        adoption_week = (sum([1 for d in days_7 if d == 1]) / len([d for d in days_7 if d is not None]) * 100) if any(d is not None for d in days_7) else 0
    else:
        # Aggregate adoption across all stores
        adoption_today = 85.0
        adoption_3days = 81.7
        adoption_week = 83.3

    # Data Completeness and Freshness
    data_today = 100.0
    data_3days = 99.8
    data_week = 99.4

    # Forecast Accuracy (Actual vs Predicted)
    accuracy_today, accuracy_3days, accuracy_week = calculate_forecast_accuracy(
        scope, stores_data, aggregate_data, selected_date
    )

    # Card 1: AI Adoption Rate (Compact)
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E8E8E8; border-radius: 8px; padding: 12px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
        <div style="color: #1A1A1A; font-size: 12px; font-weight: 600; margin-bottom: 8px;">🎯 AI Adoption Rate</div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 8px;">
            <div style="text-align: center; padding: 8px; background: #FAFAFA; border-radius: 6px;">
                <div style="color: #6B6B6B; font-size: 9px; font-weight: 600; text-transform: uppercase; margin-bottom: 3px;">Today</div>
                <div style="color: #34C759; font-size: 18px; font-weight: 700; line-height: 1;">{adoption_today:.0f}%</div>
            </div>
            <div style="text-align: center; padding: 8px; background: #FAFAFA; border-radius: 6px;">
                <div style="color: #6B6B6B; font-size: 9px; font-weight: 600; text-transform: uppercase; margin-bottom: 3px;">3 Days</div>
                <div style="color: #34C759; font-size: 18px; font-weight: 700; line-height: 1;">{adoption_3days:.0f}%</div>
            </div>
            <div style="text-align: center; padding: 8px; background: #FAFAFA; border-radius: 6px;">
                <div style="color: #6B6B6B; font-size: 9px; font-weight: 600; text-transform: uppercase; margin-bottom: 3px;">Week</div>
                <div style="color: #34C759; font-size: 18px; font-weight: 700; line-height: 1;">{adoption_week:.0f}%</div>
            </div>
        </div>
        <div style="padding: 6px 8px; background: #F0F9FF; border-radius: 4px; border-left: 2px solid #34C759;">
            <div style="color: #4A4A4A; font-size: 9px; line-height: 1.4;">
                % of days following AI recommendations
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Card 2: Data Quality (Compact)
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E8E8E8; border-radius: 8px; padding: 12px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
        <div style="color: #1A1A1A; font-size: 12px; font-weight: 600; margin-bottom: 8px;">📡 Data Quality</div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 8px;">
            <div style="text-align: center; padding: 8px; background: #FAFAFA; border-radius: 6px;">
                <div style="color: #6B6B6B; font-size: 9px; font-weight: 600; text-transform: uppercase; margin-bottom: 3px;">Today</div>
                <div style="color: #2ECC71; font-size: 18px; font-weight: 700; line-height: 1;">{data_today:.1f}%</div>
            </div>
            <div style="text-align: center; padding: 8px; background: #FAFAFA; border-radius: 6px;">
                <div style="color: #6B6B6B; font-size: 9px; font-weight: 600; text-transform: uppercase; margin-bottom: 3px;">3 Days</div>
                <div style="color: #2ECC71; font-size: 18px; font-weight: 700; line-height: 1;">{data_3days:.1f}%</div>
            </div>
            <div style="text-align: center; padding: 8px; background: #FAFAFA; border-radius: 6px;">
                <div style="color: #6B6B6B; font-size: 9px; font-weight: 600; text-transform: uppercase; margin-bottom: 3px;">Week</div>
                <div style="color: #2ECC71; font-size: 18px; font-weight: 700; line-height: 1;">{data_week:.1f}%</div>
            </div>
        </div>
        <div style="padding: 6px 8px; background: #F0FFF4; border-radius: 4px; border-left: 2px solid #2ECC71;">
            <div style="color: #4A4A4A; font-size: 9px; line-height: 1.4;">
                Completeness & freshness of data feeds
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Card 3: Forecast Accuracy (Compact)
    # Format accuracy values - show "N/A" for future dates
    today_display = "N/A" if accuracy_today == 0.0 else f"{accuracy_today:.1f}%"
    days3_display = "N/A" if accuracy_3days == 0.0 else f"{accuracy_3days:.1f}%"
    week_display = "N/A" if accuracy_week == 0.0 else f"{accuracy_week:.1f}%"

    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E8E8E8; border-radius: 8px; padding: 12px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
        <div style="color: #1A1A1A; font-size: 12px; font-weight: 600; margin-bottom: 8px;">🎯 Forecast Accuracy</div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 8px;">
            <div style="text-align: center; padding: 8px; background: #FAFAFA; border-radius: 6px;">
                <div style="color: #6B6B6B; font-size: 9px; font-weight: 600; text-transform: uppercase; margin-bottom: 3px;">Today</div>
                <div style="color: #34C759; font-size: 18px; font-weight: 700; line-height: 1;">{today_display}</div>
            </div>
            <div style="text-align: center; padding: 8px; background: #FAFAFA; border-radius: 6px;">
                <div style="color: #6B6B6B; font-size: 9px; font-weight: 600; text-transform: uppercase; margin-bottom: 3px;">3 Days</div>
                <div style="color: #34C759; font-size: 18px; font-weight: 700; line-height: 1;">{days3_display}</div>
            </div>
            <div style="text-align: center; padding: 8px; background: #FAFAFA; border-radius: 6px;">
                <div style="color: #6B6B6B; font-size: 9px; font-weight: 600; text-transform: uppercase; margin-bottom: 3px;">Week</div>
                <div style="color: #34C759; font-size: 18px; font-weight: 700; line-height: 1;">{week_display}</div>
            </div>
        </div>
        <div style="padding: 6px 8px; background: #F0FFF4; border-radius: 4px; border-left: 2px solid #34C759;">
            <div style="color: #4A4A4A; font-size: 9px; line-height: 1.4;">
                Predicted vs Realized traffic accuracy
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# SYSTEM HEALTH SECTION
# ============================================================================
st.markdown("""
<div style="background: #FFFFFF; padding: 12px 16px; border-radius: 8px; border-left: 3px solid #F2B8C6; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);">
    <div style="color: #1A1A1A; font-size: 13px; font-weight: 600; margin-bottom: 2px;">🔧 System Health Monitor</div>
</div>
""", unsafe_allow_html=True)
col_h1, col_h2, col_h3 = st.columns(3)

with col_h1:
    st.markdown("""
    <div class="status-badge">
        <div class="status-title">Data Feeds</div>
        <div class="status-value">✅ Active</div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("""
    <div class="status-badge">
        <div class="status-title">Model Drift</div>
        <div class="status-value">📊 Monitoring Active</div>
    </div>
    """, unsafe_allow_html=True)

with col_h3:
    st.markdown("""
    <div class="status-badge">
        <div class="status-title">Data Quality</div>
        <div class="status-value">✓ 99.4%</div>
    </div>
    """, unsafe_allow_html=True)
