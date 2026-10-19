
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="6G Smart Factory Diagnostics", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("smart_factory_dataset.csv")
    if 'Date' in df.columns and 'Time' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    return df

df = load_data()

st.title("🏭 Manufacturing Process Health & Operational Efficiency Analysis in 6G-Smart Factories")

# Sidebar User Capabilities / Filters
st.sidebar.header("🎛️ User Capabilities / Filters")
machines = df['Machine_ID'].unique().tolist() if 'Machine_ID' in df.columns else []
selected_machines = st.sidebar.multiselect("Machine Selector", machines, default=machines)

operation_modes = df['Operation_Mode'].unique().tolist() if 'Operation_Mode' in df.columns else []
selected_modes = st.sidebar.multiselect("Operation Mode Filter", operation_modes, default=operation_modes)

# Filter dataframe based on selections
filtered_df = df.copy()
if selected_machines and 'Machine_ID' in df.columns:
    filtered_df = filtered_df[filtered_df['Machine_ID'].isin(selected_machines)]
if selected_modes and 'Operation_Mode' in df.columns:
    filtered_df = filtered_df[filtered_df['Operation_Mode'].isin(selected_modes)]

# Dashboard Modules Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Factory Health Overview", 
    "⚙️ Machine Health Dashboard", 
    "📈 Production & Quality Panel", 
    "🔍 Efficiency Diagnostics View"
])

with tab1:
    st.header("Factory Health Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_temp = filtered_df['Temperature_C'].mean() if 'Temperature_C' in filtered_df.columns else 0
        st.metric("Avg Temperature", f"{avg_temp:.2f} °C")
    with col2:
        avg_vib = filtered_df['Vibration_Hz'].mean() if 'Vibration_Hz' in filtered_df.columns else 0
        st.metric("Avg Vibration", f"{avg_vib:.2f} Hz")
    with col3:
        avg_pow = filtered_df['Power_Consumption_kW'].mean() if 'Power_Consumption_kW' in filtered_df.columns else 0
        st.metric("Avg Power", f"{avg_pow:.2f} kW")
    with col4:
        avg_def = filtered_df['Quality_Control_Defect_Rate_%'].mean() if 'Quality_Control_Defect_Rate_%' in filtered_df.columns else 0
        st.metric("Avg Defect Rate", f"{avg_def:.2f}%")

    if 'Efficiency_Status' in filtered_df.columns:
        fig_eff = px.pie(filtered_df, names='Efficiency_Status', title="Overall Efficiency Distribution")
        st.plotly_chart(fig_eff, use_container_width=True)

with tab2:
    st.header("Machine Health Dashboard")
    if 'Timestamp' in filtered_df.columns and 'Temperature_C' in filtered_df.columns:
        fig_trend = px.line(filtered_df, x='Timestamp', y='Temperature_C', color='Machine_ID', title="Machine-wise Sensor Trends (Temperature)")
        st.plotly_chart(fig_trend, use_container_width=True)
    
    if 'Predictive_Maintenance_Score' in filtered_df.columns:
        fig_score = px.box(filtered_df, x='Machine_ID', y='Predictive_Maintenance_Score', color='Machine_ID', title="Health Scorecards (Predictive Maintenance Score)")
        st.plotly_chart(fig_score, use_container_width=True)

with tab3:
    st.header("Production & Quality Panel")
    if 'Production_Speed_units_per_hr' in filtered_df.columns and 'Quality_Control_Defect_Rate_%' in filtered_df.columns:
        fig_pq = px.scatter(filtered_df, x='Production_Speed_units_per_hr', y='Quality_Control_Defect_Rate_%', color='Machine_ID', hover_data=['Operation_Mode'], title="Production Speed vs Defect Rate")
        st.plotly_chart(fig_pq, use_container_width=True)
    
    if 'Error_Rate_%' in filtered_df.columns:
        fig_err = px.bar(filtered_df, x='Machine_ID', y='Error_Rate_%', color='Operation_Mode', barmode='group', title="Error Frequency Visualizations")
        st.plotly_chart(fig_err, use_container_width=True)

with tab4:
    st.header("Efficiency Diagnostics View")
    if 'Efficiency_Status' in filtered_df.columns and 'Operation_Mode' in filtered_df.columns:
        fig_diag = px.histogram(filtered_df, x='Operation_Mode', color='Efficiency_Status', barmode='group', title="Efficiency Status Breakdown by Operation Mode")
        st.plotly_chart(fig_diag, use_container_width=True)
