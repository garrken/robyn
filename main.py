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

        # Streamlit progress bar for feedback
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Download the repository as a zip file
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        zip_path = "robyn.zip"
        downloaded_size = 0

        # Save the downloaded content in chunks
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    progress_bar.progress(min(downloaded_size / total_size, 1.0))
                    status_text.text(f"Downloaded {downloaded_size} of {total_size} bytes...")

        # Extract only the relevant part of the repository
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.startswith("Robyn-main/python/src/robyn/"):
                    zip_ref.extract(file, ".")
        
        # Move extracted files to robyn_code for simplicity
        if os.path.exists("Robyn-main/python/src/robyn"):
            os.rename("Robyn-main/python/src/robyn", "robyn_code")

        # Create __init__.py if missing
        init_file = os.path.join("robyn_code", "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                pass

        # Cleanup unnecessary files
        os.remove(zip_path)
        if os.path.exists("Robyn-main"):
            import shutil
            shutil.rmtree("Robyn-main")

        # Update status
        status_text.text("Download complete!")
        progress_bar.empty()

# Download Robyn Python code if not already available
with st.spinner("Setting up Robyn, please wait..."):
    download_and_prepare_robyn()

# Verify file structure
st.write("Verifying file structure:")
if os.path.exists("robyn_code"):
    st.write("robyn_code contents:")
    st.write(os.listdir("robyn_code"))
else:
    st.error("robyn_code directory does not exist.")

# Import Robyn dynamically after ensuring it's downloaded
try:
    from robyn_code.robyn import Robyn
    st.write("Successfully imported 'Robyn'.")
except ImportError:
    st.error("Failed to import 'Robyn'. Please check the robyn_code structure.")
    st.stop()

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
