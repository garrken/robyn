import streamlit as st
import pandas as pd
from data_preparation import prepare_data
from robyn_runner import run_robyn_model, optimize_media_mix

st.title("Robyn SaaS - Marketing Mix Modeling")
st.sidebar.header("Settings")

# Step 1: Upload Data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    raw_data = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(raw_data.head())

    # Step 2: Prepare Data
    prepared_data = prepare_data(raw_data)
    st.subheader("Prepared Data")
    st.dataframe(prepared_data.head())

    # Step 3: Run Robyn Model
    if st.button("Run Robyn Model"):
        results = run_robyn_model(prepared_data)
        st.success("Robyn Model executed successfully!")
        st.plotly_chart(results["roas_plot"], use_container_width=True)
        st.plotly_chart(results["media_mix_plot"], use_container_width=True)

    # Step 4: Optimize Media Mix
    st.sidebar.subheader("Optimization Settings")
    goal = st.sidebar.radio("Optimization Goal", ["Maximize ROAS", "Maximize Conversions"])
    budget = st.sidebar.slider("Total Budget", 10000, 100000, 50000)

    if st.sidebar.button("Optimize Media Mix"):
        optimized_results = optimize_media_mix(goal, budget, priority_channels=[])
        st.subheader("Optimized Media Mix")
        st.write(optimized_results)

