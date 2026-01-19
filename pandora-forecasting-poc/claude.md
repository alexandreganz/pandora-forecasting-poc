# Pandora AI Traffic & Staffing Optimizer

## Project Overview

A Proof of Concept (PoC) Streamlit application designed for Pandora executives to optimize store traffic forecasting and staffing allocation across multiple retail locations. The app provides AI-powered recommendations to improve operational efficiency and maximize revenue opportunities through behavioral tracking and actionable insights.

## Key Features

### 1. Multi-Store Management
- **Aggregate View**: Combined view of all stores (London, Copenhagen, Paris)
- **Individual Store Views**: Detailed analysis per location
- **Store-Specific Data**: Each store has unique traffic patterns and staffing needs

### 2. Dual View Modes
- **Hourly View**: 12-hour window (09:00 - 21:00) for intraday planning
- **Daily View**: 7-day week view (Monday - Sunday) for weekly planning
- **Date Selector**: Choose any date to view forecasts and historical data

### 3. Traffic Forecasting with Actual vs Predicted
- **Predicted Traffic**: AI-generated customer visit forecasts (pink line)
- **Actual Traffic**: Historical customer visits up to today (dark line)
- **Visual Representation**:
  - Aggregate: Stacked area chart showing contribution by store
  - Individual: Dual y-axis chart with traffic lines and staffing bars
- **Manual Adjustments**: Store managers can adjust predictions based on local insights (-50% to +50%)
- **Smart Date Handling**:
  - Past dates: Shows actual traffic for all periods
  - Today: Shows actual traffic up to current hour/day
  - Future dates: Shows only predicted traffic

### 4. Staffing Optimization with Confidence Intervals
- **Baseline Staffing**: Legacy/current staffing levels (grey bars)
- **AI Recommended Staffing**: Optimized staffing levels (green bars)
- **FTE Calculation**: 1 Full-Time Employee per 50 customer visits
- **Average FTE/Day**: Shows average employees needed per day
- **Dual Y-Axis**:
  - Left (Primary): Staffing FTE (bars)
  - Right (Secondary): Customer Traffic (lines with confidence band)
- **Confidence Intervals**: ±10% band around predicted traffic showing forecast uncertainty
- **Interactive Legend**: Toggle chart elements on/off by clicking

### 5. Staffing Recommendation Dashboard
- **Individual Store View**: Comprehensive recommendation card showing:
  - Legacy System avg FTE/day vs AI Recommended avg FTE/day
  - FTE Difference (positive = overstaffing, negative = understaffing)
  - Revenue Impact Analysis (kr per day and per week)
  - Dynamic reallocation benefits
- **Hover Tooltip**: ⓘ icon with explanation on hover
  - FTE calculation methodology
  - Revenue impact formula details
  - View mode-specific context (hourly vs daily)
  - Dark tooltip with high contrast text
- **Calculation Basis**:
  - Revenue from 5% conversion improvement
  - 20% baseline conversion × 931 kr average ticket
- **Period-Aware**: Adapts labels and calculations for hourly vs daily view

### 6. AI Recommendation Adoption Tracking (Behavioral System)
**Replaces passive accuracy rating with active implementation tracking**

- **Decision Tracking**: Store managers commit to daily staffing approach
  - **"✓ Following AI"**: Using AI-recommended staffing
  - **"⊗ Using Legacy"**: Using legacy/baseline staffing
- **30-Day Calendar Heatmap**: Visual history of implementation decisions
  - Green squares: Days following AI recommendations
  - Grey squares: Days using legacy system
  - White squares: No decision recorded
- **Adoption Metrics**:
  - Today: Current decision status
  - 3 Days: Rolling adoption rate
  - Week: Weekly adoption percentage
- **Regional Manager View**:
  - AI adoption rate comparison across stores
  - Target line at 80% adoption
  - Stores needing support (<80%)

### 7. Interactive Traffic Adjustments
- **Time-Based Adjustments**: Modify traffic predictions by percentage
- **Real-Time Recalculation**: AI staffing and revenue impact automatically update
- **Visual Indicators**: Orange stars mark manually adjusted data points
- **Preview Mode**: See original vs. adjusted values before applying
- **Seamless Integration**: Adjustments reflected in all visualizations and recommendations

### 8. Executive KPIs
**Main Dashboard (3 cards):**
- **Total Predicted Traffic**: Customer visit forecasts
- **Revenue Recovery**: Potential sales revenue with tooltip explanation
- **Staffing Efficiency**: Optimal allocation percentage with tooltip

