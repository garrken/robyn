import os
import requests
import zipfile
import streamlit as st
import pandas as pd

os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

def download_and_prepare_robyn():
    if not os.path.exists("robyn_code"):
        st.info("Downloading Robyn Python code...")
        url = "https://github.com/facebookexperimental/Robyn/archive/refs/heads/main.zip"

        response = requests.get(url, stream=True)
        zip_path = "robyn.zip"

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        if os.path.exists("Robyn-main/python/src/robyn"):
            os.rename("Robyn-main/python/src/robyn", "robyn_code")
        else:
            st.error("Failed to extract robyn_code correctly!")

        os.remove(zip_path)

with st.spinner("Setting up Robyn, please wait..."):
    download_and_prepare_robyn()

# Debug robyn.py content
if os.path.exists("robyn_code/robyn.py"):
    st.write("Contents of robyn.py:")
    with open("robyn_code/robyn.py", "r") as file:
        st.code(file.read())
else:
    st.error("robyn.py is missing in robyn_code!")

try:
    from robyn_code.robyn import robyn as Robyn
    st.write("Successfully imported 'robyn' as 'Robyn'.")
except ImportError:
    try:
        from robyn_code.robyn import Robyn
        st.write("Successfully imported 'Robyn'.")
    except ImportError as e:
        st.error(f"Failed to import 'Robyn': {str(e)}")
        st.stop()

st.title("Robyn SaaS - Marketing Mix Modeling")
