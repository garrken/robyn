import os
import requests
import zipfile
import streamlit as st
import pandas as pd

# Fullständig inaktivering av filövervakning
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
            st.write("robyn_code contents:")
            st.write(os.listdir("robyn_code"))
        else:
            st.error("Failed to extract robyn_code correctly!")

        os.remove(zip_path)

# Ladda ner Robyns Python-kod om den inte redan finns
with st.spinner("Setting up Robyn, please wait..."):
    download_and_prepare_robyn()

# Försök importera klassen Robyn dynamiskt
try:
    from robyn_code.robyn import robyn as Robyn
    st.write("Successfully imported 'robyn' as 'Robyn'.")
except ImportError as e:
    try:
        from robyn_code.robyn import Robyn
        st.write("Successfully imported 'Robyn'.")
    except ImportError:
        st.error(f"Failed to import 'Robyn': {str(e)}")
        st.stop()

# Streamlit-applikationen börjar här
st.title("Robyn SaaS - Marketing Mix Modeling")

# Sidebar för inställningar
st.sidebar.header("Settings")

# File uploader för data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Läs och visa rådata
    raw_data = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(raw_data.head())

    # Förbered data
    def prepare_data(data):
        """Förbered data för Robyn-modellering."""
        data.fillna(0, inplace=True)
        for col in data.select_dtypes(include=["float", "int"]).columns:
            data[col] = data[col].clip(lower=0)
        return data

    prepared_data = prepare_data(raw_data)
    st.subheader("Prepared Data")
    st.dataframe(prepared_data.head())

    # Kör Robyn-modellen
    if st.button("Run Robyn Model"):
        temp_csv_path = "temp_data.csv"
        prepared_data.to_csv(temp_csv_path, index=False)

        robyn_instance = Robyn(csv_input=temp_csv_path, alpha=0.5)
        robyn_instance.run()

        st.success("Robyn Model executed successfully!")

    # Optimeringsinställningar
    st.sidebar.subheader("Optimization Settings")
    goal = st.sidebar.radio("Optimization Goal", ["Maximize ROAS", "Maximize Conversions"])
    budget = st.sidebar.slider("Total Budget (SEK)", 10000, 100000, 50000)

    if st.sidebar.button("Optimize Media Mix"):
        # Exempel på optimeringslogik
        optimized_mix = {
            "Facebook": budget * 0.4,
            "Google Ads": budget * 0.3,
            "Instagram": budget * 0.2,
            "TikTok": budget * 0.1,
        }
        st.subheader("Optimized Media Mix")
        st.json(optimized_mix)
