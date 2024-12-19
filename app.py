# app.py

import streamlit as st
from ecg import ecg_app
from emg import emg_app
from gsr_ppg import gsr_ppg_app  # Correct import

st.set_page_config(
    page_title="Biosignal Data Analysis App",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", [
    "Home",
    "ECG Analysis",
    "EMG Analysis",
    "GSR/PPG Analysis"
])

if selection == "Home":
    st.title("Welcome to the Cognitive Load - Biosignal Data Analysis App")
    st.write("""
    This app allows you to analyze ECG, EMG, GSR, and PPG data for various physiological insights.
    Use the menu on the left to navigate between different analyses and tools.
    """)
elif selection == "ECG Analysis":
    ecg_app()
elif selection == "EMG Analysis":
    emg_app()
elif selection == "GSR/PPG Analysis":
    gsr_ppg_app()
