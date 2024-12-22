import streamlit as st
import os
import subprocess
from pathlib import Path

# Function to check and install dependencies
def install_dependencies():
    """Install required dependencies for Robyn."""
    try:
        requirements_path = Path("robyn_code/requirements.txt")
        if requirements_path.exists():
            subprocess.check_call([
                "pip", "install", "-r", str(requirements_path)
            ])
        else:
            st.error("requirements.txt not found in robyn_code folder.")
    except Exception as e:
        st.error(f"Failed to install dependencies: {e}")

# Function to dynamically import Robyn
def import_robyn():
    """Import Robyn module dynamically."""
    try:
        from robyn_code.robyn import Robyn
        st.success("Successfully imported Robyn!")
        return Robyn
    except ModuleNotFoundError as e:
        st.error(f"Failed to import Robyn: {e}")
        return None

# Streamlit app starts here
st.title("Robyn SaaS - Marketing Mix Modeling")

# Install dependencies
st.write("Installing dependencies...")
install_dependencies()

# Check if robyn_code folder exists
robyn_code_path = Path("robyn_code")
if robyn_code_path.exists():
    st.write("robyn_code directory found.")
    Robyn = import_robyn()

    if Robyn:
        # Initialize Robyn
        try:
            working_dir = "./robyn_outputs"
            robyn_instance = Robyn(working_dir)
            st.success("Robyn instance created successfully!")
        except Exception as e:
            st.error(f"Failed to initialize Robyn: {e}")
else:
    st.error("robyn_code directory does not exist. Please ensure the directory is present.")
