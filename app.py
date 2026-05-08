import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Traffic Accident Dashboard",
    layout="wide"
)

# Load dataset
df = pd.read_csv(
    "data/sample_accidents.csv",
    nrows=50000
)

# Convert datetime column
df['Start_Time'] = pd.to_datetime(df['Start_Time'])

# Create new columns
df['Hour'] = df['Start_Time'].dt.hour
df['Month'] = df['Start_Time'].dt.month

# Dashboard Title
st.title("🚗 Traffic Accident Analysis Dashboard")

st.markdown("""
Analyze accident trends, severity levels, weather conditions,
and hotspot locations using interactive visualizations.
""")

st.markdown("---")

# Sidebar
st.sidebar.header("🔍 Dashboard Filters")

selected_state = st.sidebar.selectbox(
    "Select State",
    ['All'] + sorted(list(df['State'].dropna().unique()))
)

# Apply filter
if selected_state != 'All':
    df = df[df['State'] == selected_state]

# KPI Metrics
st.subheader("📌 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Accidents",
    f"{len(df):,}"
)

col2.metric(
    "Average Severity",
    round(df['Severity'].mean(), 2)
)

col3.metric(
    "Unique Cities",
    df['City'].nunique()
)

st.markdown("---")

# Severity Charts
st.subheader("⚠️ Accident Severity Analysis")

col4, col5 = st.columns(2)

# Histogram
severity_chart = px.histogram(
    df,
    x='Severity',
    title='Severity Distribution',
    color='Severity',
    template='plotly_dark'
)

col4.plotly_chart(
    severity_chart,
    width='stretch'
)

# Pie Chart with labels
severity_pie = px.pie(
    df,
    names='Severity',
    title='Severity Percentage',
    hole=0.4,
    template='plotly_dark'
)

severity_pie.update_traces(
    textinfo='percent+label'
)

col5.plotly_chart(
    severity_pie,
    width='stretch'
)

st.markdown("---")

# Time Analysis
st.subheader("⏰ Time-Based Analysis")

col6, col7 = st.columns(2)

# Hour Chart
hour_chart = px.histogram(
    df,
    x='Hour',
    title='Accidents by Hour',
    color='Hour',
    template='plotly_dark'
)

col6.plotly_chart(
    hour_chart,
    width='stretch'
)

# Monthly Trend
monthly_chart = px.histogram(
    df,
    x='Month',
    title='Monthly Accident Trends',
    color='Month',
    template='plotly_dark'
)

col7.plotly_chart(
    monthly_chart,
    width='stretch'
)

st.markdown("---")

# City Analysis
st.subheader("🏙 Top Accident Cities")

top_cities = (
    df['City']
    .value_counts()
    .head(10)
)

city_chart = px.bar(
    x=top_cities.values,
    y=top_cities.index,
    orientation='h',
    title='Top 10 Accident-Prone Cities',
    labels={
        'x': 'Number of Accidents',
        'y': 'City'
    },
    template='plotly_dark'
)

st.plotly_chart(
    city_chart,
    width='stretch'
)

st.markdown("---")

# Weather Analysis
st.subheader("🌦 Weather Condition Analysis")

weather_data = (
    df['Weather_Condition']
    .value_counts()
    .head(10)
)

weather_chart = px.bar(
    x=weather_data.index,
    y=weather_data.values,
    title='Top Weather Conditions',
    labels={
        'x': 'Weather Condition',
        'y': 'Accident Count'
    },
    template='plotly_dark'
)

st.plotly_chart(
    weather_chart,
    width='stretch'
)

st.markdown("---")

# Map Section
st.subheader("🗺 Accident Hotspot Locations")

map_data = (
    df[['Start_Lat', 'Start_Lng']]
    .dropna()
)

sample_df = map_data.sample(
    min(1000, len(map_data))
)

sample_df = sample_df.rename(
    columns={
        'Start_Lat': 'lat',
        'Start_Lng': 'lon'
    }
)

st.map(sample_df)

st.markdown("---")

# Dataset Preview
with st.expander("📂 View Dataset"):
    st.dataframe(df.head(100))