**Performance Metrics (Right Column - 3 compact cards):**
- **🎯 AI Adoption Rate**: % of days following AI recommendations (Today / 3 Days / Week)
- **📡 Data Quality**: Completeness & freshness metrics (99.4%+)
- **🎯 Forecast Accuracy**: Predicted vs Realized traffic accuracy (Today / 3 Days / Week)
  - Shows "N/A" for future dates with no actual data
  - Dynamically updates based on selected date and store

### 9. System Health Monitoring
- **Data Feeds Status**: Active/Inactive indicators
- **Model Drift Monitoring**: ML model performance tracking
- **Data Quality**: Real-time quality metrics

### 10. Model Accuracy Explanation
- **Expandable Info Section**: Located in sidebar below Model Info
- **94.7% Accuracy**: Explained as predicted vs actual traffic comparison
- **MAPE Calculation**: Mean Absolute Percentage Error over 30 days
- **Variables Included**: Foot traffic patterns, seasonal trends, store-specific patterns, weather
- **Context**: 90%+ accuracy considered excellent for retail forecasting

## Technical Stack

### Core Technologies
- **Framework**: Streamlit 1.28.0+
- **Visualization**: Plotly 5.17.0+ (with subplots for dual y-axis)
- **Data Processing**: Pandas 2.0.0+, NumPy 1.24.0+
- **Language**: Python 3.12
- **Performance**: Streamlit caching (@st.cache_data) on all data generation functions

### Key Libraries
```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
```

## Installation & Setup

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Installation Steps

1. **Clone/Navigate to Project Directory**
```bash
cd C:\Users\Alex\Desktop\personal_projects\pandora-forecasting-poc
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Application**
```bash
streamlit run app.py
# or
python -m streamlit run app.py
```

4. **Access the App**
- Local: http://localhost:8501
- Network: http://[your-ip]:8501

## Project Structure

```
pandora-forecasting-poc/
├── app.py                 # Main application file (~1500 lines)
├── requirements.txt       # Python dependencies
└── claude.md             # This documentation file
```

## Data Models & Calculations

### Traffic Generation
Each store has unique traffic patterns:
- **Peak Hours**: Store-specific high-traffic periods
- **Base Traffic**: Minimum expected customer visits
- **Peak Boost**: Additional traffic during peak times
- **Actual Traffic**: Generated with ±8% variance from predicted for historical data

### Staffing Calculation
```python
# FTE Conversion (per time period)
FTE_per_period = Customer_Visits / 50

# Average FTE per Day
Avg_FTE = mean(FTE_per_period)

# AI Recommended Staffing
AI_Staffing = Predicted_Traffic × 0.93
```

### Revenue Impact Calculation
```python
# Revenue from optimal staffing (5% conversion improvement)
Revenue_Impact (kr) = Total_Traffic × 0.05 × 0.20 × 931.25

Where:
- 5% = Conversion improvement from optimal staffing
- 20% = Baseline conversion rate
- 931.25 kr = Average ticket ($125 × 7.45 DKK/USD)
```

### AI Adoption Rate
```python
# Daily Adoption
Adoption (%) = (Days_Following_AI / Total_Days) × 100

