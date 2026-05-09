import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Geo-Spatial Traffic Accident Analytics",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

df = pd.read_csv(
    "data/sample_accidents.csv"
)

# Convert datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'])

# Extra columns
df['Hour'] = df['Start_Time'].dt.hour
df['Month'] = df['Start_Time'].dt.month

# ---------------- SIDEBAR ----------------

st.sidebar.title("🚦 Accident Analytics")

st.sidebar.markdown("""
### Geo-Spatial Dashboard

Analyze:
- Accident hotspots
- Severity trends
- Weather impact
- Geo-analysis
""")

selected_state = st.sidebar.selectbox(
    "📍 Select State",
    ['All'] + sorted(df['State'].dropna().unique())
)

# Filter
if selected_state != 'All':
    df = df[df['State'] == selected_state]

# ---------------- TITLE ----------------

st.title("🚗 Geo-Spatial Traffic Accident Analytics Platform")

st.markdown("""
Interactive dashboard for analyzing traffic accident severity,
weather impact, accident hotspots, and geo-spatial trends.
""")

st.markdown("---")

# ---------------- KPI SECTION ----------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "🚨 Total Accidents",
    f"{len(df):,}"
)

col2.metric(
    "⚠ Average Severity",
    round(df['Severity'].mean(), 2)
)

col3.metric(
    "🏙 Cities Covered",
    df['City'].nunique()
)

st.markdown("---")

# ---------------- TABS ----------------

tab1, tab2, tab3 = st.tabs([
    "📊 Analysis",
    "🗺 Hotspots",
    "📂 Dataset"
])

# =====================================================
# TAB 1 - ANALYSIS
# =====================================================

with tab1:

    st.subheader("⚠ Severity Analysis")

    col4, col5 = st.columns(2)

    # Severity Histogram
    severity_chart = px.histogram(
        df,
        x='Severity',
        color='Severity',
        template='plotly_dark',
        title='Severity Distribution'
    )

    col4.plotly_chart(
        severity_chart,
        width='stretch'
    )

    # Pie Chart
    severity_pie = px.pie(
        df,
        names='Severity',
        hole=0.4,
        template='plotly_dark',
        title='Severity Percentage'
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
    st.subheader("⏰ Time-Based Trends")

    col6, col7 = st.columns(2)

    # Hour Analysis
    hour_chart = px.histogram(
        df,
        x='Hour',
        color='Hour',
        template='plotly_dark',
        title='Accidents by Hour'
    )

    col6.plotly_chart(
        hour_chart,
        width='stretch'
    )

    # Monthly Trends
    month_chart = px.histogram(
        df,
        x='Month',
        color='Month',
        template='plotly_dark',
        title='Monthly Accident Trends'
    )

    col7.plotly_chart(
        month_chart,
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
        template='plotly_dark',
        title='Top 10 Accident-Prone Cities',
        labels={
            'x': 'Accident Count',
            'y': 'City'
        }
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
        template='plotly_dark',
        title='Top Weather Conditions',
        labels={
            'x': 'Weather',
            'y': 'Accidents'
        }
    )

    st.plotly_chart(
        weather_chart,
        width='stretch'
    )

# =====================================================
# TAB 2 - MAPS
# =====================================================

with tab2:

    st.subheader("🗺 Accident Hotspot Heatmap")

    map_data = (
        df[['Start_Lat', 'Start_Lng']]
        .dropna()
    )

    sample_df = map_data.sample(
        min(3000, len(map_data))
    )

    sample_df = sample_df.rename(
        columns={
            'Start_Lat': 'lat',
            'Start_Lng': 'lon'
        }
    )

    # Pydeck Heatmap
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=pdk.ViewState(
                latitude=37.7749,
                longitude=-122.4194,
                zoom=3,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=sample_df,
                    get_position='[lon, lat]',
                    radius=10000,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )

    st.markdown("---")

    st.subheader("📍 Accident Location Map")

    st.map(sample_df)

# =====================================================
# TAB 3 - DATASET
# =====================================================

with tab3:

    st.subheader("📂 Dataset Preview")

    st.dataframe(
        df.head(100),
        width='stretch'
    )

    st.markdown("---")

    # Download button
    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Dataset",
        csv,
        "accidents.csv",
        "text/csv"
    )

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
### 👩‍💻 Developed by Tanushree

Built using:
- Python
- Streamlit
- Plotly
- PyDeck
- Pandas
""")