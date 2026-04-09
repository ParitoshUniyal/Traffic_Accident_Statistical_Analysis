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

# --- Data Loading ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjust path if needed based on your structure
    path = os.path.join(current_dir, "../../data/cleaned_accidents.csv")
    return pd.read_csv(path)

df = load_data()

# --- Sidebar Logic ---
st.sidebar.header("🎯 Environment Filters")
states = ["All"] + sorted(df['state_name'].unique())
selected_state = st.sidebar.selectbox("Select State", states)

filtered_df = df if selected_state == "All" else df[df['state_name'] == selected_state]

# --- Main Content ---
st.title("🌦️ Environmental & Infrastructure Analysis")
st.markdown(f"Investigating external risk factors in **{selected_state}**")

# Section 1: The Correlation Heatmap
st.subheader("Weather vs. Road Condition Density")
fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#0E1117')

# Creating a pivot for the heatmap
pivot_data = filtered_df.pivot_table(
    index='weather_conditions', 
    columns='road_condition', 
    values='number_of_fatalities', 
    aggfunc='size' # Count of accidents
).fillna(0)

sns.heatmap(pivot_data, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax, cbar=False)

ax.set_title("Accident Frequency: Weather vs. Road Surface", color='white')
ax.tick_params(colors='white')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Section 2: Complexity Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Lighting Impact on Severity")
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    # Severity by Light
    sns.countplot(data=filtered_df, x='lighting_conditions', hue='accident_severity', palette='viridis', ax=ax)
    
    ax.set_title("Severity Distribution by Light", color='white')
    ax.tick_params(colors='white', labelsize=8)
    ax.legend(facecolor='#0E1117', labelcolor='white', fontsize=8)
    for spine in ax.spines.values(): spine.set_visible(False)
    plt.xticks(rotation=30)
    st.pyplot(fig)

with col2:
    st.subheader("Traffic Control Effectiveness")
    # A Styled Table showing average casualties by Traffic Control Presence
    control_stats = filtered_df.groupby('traffic_control_presence')['number_of_casualties'].mean().reset_index()
    control_stats.columns = ['Control Type', 'Avg Casualties']
    st.table(control_stats.style.background_gradient(cmap='Blues'))