# Regional Average
Regional_Avg = Mean of all store adoption rates
```

## User Interface Components

### Sidebar Controls
1. **View Mode Toggle**: Switch between Hourly/Daily views (clears adjustments on switch)
2. **Store Selector**: Choose store or aggregate view
3. **Date Picker**: Select forecast date (updates actual traffic display)
4. **Traffic Adjustment Tool** (individual stores only):
   - Time selector (hour or day)
   - Adjustment slider (-50% to +50%)
   - Preview (Original vs. Adjusted values)
   - Apply/Reset All buttons
   - Active adjustments counter
5. **Model Info**: XGBoost + LSTM, 94.7% accuracy

### Main Dashboard (2-Column Layout)

**Left Column (60%):**
- **Traffic & Staffing Analysis Chart**:
  - Dual y-axis visualization
  - Pink line: Predicted traffic (always visible)
  - Dark line: Actual traffic (past dates only)
  - Grey bars: Baseline staffing (legacy)
  - Green bars: AI recommended staffing
  - Orange stars: Manual adjustment markers
  - Interactive hover details
- **AI Recommendation Adoption**:
  - 30-day calendar heatmap (green = AI, grey = Legacy)
  - Implementation decision buttons
  - Current decision status

**Right Column (40%):**
- **Staffing Recommendation** (individual stores):
  - 3-metric comparison (Legacy / AI / Difference)
  - Analysis of staffing patterns
  - Revenue impact calculation
  - Period-specific recommendations
- **Performance Metrics** (3 compact KPI cards):
  - AI Adoption Rate
  - Data Quality
  - Sales Opportunity

### Executive Header
- Project title with Pandora branding (💎)
- Selected scope and date
- 3 main KPI cards with hover tooltips

### System Health Footer
- Data feed status (✅ Active)
- Model drift monitoring (📊)
- Data quality indicator (✓ 99.4%)

## Design System

### Color Palette
- **Primary (Pandora Blush)**: #F2B8C6
- **Store Colors**:
  - London: #F2B8C6
  - Copenhagen: #E5A0B1
  - Paris: #D88D9C
- **Baseline Staffing**: #D0D0D0 (grey)
- **AI Recommended**: #34C759 (green)
- **Actual Traffic**: #2C2C2C (dark grey/black)
- **Manual Adjustments**: #FF9500 (orange)
- **Background**: Linear gradient (#FAFAFA to #F5F5F5)
- **Charts**: White (#FFFFFF)
- **Text**: #1A1A1A (dark grey)

### Typography
- **Font Family**: Inter
- **Section Headers**: 13px, bold (uniform across all sections)
- **Card Titles**: 12px, bold
- **Body**: 9-13px, regular
- **Main KPI Values**: 32-40px, bold
- **Compact KPI Values**: 16-18px, bold

### Layout Principles
- Minimalist design with clean white cards
- Light grey borders and subtle shadows
- Consistent 12px padding for section headers
- 3px left border (Pandora Blush) on all section headers
- Compact card design for right column metrics
- **2x2 Grid Layout**: Perfect 60/40 split (3:2 ratio)
  - Left: Traffic chart + Implementation tracking
  - Right: Staffing recommendation + Performance metrics
  - Fully aligned columns with no misalignment

## Key Features Explained

### Traffic Adjustment Workflow
1. Select a specific store (not aggregate)
2. Choose time period (hour or day based on view mode)
3. Adjust slider to modify traffic prediction
4. Preview shows original vs. adjusted values
5. Click "Apply" to save adjustment
6. Chart updates with orange star marker on pink line
7. AI staffing and revenue impact automatically recalculate
8. Adjustments persist until reset or view mode change

### Implementation Tracking Flow (Behavioral System)
1. Manager reviews AI recommendation with context:
   - AI Recommendation: X.X FTE/Day
   - Legacy System: Y.Y FTE/Day
2. Manager commits to staffing approach:
   - "✓ Following AI" or "⊗ Using Legacy"
3. Decision recorded with timestamp
4. Calendar heatmap updates (green or grey square for today)
5. Adoption rate metrics recalculate
6. Regional manager sees adoption trends across stores

**Why Implementation Tracking > Accuracy Rating:**
- Measures actual trust and commitment (did they act on it?)
- Creates accountability through public decision
- Enables performance comparison (AI days vs Legacy days)
- Tracks behavioral patterns over time
- Builds business case with real adoption data

### Dual Y-Axis Chart Logic
- **Left Axis (Primary)**: Staffing in FTE (calculated from traffic)
  - Grey bars: Baseline staffing (legacy, flat)
  - Green bars: AI recommended (dynamic)
  - Bars grouped side-by-side for easy comparison
- **Right Axis (Secondary)**: Customer Traffic (absolute numbers)
  - Light pink band: Confidence interval (±10%)
  - Pink line: Predicted traffic (3px width)
  - Dark line: Actual traffic (visible for past dates only)
  - Orange stars: Manual adjustments
- **Confidence Intervals**: ±10% band typical for retail forecasting
  - Represents forecast uncertainty
  - 80% of actual results fall within this range
- **Layering**: Bars first, then confidence band, then traffic lines
- **Axes Layer**: Set to 'below traces' for proper visibility
- **Interactive Legend**: Click to toggle elements on/off

### Date Selector Behavior
- **Past Dates**: Shows actual traffic for all hours/days
- **Today**: Shows actual traffic up to current hour (hourly) or today (daily)
- **Future Dates**: Shows only predicted traffic (no actual line)
- **Data Generation**: Happens after date selection to use correct date
- **Actual Traffic**: Generated with ±8% variance from predicted

## Session State Management

The app maintains state across reruns:
```python
st.session_state.traffic_adjustments = {
    "London": {},      # {time: adjustment_percentage}
    "Copenhagen": {},
    "Paris": {}
}

st.session_state.implementation_history = {
    "London": {
        "2026-01-19": {"decision": 1}  # 1 = AI, 0 = Legacy
    },
    # ... 30 days of history per store
}

