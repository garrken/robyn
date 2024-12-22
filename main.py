import os
import subprocess
import streamlit as st

# Funktion för att klona Robyn-repot och förbereda koden
def setup_robyn_code():
    repo_url = "https://github.com/facebookexperimental/Robyn.git"
    robyn_code_path = os.path.join(os.getcwd(), "robyn_code")
    python_path = os.path.join(robyn_code_path, "python")

    # Kontrollera om robyn_code redan finns
    if not os.path.exists(robyn_code_path):
        st.write("Cloning Robyn repository...")
        try:
            subprocess.check_call(["git", "clone", repo_url, "robyn_code"])
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to clone repository: {e}")
            return False

    # Kontrollera om python-mappen finns i robyn_code
    if not os.path.exists(python_path):
        st.error(f"'python' directory not found in {robyn_code_path}. Please check the repository structure.")
        return False

    st.write("Robyn repository cloned successfully.")
    return True

# Funktion för att installera beroenden
def install_dependencies():
    requirements_path = os.path.join(os.getcwd(), "robyn_code", "python", "requirements.txt")

    if not os.path.exists(requirements_path):
        st.error("requirements.txt not found in robyn_code/python.")
        return False

    st.write("Installing dependencies...")
    try:
        subprocess.check_call(["pip", "install", "-r", requirements_path])
        st.write("Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to install dependencies: {e}")
        return False

# Hämta och konfigurera Robyn
if setup_robyn_code() and install_dependencies():
    try:
        # Importera Robyn från den klonade koden
        from robyn.robyn import Robyn
        st.write("Successfully imported Robyn.")
        st.title("Robyn SaaS - Marketing Mix Modeling")

        # Exempel på Robyn-användning
        working_dir = "./robyn_working_dir"
        os.makedirs(working_dir, exist_ok=True)
        robyn_instance = Robyn(working_dir=working_dir)
        st.write("Robyn instance created successfully.")

    except ImportError as e:
        st.error(f"Failed to import Robyn: {e}")
else:
    st.stop()
