import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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
    path = os.path.join(current_dir, "../../data/cleaned_accidents.csv")
    return pd.read_csv(path)

df = load_data()

# --- Sidebar Logic (Copied for consistency) ---
st.sidebar.header("🎯 Driver Analysis Filters")
states = ["All"] + sorted(df['state_name'].unique())
selected_state = st.sidebar.selectbox("Select State", states)

if selected_state == "All":
    filtered_df = df
else:
    filtered_df = df[df['state_name'] == selected_state]

# st.sidebar.markdown("---")
# st.sidebar.subheader("Insights")
# # Calc insights
# top_factor = filtered_df['driver_action'].mode()[0] if 'driver_action' in filtered_df.columns else "N/A"
# alcohol_pct = (filtered_df['alcohol_involvement'].value_counts(normalize=True).get('Yes', 0)) * 100

# st.sidebar.metric("Alcohol Involvement", f"{alcohol_pct:.1f}%")

# st.sidebar.markdown(f"""
#     <div class="sidebar-card" style="border-left-color: #9D4EDD;">
#         <span style="color: #9D4EDD; font-weight: bold;">⚠️ TOP ACTION</span><br>
#         <span style="font-size: 16px; color: white;">{top_factor}</span>
#     </div>
# """, unsafe_allow_html=True)

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


st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Quick Navigation")

if st.sidebar.button("🏠 Home Overview", use_container_width=True):
    st.switch_page("app.py")

if st.sidebar.button("👤 Driver Analysis", use_container_width=True):
    # Even though we are on this page, the path remains the same for consistency
    st.switch_page(r"pages/driver_analysis.py") 

if st.sidebar.button("🌦️ Environmental Factors", use_container_width=True):
    st.switch_page(r"pages/Environmental_Factors.py")

# --- Main Content ---
st.title("👤 Driver Behavior & Demographic Analysis")
st.markdown(f"Deep dive into accident patterns for **{selected_state}**")

# --- Section 1: Complex Distribution ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Age & Gender vs. Severity")
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    # Complex Violin Plot
    sns.violinplot(
        data=filtered_df, 
        x='accident_severity', 
        y='driver_age', 
        hue='driver_gender', 
        split=True, 
        inner="quart", 
        palette="magma",
        ax=ax
    )
    
    ax.set_title("Age Density Distribution by Severity", color='white', fontsize=12)
    ax.tick_params(colors='white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    for spine in ax.spines.values(): spine.set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)

with col_right:
    st.subheader("Statistical Summary")
    # A mini-table for age demographics
    age_stats = filtered_df.groupby('accident_severity')['driver_age'].agg(['mean', 'median', 'std'])
    st.table(age_stats.style.format("{:.1f}").background_gradient(cmap='Greys'))

# --- Section 2: The Data Table ---
st.subheader("📑 High-Risk Incident Log")
st.markdown("Sorted by most fatalities. Explore the raw patterns below.")

# Styling the dataframe
def color_severity(val):
    color = '#FF6363' if val == 'Fatal' else '#9D4EDD' if val == 'Serious' else '#00ADB5'
    return f'color: {color}; font-weight: bold'

display_cols = ['state_name', 'city_name', 'driver_age', 'driver_gender', 'accident_severity', 'number_of_fatalities', 'alcohol_involvement']
styled_df = filtered_df[display_cols].sort_values(by='number_of_fatalities', ascending=False).head(20)

st.dataframe(
    styled_df.style.applymap(color_severity, subset=['accident_severity']),
    use_container_width=True,
    height=400
)

# --- Section 3: Behavioral Correlation ---
st.subheader("Correlation Analysis")
col1, col2 = st.columns(2)

# Define a standard height/width for both figures
FIXED_SIZE = (6, 4.5)

with col1:
    st.markdown("### Alcohol Involvement vs Severity")
    fig, ax = plt.subplots(figsize=FIXED_SIZE)
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    ct = pd.crosstab(filtered_df['alcohol_involvement'], filtered_df['accident_severity'], normalize='index') * 100
    ct.plot(kind='bar', stacked=True, ax=ax, color=['#295179', '#457B9D', '#A8DADC'])
    
    # Remove Matplotlib title to use the Streamlit one above
    ax.set_title("") 
    ax.tick_params(colors='white', labelsize=9)
    ax.set_xlabel("Alcohol Involvement", color='white')
    ax.set_ylabel("Percentage (%)", color='white')
    
    legend = ax.legend(facecolor='#0E1117', edgecolor='none', labelcolor='white', fontsize=9)
    for spine in ax.spines.values(): spine.set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.markdown("### Average Casualty Trend by Age")
    fig, ax = plt.subplots(figsize=FIXED_SIZE)
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    # Line plot with confidence interval shadow
    sns.lineplot(
        data=filtered_df, 
        x="driver_age", 
        y="number_of_casualties", 
        color="#00ADB5", 
        linewidth=2, 
        ax=ax
    )
    
    ax.set_title("") # Remove Matplotlib title
    ax.tick_params(colors='white', labelsize=9)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.set_xlabel("Driver Age", color='white')
    ax.set_ylabel("Number of Casualties", color='white')
    
    for spine in ax.spines.values(): spine.set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)