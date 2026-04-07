import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.facecolor'] = '#0E1117'
plt.rcParams['axes.facecolor'] = '#0E1117'

sns.set_style("dark")

# Page config
st.set_page_config(page_title="Traffic Accident Dashboard", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Traffic Accident Analysis Dashboard")

# Load data
df = pd.read_csv("../data/cleaned_accidents.csv")

# Sidebar filter FIRST
st.sidebar.header("Filters")

states = ["All"] + sorted(df['state_name'].unique())

selected_state = st.sidebar.selectbox("Select State", states)


# Filter logic
if selected_state == "All":
    filtered_df = df
else:
    filtered_df = df[df['state_name'] == selected_state]

st.sidebar.markdown("### 🧠 Insights")

# Most accident-prone time
top_time = filtered_df['time_of_day'].mode()[0]

# Most common weather
top_weather = filtered_df['weather_conditions'].mode()[0]

# Most dangerous road condition (based on fatalities)
danger_road = (
    filtered_df.groupby('road_condition')['number_of_fatalities']
    .sum()
    .idxmax()
)

# Alcohol involvement %
alcohol_pct = (
    filtered_df['alcohol_involvement']
    .value_counts(normalize=True)
    .get('Yes', 0) * 100
)

st.sidebar.markdown(f"""
- 🚗 Most accidents occur during **{top_time}**
- 🌦️ Common weather condition: **{top_weather}**
- 🛣️ Highest fatalities on **{danger_road}** roads
- 🍺 Alcohol involved in **{alcohol_pct:.0f}%** of cases
""")


# Dataset preview
# st.subheader("Dataset Preview")
# st.dataframe(df.head())

# ---- Key Insights Section ----
st.subheader("Key Insights")

colA, colB, colC, colD = st.columns(4)

# Card 1: Total Accidents
with colA:
    st.markdown(f"""
    <div style="
        background-color:#161B22;
        padding:15px;
        border-radius:10px;
        text-align:center;">
        <h3 style="color:white;">Total Accidents</h3>
        <h2 style="color:#00ADB5;">{len(filtered_df)}</h2>
    </div>
    """, unsafe_allow_html=True)

# Card 2: Avg Casualties
with colB:
    avg_casualties = filtered_df['number_of_casualties'].mean()
    st.markdown(f"""
    <div style="
        background-color:#161B22;
        padding:15px;
        border-radius:10px;
        text-align:center;">
        <h3 style="color:white;">Avg Casualties</h3>
        <h2 style="color:#F8B400;">{avg_casualties:.1f}</h2>
    </div>
    """, unsafe_allow_html=True)

# Card 3: Alcohol Involvement %
with colC:
    alcohol_pct = (filtered_df['alcohol_involvement'].value_counts(normalize=True).get('Yes', 0)) * 100
    st.markdown(f"""
    <div style="
        background-color:#161B22;
        padding:15px;
        border-radius:10px;
        text-align:center;">
        <h3 style="color:white;">Alcohol Cases</h3>
        <h2 style="color:#FF6363;">{alcohol_pct:.0f}%</h2>
    </div>
    """, unsafe_allow_html=True)

# Card 4: Most Common Severity
with colD:
    common_severity = filtered_df['accident_severity'].mode()[0]
    st.markdown(f"""
    <div style="
        background-color:#161B22;
        padding:15px;
        border-radius:10px;
        text-align:center;">
        <h3 style="color:white;">Top Severity</h3>
        <h2 style="color:#9D4EDD;">{common_severity}</h2>
    </div>
    """, unsafe_allow_html=True)

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