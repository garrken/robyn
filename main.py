import os
import requests
import zipfile
import streamlit as st
import pandas as pd

# Function to download and extract only the Python part of Robyn
def download_and_prepare_robyn():
    if not os.path.exists("robyn_code"):
        st.info("Downloading Robyn Python code...")
        url = "https://github.com/facebookexperimental/Robyn/archive/refs/heads/main.zip"
        
        # Download the repository as a zip file
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        zip_path = "robyn.zip"
        
        # Save the downloaded content
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        # Extract only the Python part of the repository
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.startswith("Robyn-main/python/"):
                    zip_ref.extract(file, ".")
        
        # Rename the extracted folder for simplicity
        os.rename("Robyn-main/python", "robyn_code")
        
        # Cleanup
        os.remove(zip_path)
        os.rmdir("Robyn-main")

# Download Robyn Python code if not already available
with st.spinner("Setting up Robyn, please wait..."):
    download_and_prepare_robyn()

# Import Robyn dynamically after ensuring it's downloaded
from robyn_code.robyn import Robyn

# Streamlit app starts here
st.title("Robyn SaaS - Marketing Mix Modeling")

# Sidebar for settings
st.sidebar.header("Settings")

# File uploader for data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Load and display raw data
    raw_data = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(raw_data.head())

    # Prepare the data
    def prepare_data(data):
        """Prepare data for Robyn modeling."""
        data.fillna(0, inplace=True)
        for col in data.select_dtypes(include=["float", "int"]).columns:
            data[col] = data[col].clip(lower=0)
        return data

    prepared_data = prepare_data(raw_data)
    st.subheader("Prepared Data")
    st.dataframe(prepared_data.head())

    # Run Robyn Model
    if st.button("Run Robyn Model"):
        temp_csv_path = "temp_data.csv"
        prepared_data.to_csv(temp_csv_path, index=False)

        robyn_instance = Robyn(csv_input=temp_csv_path, alpha=0.5)
        robyn_instance.run()

        st.success("Robyn Model executed successfully!")
        st.image(robyn_instance.get_plot_data(), caption="ROAS Plot")
        st.image(robyn_instance.get_media_mix_plot(), caption="Media Mix")

    # Sidebar optimization settings
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
