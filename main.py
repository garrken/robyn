import os
import subprocess
import streamlit as st

# Funktion för att klona och installera Robyn
def install_robyn():
    """Klonar och installerar Robyn från GitHub."""
    repo_url = "https://github.com/facebookexperimental/Robyn.git"
    target_dir = "Robyn"

    if not os.path.exists(target_dir):
        st.info("Cloning Robyn repository...")
        result = subprocess.run(
            ["git", "clone", repo_url, target_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            st.error(f"Failed to clone Robyn repository: {result.stderr.decode()}")
            return

    st.info("Installing Robyn as a Python module...")
    result = subprocess.run(
        ["pip", "install", "-e", os.path.join(target_dir, "python")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        st.error(f"Failed to install Robyn: {result.stderr.decode()}")
    else:
        st.success("Robyn installed successfully!")

# Kör installation av Robyn
with st.spinner("Setting up Robyn, please wait..."):
    install_robyn()

# Importera Robyn efter installation
try:
    from robyn import Robyn
    st.success("Robyn imported successfully!")
except ImportError as e:
    st.error(f"Failed to import Robyn: {str(e)}")

# Initiera applikationens huvudgränssnitt
st.title("Robyn SaaS - Marketing Mix Modeling")

# Skapa arbetskatalog
working_dir = "robyn_output"
os.makedirs(working_dir, exist_ok=True)

# Skapa en Robyn-instans
try:
    robyn_instance = Robyn(working_dir=working_dir)
    st.success("Robyn initialized successfully!")
except Exception as e:
    st.error(f"Failed to initialize Robyn: {str(e)}")

# Användargränssnitt för att köra Robyn-modellen
uploaded_file = st.file_uploader("Upload your MMM data CSV file", type=["csv"])

if uploaded_file:
    st.subheader("Uploaded File")
    st.dataframe(pd.read_csv(uploaded_file).head())

    if st.button("Run Robyn Model"):
        # Exempel: använd Robyn-instansen
        try:
            st.info("Running Robyn...")
            # Lägg till körlogik här baserat på Robyn-instansen
            st.success("Robyn model run completed!")
        except Exception as e:
            st.error(f"Failed to run Robyn model: {str(e)}")
