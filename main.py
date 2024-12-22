import os
import streamlit as st
import sys
import subprocess

# Install dependencies if needed
def install_dependencies():
    robyn_requirements_path = os.path.join("robyn_code", "python", "requirements.txt")
    if os.path.exists(robyn_requirements_path):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", robyn_requirements_path])
            st.success("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to install dependencies: {e}")
    else:
        st.error("requirements.txt not found in robyn_code/python.")

# Clone Robyn repo if not already cloned
def clone_robyn_repo():
    if not os.path.exists("robyn_code"):
        try:
            subprocess.check_call([
                "git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
                "https://github.com/facebookexperimental/Robyn.git", "robyn_code"
            ])
            os.chdir("robyn_code")
            subprocess.check_call(["git", "sparse-checkout", "init", "--cone"])
            subprocess.check_call(["git", "sparse-checkout", "set", "python"])
            os.chdir("..")
            st.success("Cloned Robyn repository successfully.")
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to clone Robyn repository: {e}")
    else:
        st.info("Robyn repository already exists.")

# Add robyn_code/python to sys.path
def add_robyn_to_sys_path():
    robyn_path = os.path.join(os.getcwd(), "robyn_code", "python")
    if robyn_path not in sys.path:
        sys.path.append(robyn_path)
        st.info("Added robyn_code/python to sys.path.")
    else:
        st.info("robyn_code/python already in sys.path.")

# Initialize Robyn instance
def initialize_robyn():
    try:
        from robyn import Robyn
        st.success("Robyn imported successfully.")
        if 'robyn_instance' not in st.session_state:
            working_dir = "./robyn_working_dir"
            os.makedirs(working_dir, exist_ok=True)
            st.session_state.robyn_instance = Robyn(working_dir=working_dir)
            st.success("Robyn instance initialized.")
        else:
            st.info("Robyn instance already initialized.")
    except ImportError as e:
        st.error(f"Failed to import Robyn: {e}")

# Main application logic
st.title("Robyn SaaS - Marketing Mix Modeling")

st.header("Setup Robyn Environment")
if st.button("Clone Robyn Repository"):
    clone_robyn_repo()

if st.button("Install Dependencies"):
    install_dependencies()

add_robyn_to_sys_path()

st.header("Initialize Robyn")
if st.button("Initialize Robyn Instance"):
    initialize_robyn()

st.header("Use Robyn")
if 'robyn_instance' in st.session_state:
    st.write("Robyn is ready to use.")
else:
    st.warning("Robyn is not initialized yet.")
