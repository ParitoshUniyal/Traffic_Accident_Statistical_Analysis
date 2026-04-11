import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Page Config ---
st.set_page_config(page_title="Environmental Factors", layout="wide")

# --- CSS Styling (Consistency) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stImage"] img {
        border: 2px solid white !important;
        border-radius: 15px !important;
        padding: 5px !important;
    }
    .sidebar-card {
        background: rgba(22, 27, 34, 0.5);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00ADB5;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Robust pathing: Go up 2 levels if in pages/, 1 if in app.py
    if "pages" in current_dir:
        path = os.path.join(current_dir, "../../data/cleaned_accidents.csv")
    else:
        path = os.path.join(current_dir, "../data/cleaned_accidents.csv")
    
    df = pd.read_csv(path)
    
    # Pre-cleaning: Standardize "Unknown" values
    df['city_name'] = df['city_name'].replace(['Unknown', 'unknown', 'UNKNOWN'], None)
    return df

df = load_data()

# --- Sidebar Logic ---
st.sidebar.header("🎯 Environment Filters")
states = ["All"] + sorted(df['state_name'].unique())
selected_state = st.sidebar.selectbox("Select State", states)

filtered_df = df if selected_state == "All" else df[df['state_name'] == selected_state]

# Sidebar Insights
st.sidebar.markdown("---")
st.sidebar.subheader("Insights")

# Most common weather in the current selection
top_weather = filtered_df['weather_conditions'].mode()[0] if not filtered_df.empty else "N/A"

# Calculate Night-time Risk (Dark, Dusk, Dawn)
night_conditions = ['Dark', 'Dusk', 'Dawn']
night_count = filtered_df[filtered_df['lighting_conditions'].isin(night_conditions)].shape[0]
night_pct = (night_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0

st.sidebar.metric("Low-Light Accidents", f"{night_pct:.1f}%")

st.sidebar.markdown(f"""
    <div class="sidebar-card">
        <span style="color: #00ADB5; font-weight: bold;">🌦️ PRIMARY WEATHER</span><br>
        <span style="font-size: 16px; color: white;">{top_weather}</span>
    </div>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Quick Navigation")
if st.sidebar.button("🏠 Home Overview", use_container_width=True): st.switch_page("app.py")
if st.sidebar.button("👤 Driver Analysis", use_container_width=True): st.switch_page("pages/driver_analysis.py")
if st.sidebar.button("🌦️ Environmental Factors", use_container_width=True): st.switch_page("pages/Environmental_Factors.py")

# --- Main Content ---
st.title("🌦️ Environmental & Infrastructure Analysis")
st.markdown(f"Investigating external risk factors in **{selected_state}**")

# Section 1: Incident Locations (Fixed)
st.subheader("1. Top Impacted Cities")
# Filter out nulls (which include the old 'Unknown' values)
clean_city_data = filtered_df.dropna(subset=['city_name'])

if not clean_city_data.empty:
    top_cities = clean_city_data['city_name'].value_counts().head(10)
    # Using a horizontal bar chart for better readability of city names
    st.bar_chart(top_cities, color='#00ADB5', horizontal=True)
else:
    st.info("No specific city data available for the current selection (all data may be 'Unknown').")

# Section 2: Weather & Road Interaction
st.subheader("2. Weather vs. Road Condition Density")
col_plot, col_stats = st.columns([2, 1])

with col_plot:
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    pivot_data = filtered_df.pivot_table(
        index='weather_conditions', 
        columns='road_condition', 
        values='number_of_fatalities', 
        aggfunc='size'
    ).fillna(0)

    sns.heatmap(pivot_data, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax, cbar=False)
    ax.tick_params(colors='white')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col_stats:
    st.write("#### Danger Zones")
    st.markdown("Most lethal weather/road combinations:")
    high_risk = filtered_df.groupby(['weather_conditions', 'road_condition'])['number_of_fatalities'].sum().reset_index()
    high_risk = high_risk.sort_values(by='number_of_fatalities', ascending=False).head(5)
    st.dataframe(high_risk, hide_index=True, use_container_width=True)

# Section 3: Infrastructure Impact
st.subheader("3. Infrastructure & Visibility")
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Severity by Lighting")
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    sns.countplot(data=filtered_df, x='lighting_conditions', hue='accident_severity', palette='viridis', ax=ax)
    ax.tick_params(colors='white', labelsize=8)
    ax.legend(facecolor='#0E1117', labelcolor='white', fontsize=8)
    for spine in ax.spines.values(): spine.set_visible(False)
    st.pyplot(fig)

with c2:
    st.markdown("#### Traffic Control Performance")
    control_stats = filtered_df.groupby('traffic_control_presence')['number_of_casualties'].mean().reset_index()
    control_stats.columns = ['Control Type', 'Avg Casualties']
    st.table(control_stats.style.background_gradient(cmap='Blues'))

# --- Section 4: Speed & Road Infrastructure ---
st.markdown("---")
st.subheader("4. Speed & Road Infrastructure Analysis")
col_speed, col_road = st.columns([1, 2])

with col_speed:
    st.markdown("#### Fatalities by Speed Zone")
    
    # Binning speed limits into 4 clean categories for the Radar Chart
    def bin_speed(speed):
        if speed <= 40: return 'City (0-40)'
        elif speed <= 70: return 'Suburban (41-70)'
        elif speed <= 100: return 'Highway (71-100)'
        else: return 'Express (101+)'

    temp_speed_df = filtered_df.copy()
    temp_speed_df['speed_zone'] = temp_speed_df['speed_limit_kmh'].apply(bin_speed)
    speed_impact = temp_speed_df.groupby('speed_zone')['number_of_fatalities'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#161B22')
    
    categories = speed_impact['speed_zone'].tolist()
    values = speed_impact['number_of_fatalities'].tolist()
    num_vars = len(categories)
    angles = [n / float(num_vars) * 2 * 3.14159 for n in range(num_vars)]
    angles += angles[:1]
    values += values[:1]
    
    ax.plot(angles, values, color='#FF6363', linewidth=2)
    ax.fill(angles, values, color='#FF6363', alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color='white', size=8)
    ax.set_yticklabels([])
    ax.spines['polar'].set_color('#30363D')
    st.pyplot(fig)

with col_road:
    st.markdown("#### Road Type vs. Condition Matrix")
    road_matrix = pd.crosstab(
        filtered_df['road_type'], 
        filtered_df['road_condition'], 
        values=filtered_df['number_of_casualties'], 
        aggfunc='mean'
    ).fillna(0)
    
    st.dataframe(
        road_matrix.style.background_gradient(cmap='viridis', axis=None)
        .format("{:.2f}"),
        use_container_width=True,
        height=300
    )
# --- Section 5: Structural & Weekly Risk Breakdown ---
st.markdown("---")
st.subheader("5. Road Infrastructure & Weekly Risk")
col_table, col_day = st.columns([1, 1.2])

with col_table:
    st.markdown("#### Road Safety Scoreboard")
    # Aggregating multiple metrics to create a "Risk Score" per road type
    road_safety = filtered_df.groupby('road_type').agg({
        'number_of_fatalities': 'sum',
        'number_of_casualties': 'mean',
        'number_of_vehicles_involved': 'max'
    }).rename(columns={
        'number_of_fatalities': 'Total Deaths',
        'number_of_casualties': 'Avg Injuries',
        'number_of_vehicles_involved': 'Max Pile-up'
    }).sort_values(by='Total Deaths', ascending=False)

    # Displaying as a beautiful, color-coded table
    st.dataframe(
        road_safety.style.background_gradient(cmap='OrRd', subset=['Total Deaths'])
        .background_gradient(cmap='YlGnBu', subset=['Avg Injuries'])
        .format("{:.1f}", subset=['Avg Injuries']),
        use_container_width=True
    )
    st.caption("Detailed breakdown of lethality vs. complexity per road category.")

with col_day:
    st.markdown("#### Weekly Vehicle Involvement")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_stats = filtered_df.groupby('day_of_week')['number_of_vehicles_involved'].mean().reindex(day_order)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    sns.barplot(x=day_stats.index, y=day_stats.values, palette="flare", ax=ax)
    
    ax.set_title("Avg Vehicles Involved per Day", color='white', fontsize=10)
    ax.tick_params(colors='white', labelsize=8)
    plt.xticks(rotation=30)
    for spine in ax.spines.values(): spine.set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)