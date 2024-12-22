import os
import requests
import zipfile
import streamlit as st
import pandas as pd
from robyn_code.robyn import Robyn  # Dynamisk import efter nedladdning

# Function to download and extract Robyn code
def download_robyn_code():
    if not os.path.exists("robyn_code"):
        st.info("Downloading Robyn code...")
        url = "https://github.com/facebookexperimental/Robyn/archive/refs/heads/main.zip"
        
        # Download the zip file
        response = requests.get(url)
        zip_path = "robyn.zip"
        with open(zip_path, "wb") as f:
            f.write(response.content)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Move the necessary files to a folder called `robyn_code`
        os.rename("Robyn-main/python", "robyn_code")
        
        # Clean up unnecessary files
        os.remove(zip_path)
        os.rmdir("Robyn-main")

# Download Robyn at app start
download_robyn_code()

# App title
st.title("Robyn SaaS - Marketing Mix Modeling")

# Sidebar settings
st.sidebar.header("Settings")

# File uploader for data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Step 1: Load the uploaded file
    raw_data = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(raw_data.head())

    # Step 2: Prepare data (this part assumes a preparation function exists)
    def prepare_data(data):
        """Prepare data for Robyn modeling."""
        data.fillna(0, inplace=True)  # Handle missing values
        for col in data.select_dtypes(include=["float", "int"]).columns:
            data[col] = data[col].clip(lower=0)  # Clip negative values
        return data

    prepared_data = prepare_data(raw_data)
    st.subheader("Prepared Data")
    st.dataframe(prepared_data.head())

    # Step 3: Run Robyn model
    if st.button("Run Robyn Model"):
        temp_csv_path = "temp_data.csv"
        prepared_data.to_csv(temp_csv_path, index=False)

        robyn_instance = Robyn(csv_input=temp_csv_path, alpha=0.5)
        robyn_instance.run()

        st.success("Robyn Model executed successfully!")
        st.image(robyn_instance.get_plot_data(), caption="ROAS Plot")
        st.image(robyn_instance.get_media_mix_plot(), caption="Media Mix")

    # Step 4: Optimization settings
    st.sidebar.subheader("Optimization Settings")
    goal = st.sidebar.radio("Optimization Goal", ["Maximize ROAS", "Maximize Conversions"])
    budget = st.sidebar.slider("Total Budget (SEK)", 10000, 100000, 50000)

    if st.sidebar.button("Optimize Media Mix"):
        # Example optimization logic
        optimized_mix = {
            "Facebook": budget * 0.4,
            "Google Ads": budget * 0.3,
            "Instagram": budget * 0.2,
            "TikTok": budget * 0.1,
        }
        st.subheader("Optimized Media Mix")
        st.json(optimized_mix)

