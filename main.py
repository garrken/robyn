import os
import sys
import subprocess
import streamlit as st

# Klona Robyn-repositoryt om det inte redan finns
robyn_code_path = os.path.join(os.getcwd(), "robyn_code")
if not os.path.exists(robyn_code_path):
    st.info("Cloning Robyn repository...")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", "https://github.com/facebookexperimental/Robyn.git", "robyn_code"],
            check=True,
        )
        subprocess.run(["git", "-C", "robyn_code", "sparse-checkout", "set", "python"], check=True)
        st.success("Successfully cloned Robyn repository.")
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to clone Robyn repository: {e}")
        st.stop()

# Kontrollera om /python-mappen finns, annars skapa den
python_folder = os.path.join(robyn_code_path, "python")
if not os.path.exists(python_folder):
    os.makedirs(python_folder)

# Kontrollera om requirements.txt finns
requirements_file = os.path.join(python_folder, "requirements.txt")
if not os.path.exists(requirements_file):
    st.error("requirements.txt not found in robyn_code/python folder.")
    st.stop()

# Lägg till robyn_code/python till sys.path
if python_folder not in sys.path:
    sys.path.append(python_folder)

# Installera beroenden, ignorera rpy2
try:
    st.info("Installing dependencies...")
    with open(requirements_file, "r") as req_file:
        requirements = req_file.readlines()
    requirements = [req.strip() for req in requirements if not req.startswith("rpy2")]
    with open("filtered_requirements.txt", "w") as filtered_req:
        filtered_req.write("\n".join(requirements))
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "filtered_requirements.txt"])
    st.success("Dependencies installed successfully (excluding rpy2).")
except subprocess.CalledProcessError as e:
    st.error(f"Dependency installation failed: {e}")
    st.stop()

# Importera Robyn
try:
    from robyn.robyn import Robyn
    st.success("Successfully imported Robyn.")
except ImportError as e:
    st.error(f"Failed to import Robyn: {e}")
    st.stop()

st.title("Robyn SaaS - Marketing Mix Modeling")

# Exempel på användning av Robyn
if 'robyn_instance' not in st.session_state:
    working_dir = "./robyn_working_dir"
    os.makedirs(working_dir, exist_ok=True)
    try:
        st.session_state.robyn_instance = Robyn(working_dir=working_dir)
        st.success("Robyn instance created.")
    except Exception as e:
        st.error(f"Failed to create Robyn instance: {e}")
else:
    st.info("Robyn instance is already created.")

st.write("Använd Robyn för att utföra Marketing Mix Modeling.")
