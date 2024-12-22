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

        # Streamlit progress bar for visual feedback
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

        # Extract only the Python part of the repository
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.startswith("Robyn-main/python/"):
                    zip_ref.extract(file, ".")
        if os.path.exists("Robyn-main/python"):
            os.rename("Robyn-main/python", "robyn_code")
        
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
    st.error("robyn_code does not exist.")

# Import Robyn dynamically after ensuring it's downloaded
try:
    from robyn_code.robyn import Robyn
except ModuleNotFoundError:
    st.error("Robyn code was not found. Ensure download_and_prepare_robyn is working correctly.")
    raise
