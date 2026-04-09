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

st.sidebar.markdown("---")
st.sidebar.subheader("Insights")
# Calc insights
top_factor = filtered_df['driver_action'].mode()[0] if 'driver_action' in filtered_df.columns else "N/A"
alcohol_pct = (filtered_df['alcohol_involvement'].value_counts(normalize=True).get('Yes', 0)) * 100

st.sidebar.metric("Alcohol Involvement", f"{alcohol_pct:.1f}%")

st.sidebar.markdown(f"""
    <div class="sidebar-card" style="border-left-color: #9D4EDD;">
        <span style="color: #9D4EDD; font-weight: bold;">⚠️ TOP ACTION</span><br>
        <span style="font-size: 16px; color: white;">{top_factor}</span>
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

with col1:
    # Bar chart: Alcohol vs Severity
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    ct = pd.crosstab(filtered_df['alcohol_involvement'], filtered_df['accident_severity'], normalize='index') * 100
    ct.plot(kind='bar', stacked=True, ax=ax, color=['#295179', '#457B9D', '#A8DADC'])
    
    ax.set_title("Alcohol Involvement vs Severity (%)", color='white')
    ax.tick_params(colors='white', labelsize=8)
    ax.legend(facecolor='#0E1117', edgecolor='none', labelcolor='white', fontsize=8)
    for spine in ax.spines.values(): spine.set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    # Scatter plot: Age vs Number of Casualties
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    sns.regplot(data=filtered_df, x='driver_age', y='number_of_casualties', 
                scatter_kws={'alpha':0.3, 'color':'#00ADB5'}, line_kws={'color':'#FF6363'}, ax=ax)
    
    ax.set_title("Driver Age vs. Number of Casualties", color='white')
    ax.tick_params(colors='white', labelsize=8)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values(): spine.set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)