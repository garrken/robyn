import os
import streamlit as st
import sys
import subprocess

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

# Lägg till robyn_code/python till sys.path
python_path = os.path.join(robyn_code_path, "python")
sys.path.append(python_path)

# Importera Robyn
try:
    from robyn import Robyn
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

# Placeholder för framtida interaktioner
st.write("Använd Robyn för att utföra Marketing Mix Modeling.")
