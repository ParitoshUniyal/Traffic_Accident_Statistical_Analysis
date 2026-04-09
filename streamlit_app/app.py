import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
# st.write("Files Streamlit sees:", os.listdir("pages") if os.path.exists("pages") else "Pages folder not found")

@st.cache_data
def load_data():
    # This finds the directory where the current file is, then goes up to the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjusting path to get to the 'data' folder from 'streamlit_app' or 'pages'
    # If in app.py: current_dir is .../streamlit_app
    # If in pages/page.py: current_dir is .../streamlit_app/pages
    
    if "pages" in current_dir:
        path = os.path.join(current_dir, "../../data/cleaned_accidents.csv")
    else:
        path = os.path.join(current_dir, "../data/cleaned_accidents.csv")
        
    return pd.read_csv(path)

df = load_data()

plt.rcParams['figure.facecolor'] = '#0E1117'
plt.rcParams['axes.facecolor'] = '#0E1117'

sns.set_style("dark")

# Page config
st.set_page_config(page_title="Traffic Accident Dashboard", layout="wide")

# Added the white frame and rounded corners targeting Streamlit images
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    /* Hides the default multipage navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    /* Photo frame effect for all matplotlib graphs */
    [data-testid="stImage"] img {
        border: 2px solid white !important;
        border-radius: 15px !important;
        padding: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Traffic Accident Analysis Dashboard")

# Load data
df = pd.read_csv("../data/cleaned_accidents.csv")

# --- Sidebar Setup ---
st.sidebar.header("🎯 Control Panel")

# State Selection
states = ["All"] + sorted(df['state_name'].unique())
selected_state = st.sidebar.selectbox("Select State", states)

# Filter logic
if selected_state == "All":
    filtered_df = df
else:
    filtered_df = df[df['state_name'] == selected_state]

st.sidebar.markdown("---")
st.sidebar.subheader("Insights")

# Calculations
top_time = filtered_df['time_of_day'].mode()[0]
top_weather = filtered_df['weather_conditions'].mode()[0]
danger_road = filtered_df.groupby('road_condition')['number_of_fatalities'].sum().idxmax()
alcohol_counts = filtered_df['alcohol_involvement'].value_counts(normalize=True)
alcohol_pct = alcohol_counts.get('Yes', 0) * 100

# --- Beautiful Sidebar Insights ---

# 1. Peak Time Metric (Native Streamlit Metric)
st.sidebar.metric(label="Peak Accident Time", value=top_time)

# 2. Alcohol Involvement (Styled with a warning color)
st.sidebar.markdown(f"""
    <div style="background-color: rgba(255, 75, 75, 0.1); 
                padding: 15px; 
                border-left: 5px solid #FF4B4B; 
                border-radius: 5px; 
                margin-bottom: 10px;">
        <span style="color: #FF4B4B; font-weight: bold; font-size: 14px;">⚠️ ALCOHOL FACTOR</span><br>
        <span style="font-size: 22px; font-weight: bold; color: white;">{alcohol_pct:.1f}%</span>
        <p style="font-size: 12px; margin: 0; color: #808495;">of accidents involved alcohol</p>
    </div>
""", unsafe_allow_html=True)

# 3. Weather Insight (Sleek Blue Card)
st.sidebar.markdown(f"""
    <div style="background-color: rgba(0, 173, 181, 0.1); 
                padding: 15px; 
                border-left: 5px solid #00ADB5; 
                border-radius: 5px; 
                margin-bottom: 10px;">
        <span style="color: #00ADB5; font-weight: bold; font-size: 14px;">🌦️ PRIMARY WEATHER</span><br>
        <span style="font-size: 18px; font-weight: bold; color: white;">{top_weather}</span>
    </div>
""", unsafe_allow_html=True)

# 4. Road Condition (Simple Highlight)
st.sidebar.markdown(f"""
    <div style="background-color: rgba(157, 78, 221, 0.1); 
                padding: 15px; 
                border-left: 5px solid #9D4EDD; 
                border-radius: 5px;">
        <span style="color: #9D4EDD; font-weight: bold; font-size: 14px;">🛣️ HIGH RISK ROAD</span><br>
        <span style="font-size: 16px; font-weight: bold; color: white;">{danger_road} Surfaces</span>
    </div>
""", unsafe_allow_html=True)


# Dataset preview
# st.subheader("Dataset Preview")
# st.dataframe(df.head())

# ---- Key Insights Section ----
st.subheader("Key Insights")

colA, colB, colC, colD = st.columns(4)

# Re-calculating values for the cards
total_accidents = len(filtered_df)
avg_casualties = filtered_df['number_of_casualties'].mean()
alcohol_pct = (filtered_df['alcohol_involvement'].value_counts(normalize=True).get('Yes', 0)) * 100
common_severity = filtered_df['accident_severity'].mode()[0]

# Helper function for the "Beautiful" Card
def draw_key_card(column, label, value, color, icon):
    column.markdown(f"""
    <div style="
        background: rgba(22, 27, 34, 0.5);
        padding: 24px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        text-align: left;
        position: relative;
        overflow: hidden;
        min-height: 140px;
    ">
        <div style="
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 4px; 
            height: 100%; 
            background-color: {color};
        "></div>
        <p style="color: #8B949E; font-size: 12px; margin: 0; text-transform: uppercase; letter-spacing: 1px;">{icon} {label}</p>
        <h2 style="color: white; margin: 10px 0 0 0; font-size: 32px; font-weight: 700;">{value}</h2>
        <p style="color: {color}; font-size: 12px; margin: 5px 0 0 0; font-weight: 600;">Active Filter Data</p>
    </div>
    """, unsafe_allow_html=True)

# Card 1: Total Accidents
with colA:
    draw_key_card(colA, "Total Incidents", f"{total_accidents:,}", "#00ADB5", "📉")

# Card 2: Avg Casualties
with colB:
    draw_key_card(colB, "Avg Casualties", f"{avg_casualties:.2f}", "#F8B400", "🚑")

# Card 3: Alcohol Involvement
with colC:
    draw_key_card(colC, "Alcohol Cases", f"{alcohol_pct:.1f}%", "#FF6363", "🍺")

# Card 4: Main Severity
with colD:
    draw_key_card(colD, "Top Severity", common_severity, "#9D4EDD", "⚠️")

st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Quick Navigation")

if st.sidebar.button("🏠 Home Overview", use_container_width=True):
    st.switch_page("app.py")

if st.sidebar.button("👤 Driver Analysis", use_container_width=True):
    # This must match the folder name 'pages' and the filename exactly
    st.switch_page(r"pages/driver_analysis.py") 

if st.sidebar.button("🌦️ Environmental Factors", use_container_width=True):
    st.switch_page(r"pages/Environmental_Factors.py")
    
# Section title
st.subheader(f"Analysis for {selected_state}")

FIG_SIZE = (4, 2.5)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

st.subheader("Additional Insights")
col5, col6 = st.columns(2)

st.subheader("Trends & Comparisons")
col7, col8 = st.columns(2)

st.subheader("Impact Analysis")
col9, col10 = st.columns(2)

st.subheader("Behavioral Insights")
col11, col12 = st.columns(2)

# Chart 1: Severity
with col1:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    sns.countplot(x='accident_severity', data=filtered_df, ax=ax, palette='viridis')

    # Style text for dark theme
    ax.set_title("Accident Severity", fontsize=10, color='white')
    ax.set_xlabel("", color='white')
    ax.set_ylabel("", color='white')

    ax.tick_params(colors='white')

    # Remove spines (clean look)
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)