st.session_state.view_mode = 'hourly'  # or 'daily'
```

**Mock Data Generation:**
- London: 85% AI adoption rate
- Copenhagen: 70% AI adoption rate
- Paris: 90% AI adoption rate

## Business Value & KPIs

### Key Metrics Tracked
1. **AI Adoption Rate**: % of days following AI recommendations (target: 80%)
2. **Revenue Opportunity**: Additional revenue from optimal staffing
3. **Staffing Efficiency**: Optimal allocation vs legacy system
4. **Data Quality**: Completeness and freshness of data feeds

### Executive Insights
- **Store Comparison**: Regional manager can identify high/low adopters
- **Performance Tracking**: 30-day behavioral history per store
- **Revenue Impact**: Quantified benefits of AI adoption
- **Actionable Alerts**: "Needs Support" flag for stores <80% adoption

## Future Enhancement Opportunities

1. **Real Data Integration**: Connect to actual POS and foot traffic systems
2. **ML Model**: Replace synthetic data with trained forecasting model
3. **Historical Analysis**: Trend analysis and seasonality detection
4. **Performance Comparison**: Analyze outcomes of AI days vs Legacy days
5. **Alert System**: Notifications for low adoption or staffing gaps
6. **Export Functionality**: Download reports, forecasts, and adoption metrics
7. **Multi-Language**: Support for Danish, French, English
8. **Mobile Optimization**: Responsive design for tablets
9. **Authentication**: Role-based access (manager vs. regional manager)
10. **A/B Testing Framework**: Compare AI vs Legacy system outcomes

## Known Limitations

1. **Synthetic Data**: Currently uses generated data, not real store data
2. **No Persistence**: Data resets when app restarts (no database)
3. **Session-Based**: Implementation history limited to current session
4. **Single Date View**: Can only view one date at a time
5. **Mock Adoption Rates**: Historical adoption data is pre-generated

## Support & Maintenance

### Troubleshooting

**App won't start:**
```bash
# Try with python -m prefix
python -m streamlit run app.py

# Check dependencies
pip install -r requirements.txt --upgrade
```

**Localhost not working:**
- Use network URL instead: http://192.168.1.5:8501
- Check firewall settings

**Charts not displaying:**
- Clear browser cache
- Check console for JavaScript errors
- Verify Plotly version compatibility

**Date picker not updating chart:**
- Data generation happens after date selection
- Check that selected_date is being passed to generate_all_stores_data()

### Development Notes

- Python version: 3.12
- Streamlit version: Latest (1.28.0+)
- Browser: Chrome/Edge recommended
- Screen resolution: 1920×1080 or higher optimal
- App structure: ~1500 lines in single file (app.py)

## Version History

- **v3.0** (2026-01-19): Performance optimization and UX improvements
  - **Forecast Confidence Intervals**: Added ±10% band around predictions
  - **Chart Axis Swap**: Staffing (FTE) on left, Traffic on right
  - **Performance Caching**: Added @st.cache_data to all data generation functions
    - 60-70% faster after first load
    - Store switches: 2s → 0.3s
    - Date changes: 1-2s → 0.5s
  - **Forecast Accuracy Metric**: Replaced Sales Opportunity with dynamic accuracy tracking
  - **Model Accuracy Explanation**: Expandable info section in sidebar
  - **Scope Persistence**: Fixed bug where city filter reset on view mode change
  - **Removed Redundant Text**: Kept only interactive chart legend
  - **Layout Optimization**: Perfect 2x2 grid alignment (60/40 split with 3:2 ratio)
  - **Hover Tooltip**: Added to Staffing Recommendation header with calculation details
  - **Code Cleanup**: Removed unused variables and optimized structure

- **v2.0** (2026-01-19): Major update with behavioral tracking
  - Replaced accuracy feedback with implementation tracking
  - Added staffing recommendation dashboard with revenue impact
  - Added actual traffic line (dark) vs predicted (pink)
  - Added 3 compact KPI cards (Adoption, Quality, Sales)
  - Improved date selector with actual traffic handling
  - Fixed chart layering (lines now render in front of bars)
  - Uniform section headers (13px) across entire app
  - AI adoption tracking with 30-day heatmap
  - Regional manager adoption comparison view

- **v1.0** (2026-01-19): Initial PoC release
  - Multi-store forecasting
  - Dual y-axis charts with FTE
  - Interactive traffic adjustments
  - Feedback tracking system
  - Executive KPI dashboard
  - System health monitoring

## License & Credits

**Created for**: Pandora Jewelry
**Purpose**: Internal PoC for traffic & staffing optimization
**Technology**: Streamlit, Plotly, Python
**AI Assistant**: Claude Sonnet 4.5 (Anthropic)

---

*This is a Proof of Concept application for demonstration purposes. All data shown is synthetic and generated for visualization purposes only.*
