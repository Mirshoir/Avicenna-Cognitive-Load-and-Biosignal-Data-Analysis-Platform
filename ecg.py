import streamlit as st
import os
import time
import csv
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
from sklearn.preprocessing import StandardScaler
from serial import Serial
from pyshimmer import ShimmerBluetooth, DEFAULT_BAUDRATE, DataPacket, EChannelType
from serial.tools import list_ports
from queue import Queue
import threading

# Suppress warnings from matplotlib
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

# ------------------------------------------
# Global Variables and Setup
# ------------------------------------------

ECG_SAMPLING_RATE = 1000  # in Hz
DATA_STORAGE_DIR = 'uploaded_data_ecg'

if not os.path.exists(DATA_STORAGE_DIR):
    os.makedirs(DATA_STORAGE_DIR)

if 'is_collecting' not in st.session_state:
    st.session_state['is_collecting'] = False

if 'stop_event' not in st.session_state:
    st.session_state['stop_event'] = None

if 'collection_thread' not in st.session_state:
    st.session_state['collection_thread'] = None

# ------------------------------------------
# Functions
# ------------------------------------------

def list_available_ports():
    """List and return all available COM ports."""
    ports = list_ports.comports()
    return [port.device for port in ports]

def ecg_handler(pkt: DataPacket, csv_writer):
    """Handle incoming ECG data packets."""
    try:
        ecg_ch1 = pkt[EChannelType.EXG_ADS1292R_1_CH1_24BIT]
        ecg_ch2 = pkt[EChannelType.EXG_ADS1292R_1_CH2_24BIT]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        csv_writer.writerow([timestamp, ecg_ch1, ecg_ch2])
    except KeyError as e:
        print(f"KeyError: {e}")

def collect_ecg_data(shimmer, csv_file_path, stop_event):
    """Collect ECG data from the Shimmer device and save to a CSV file."""
    try:
        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Timestamp", "ECG_CH1", "ECG_CH2"])
            shimmer.add_stream_callback(lambda pkt: ecg_handler(pkt, csv_writer))
            shimmer.start_streaming()

            while not stop_event.is_set():
                time.sleep(0.1)

            shimmer.stop_streaming()
    except Exception as e:
        st.error(f"Error during data collection: {e}")
    finally:
        shimmer.shutdown()

def connect_shimmer(selected_port):
    """Connect to a Shimmer device on the specified COM port."""
    try:
        serial_conn = Serial(selected_port, DEFAULT_BAUDRATE, timeout=None)
        shimmer = ShimmerBluetooth(serial_conn)
        shimmer.initialize()
        return shimmer
    except Exception as e:
        st.error(f"Failed to connect to Shimmer device: {e}")
        return None

def analyze_ecg_data(ecg_data):
    """Perform ECG data analysis with cognitive load estimation."""
    st.header("ECG Data Analysis and Cognitive Load Estimation")

    if 'ECG_CH1' not in ecg_data.columns or 'ECG_CH2' not in ecg_data.columns:
        st.error("Uploaded data does not have the required columns: 'ECG_CH1' and 'ECG_CH2'")
        return

    ecg_signal = ecg_data['ECG_CH1'].values
    ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate=ECG_SAMPLING_RATE)

    st.line_chart(ecg_cleaned)

    try:
        ecg_peaks, info = nk.ecg_peaks(ecg_cleaned, sampling_rate=ECG_SAMPLING_RATE)
        r_peak_indices = ecg_peaks['ECG_R_Peaks']

        # Plot cleaned signal with R-peaks
        fig, ax = plt.subplots(figsize=(10, 4))
        time_axis = np.arange(len(ecg_cleaned)) / ECG_SAMPLING_RATE
        ax.plot(time_axis, ecg_cleaned, label='Cleaned ECG Signal')
        ax.scatter(time_axis[r_peak_indices], ecg_cleaned[r_peak_indices], color='red', label='R-peaks')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.legend()
        st.pyplot(fig)

        # Compute HRV metrics
        hrv_metrics = nk.hrv(ecg_peaks, sampling_rate=ECG_SAMPLING_RATE, show=False)
        st.subheader("HRV Metrics")
        st.write(hrv_metrics)

        # Cognitive Load Estimation
        if 'HRV_SDNN' in hrv_metrics.columns and 'HRV_LFHF' in hrv_metrics.columns:
            sdnn = hrv_metrics['HRV_SDNN'].iloc[0]
            lf_hf = hrv_metrics['HRV_LFHF'].iloc[0]

            st.subheader("Cognitive Load Estimation")
            st.write(f"**SDNN**: {sdnn:.2f} ms")
            st.write(f"**LF/HF Ratio**: {lf_hf:.2f}")

            if sdnn < 50 or lf_hf > 2.0:
                st.error("High Cognitive Load Detected")
            elif sdnn > 100 and lf_hf < 1.0:
                st.success("Low Cognitive Load")
            else:
                st.warning("Moderate Cognitive Load")

    except Exception as e:
        st.error(f"Error analyzing ECG data: {e}")

# ------------------------------------------
# Streamlit Application
# ------------------------------------------

def ecg_app():
    """Streamlit app for ECG data collection and analysis."""
    st.title("ECG Data Collection and Analysis")

    # Select COM port and start streaming
    st.sidebar.header("Data Collection")
    selected_port = st.sidebar.selectbox("Select COM Port", list_available_ports())
    start_button = st.sidebar.button("Start Streaming")
    stop_button = st.sidebar.button("Stop Streaming")

    if start_button and not st.session_state['is_collecting']:
        if selected_port:
            st.session_state['stop_event'] = threading.Event()
            csv_file_path = os.path.join(DATA_STORAGE_DIR, f"ecg_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            shimmer = connect_shimmer(selected_port)
            if shimmer:
                st.session_state['collection_thread'] = threading.Thread(
                    target=collect_ecg_data, args=(shimmer, csv_file_path, st.session_state['stop_event'])
                )
                st.session_state['collection_thread'].start()
                st.session_state['is_collecting'] = True
                st.success("Started data collection. Data will be saved in the 'uploaded_data_ecg' folder.")
        else:
            st.error("Please select a COM port.")

    if stop_button and st.session_state['is_collecting']:
        st.session_state['stop_event'].set()
        st.session_state['collection_thread'].join()
        st.session_state['is_collecting'] = False
        st.success("Stopped data collection.")

    st.markdown("---")

    # Upload and analyze data
    st.header("Upload and Analyze Data")
    uploaded_file = st.file_uploader("Upload ECG Data CSV", type="csv")
    if uploaded_file:
        try:
            ecg_data = pd.read_csv(uploaded_file)
            analyze_ecg_data(ecg_data)
        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")

if __name__ == "__main__":
    ecg_app()