# Chart 2: Weather
with col2:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    # FORCE dark background
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    weather_counts = filtered_df['weather_conditions'].value_counts()

    sns.barplot(
        x=weather_counts.values,
        y=weather_counts.index,
        ax=ax,
        palette='viridis'
    )

    # Style text for dark theme
    ax.set_title("Weather Distribution", fontsize=10, color='white')
    ax.set_xlabel("", color='white')
    ax.set_ylabel("", color='white')

    ax.tick_params(colors='white')

    # Remove spines (clean look)
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)
# Chart 3: Road Condition
with col3:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    # FORCE dark background
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    sns.countplot(x='road_condition', data=filtered_df, ax=ax, palette='coolwarm')
    ax.set_title("Road Condition", fontsize=10, color='white')
    ax.set_xlabel("", color='white')
    ax.set_ylabel("", color='white')

    ax.tick_params(colors='white')

    # Remove spines (clean look)
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.xticks(rotation=25, fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)

# Chart 4: Lighting
with col4:
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    # FORCE dark background
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
        
    sns.countplot(x='lighting_conditions', data=filtered_df, ax=ax, palette='magma')
    ax.set_title("Lighting Conditions", fontsize=10, color='white')
    ax.set_xlabel("", color='white')
    ax.set_ylabel("", color='white')

    ax.tick_params(colors='white')

    # Remove spines (clean look)
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.xticks(rotation=25, fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
with col5:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    gender_counts = filtered_df['driver_gender'].value_counts()

    wedges, texts, autotexts = ax.pie(
        gender_counts,
        autopct='%1.0f%%',
        startangle=90,
        colors=sns.color_palette("pastel")
    )
    ax.set_title("Driver Gender", fontsize=10, color='white')

    ax.legend(
        wedges,
        gender_counts.index,
        title="Gender",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        labelcolor='white'
    )

    for text in autotexts:
        text.set_color('white')

    plt.tight_layout()
    st.pyplot(fig)

with col6:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    alcohol_counts = filtered_df['alcohol_involvement'].value_counts()

    wedges, texts, autotexts = ax.pie(
        alcohol_counts,
        autopct='%1.0f%%',
        startangle=90,
        colors=sns.color_palette("coolwarm")
    )

    ax.set_title("Alcohol Involvement", fontsize=10, color='white')

    ax.legend(
        wedges,
        alcohol_counts.index,
        title="Alcohol",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        labelcolor='white'
    )

    for text in autotexts:
        text.set_color('white')

    plt.tight_layout()
    st.pyplot(fig)

with col7:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    yearly_counts = filtered_df.groupby('year').size()

    ax.plot(yearly_counts.index, yearly_counts.values, marker='o')

    ax.set_title("Yearly Accidents", fontsize=10, color='white')
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.grid(alpha=0.2)

    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)

