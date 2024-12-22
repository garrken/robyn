import os
import subprocess
import streamlit as st


def install_robyn():
    """Install Robyn with dependencies, excluding rpy2."""
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
            return False

    st.info("Installing Robyn dependencies...")
    try:
        # Installera beroenden från uppdaterad requirements.txt
        subprocess.check_call(["pip", "install", "-r", os.path.join(target_dir, "python", "requirements.txt")])

        # Installera Robyn utan att använda `rpy2`
        subprocess.check_call(["pip", "install", "--no-deps", os.path.join(target_dir, "python")])
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to install Robyn dependencies: {e}")
        return False

    st.success("Robyn installed successfully!")
    return True


def main():
    st.title("Robyn SaaS - Marketing Mix Modeling")

    # Installera Robyn om det inte redan finns
    if not os.path.exists("Robyn/python") or not os.path.exists("Robyn/python/robyn"):
        if not install_robyn():
            st.error("Failed to set up Robyn. Please check the logs.")
            return

    # Dynamiskt importera Robyn
    try:
        from Robyn.python.robyn import Robyn
        st.success("Successfully imported Robyn!")
    except ImportError as e:
        st.error(f"Failed to import Robyn: {e}")
        return

    # Använd Robyn
    try:
        robyn_instance = Robyn(working_dir="robyn_logs")
        robyn_instance.initialize(
            mmm_data="path_to_mmm_data.csv",
            holidays_data="path_to_holidays.csv",
            hyperparameters="path_to_hyperparameters.csv",
        )
        st.write("Robyn initialized successfully!")
    except Exception as e:
        st.error(f"Failed to initialize Robyn: {e}")
        return

    st.write("Robyn is ready to use!")


if __name__ == "__main__":
    main()
