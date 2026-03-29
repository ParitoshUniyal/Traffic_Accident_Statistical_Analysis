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
st.title("🚗 Traffic Accident Analysis Dashboard")

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

# Dataset preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Section title
st.subheader(f"Analysis for {selected_state}")

FIG_SIZE = (4, 2.5)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

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