import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="6G Smart Factory Diagnostics", layout="wide")
df = pd.read_csv("smart_factory_dataset.csv")

st.title("Factory Health Overview")
st.metric("Avg Temperature", f"{df['Temperature_C'].mean():.2f} °C")

fig_temp = px.line(df, x="Time", y="Temperature_C", color="Machine_ID", title="Temperature Trends")
st.plotly_chart(fig_temp)
