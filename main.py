import os
import subprocess
import streamlit as st

def install_dependencies():
    """Install dependencies for robyn_code."""
    st.info("Installing dependencies...")
    try:
        subprocess.check_call(["pip", "install", "-r", "robyn_code/requirements.txt"])
        st.success("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to install dependencies: {e}")
        return False
    return True

def main():
    st.title("Robyn SaaS - Marketing Mix Modeling")

    # Install dependencies if not already installed
    if not install_dependencies():
        st.stop()

    # Dynamically import Robyn from robyn_code
    try:
        from robyn_code.robyn import Robyn
        st.success("Successfully imported Robyn!")
    except ImportError as e:
        st.error(f"Failed to import Robyn: {e}")
        st.stop()

    # Initialize Robyn
    try:
        robyn_instance = Robyn(working_dir="robyn_logs")
        st.write("Robyn initialized successfully!")
    except Exception as e:
        st.error(f"Failed to initialize Robyn: {e}")
        st.stop()

    # Add functionality for user interaction
    st.subheader("Run Robyn Model")
    csv_input = st.text_input("Enter CSV input path:")
    alpha = st.slider("Set alpha value:", min_value=0.0, max_value=1.0, value=0.5)

    if st.button("Run Model"):
        if csv_input:
            try:
                result = robyn_instance.run(csv_input=csv_input, alpha=alpha)
                st.success(f"Model run successfully: {result}")
            except Exception as e:
                st.error(f"Error running model: {e}")
        else:
            st.error("Please provide a valid CSV input path.")

if __name__ == "__main__":
    main()