with col8:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    if selected_state == "All":
        state_counts = df['state_name'].value_counts().head(10)
    else:
        state_counts = filtered_df['city_name'].value_counts().head(10)

    sns.barplot(
        x=state_counts.values,
        y=state_counts.index,
        ax=ax,
        palette='magma'
    )

    ax.set_title("Top Locations", fontsize=10, color='white')
    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)

with col9:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    fatalities_by_state = (
        filtered_df.groupby('state_name')['number_of_fatalities']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    sns.barplot(
        x=fatalities_by_state.values,
        y=fatalities_by_state.index,
        ax=ax,
        palette='Reds'
    )

    ax.set_title("Top States by Fatalities", fontsize=10, color='white')
    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)

with col10:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    severity_vehicle = pd.crosstab(
        filtered_df['vehicle_type_involved'],
        filtered_df['accident_severity']
    )

    x = range(len(severity_vehicle.index))

    ax.bar([i - 0.25 for i in x], severity_vehicle['Fatal'], 
       width=0.25, label='Fatal', color="#295179")

    ax.bar([i for i in x], severity_vehicle['Minor'], 
        width=0.25, label='Minor', color='#A8DADC')

    ax.bar([i + 0.25 for i in x], severity_vehicle['Serious'], 
        width=0.25, label='Serious', color='#457B9D')

    ax.set_xticks(x)
    ax.set_xticklabels(severity_vehicle.index, rotation=45, fontsize=8)

    ax.set_title("Vehicle Type vs Severity", fontsize=10, color='white')

    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(axis='y', alpha=0.15)

    legend = ax.legend(facecolor='#0E1117', edgecolor='none')
    for text in legend.get_texts():
        text.set_color('white')

    plt.tight_layout()
    st.pyplot(fig)

with col11:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    # Create age bins
    age_bins = [0, 18, 25, 35, 45, 60, 100]
    age_labels = ['<18', '18-25', '26-35', '36-45', '46-60', '60+']

    filtered_df['age_group'] = pd.cut(
        filtered_df['driver_age'],
        bins=age_bins,
        labels=age_labels
    )

    age_counts = filtered_df['age_group'].value_counts().sort_index()

    # Soft blue gradient vibe
    line_color = '#7FD1FF'   # main
    glow_color = '#7FD1FF'   # same but used for glow

    # Glow effect (draw multiple transparent lines)
    for i in range(1, 5):
        ax.plot(age_counts.index, age_counts.values,
                linewidth=2 + i,
                alpha=0.05,
                color=glow_color)

    # Main line
    ax.plot(age_counts.index, age_counts.values,
            marker='o',
            linewidth=2.5,
            color=line_color)

    ax.set_title("Accidents by Age Group", fontsize=10, color='white')

    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(alpha=0.15)

    plt.tight_layout()
    st.pyplot(fig)

with col12:
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    control_counts = filtered_df['traffic_control_presence'].value_counts()

    
    colors = ['#BDE0FE', '#89C2D9', '#468FAF'] 
    
    sns.barplot(
    x=control_counts.values,
    y=control_counts.index,
    ax=ax,
    palette=colors
    )
    for p in ax.patches:
        p.set_alpha(0.85)

    ax.set_title("Traffic Control Presence", fontsize=10, color='white')

    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)