import os
import csv
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import neurokit2 as nk
import matplotlib.pyplot as plt
from serial import Serial
from pyshimmer import ShimmerBluetooth, DEFAULT_BAUDRATE, DataPacket, EChannelType
from serial.tools import list_ports
from queue import Queue

# ------------------------------------------
# Global Variables
# ------------------------------------------
DATA_STORAGE_DIR = 'uploaded_data_gsr_ppg'
if not os.path.exists(DATA_STORAGE_DIR):
    os.makedirs(DATA_STORAGE_DIR)

data_queue = Queue()
stress_events = []  # Store stress detection times

GSR_THRESHOLD = 35000  # Hypothetical GSR threshold for stress detection
ppg_sampling_rate = 1000  # Hz

# ------------------------------------------
# Functions
# ------------------------------------------

def list_available_ports():
    """List available COM ports."""
    ports = list_ports.comports()
    return [port.device for port in ports]

def handler(pkt: DataPacket, csv_writer):
    """Handle incoming data and write to CSV."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        gsr_value = pkt[EChannelType.GSR_RAW]
        ppg_value = pkt[EChannelType.INTERNAL_ADC_13]
        csv_writer.writerow([timestamp, gsr_value, ppg_value])
        data_queue.put((timestamp, gsr_value, ppg_value))
    except KeyError:
        pass

def run_streaming(username, selected_port):
    """Run live streaming from the device."""
    csv_file_path = os.path.join(DATA_STORAGE_DIR, f"{username}_live_data.csv")
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Timestamp", "GSR_Value", "PPG_Value"])

        try:
            serial_conn = Serial(selected_port, DEFAULT_BAUDRATE)
            shimmer = ShimmerBluetooth(serial_conn)
            shimmer.initialize()
            shimmer.start_streaming()
            shimmer.add_stream_callback(lambda pkt: handler(pkt, csv_writer))
            st.info("Streaming... Click 'Stop Streaming' to stop.")
            while not st.session_state.get('stop_streaming', False):
                pass
            shimmer.stop_streaming()
            shimmer.shutdown()
        except Exception as e:
            st.error(f"Error: {e}")
    return csv_file_path

def process_data(data):
    """Process GSR and PPG data for stress detection and HRV features."""
    st.subheader("GSR and PPG Analysis")

    # Extract GSR and PPG data
    gsr_values = data['GSR_Value']
    ppg_values = data['PPG_Value']
    timestamps = pd.to_datetime(data['Timestamp'])

    # Plot GSR Signal
    st.subheader("GSR Signal")
    fig, ax = plt.subplots()
    ax.plot(timestamps, gsr_values, color="blue")
    ax.set_title("GSR Signal")
    ax.set_xlabel("Time")
    ax.set_ylabel("GSR Value")
    st.pyplot(fig)

    # Plot PPG Signal
    st.subheader("PPG Signal")
    fig, ax = plt.subplots()
    ax.plot(timestamps, ppg_values, color="red")
    ax.set_title("PPG Signal")
    ax.set_xlabel("Time")
    ax.set_ylabel("PPG Value")
    st.pyplot(fig)

    # Stress Analysis based on GSR
    stress_count = sum(1 for gsr in gsr_values if gsr > GSR_THRESHOLD)
    stress_percentage = (stress_count / len(gsr_values)) * 100
    st.subheader("Stress Analysis")
    st.write(f"**Stress Detected in {stress_percentage:.2f}% of the session.**")
    if stress_percentage > 30:
        st.error("High Stress Detected!")
    else:
        st.success("Relaxed State")

    # HRV Feature Extraction from PPG
    st.subheader("HRV Analysis from PPG")
    ppg_cleaned = nk.ppg_clean(ppg_values, sampling_rate=ppg_sampling_rate)
    peaks = nk.ppg_findpeaks(ppg_cleaned, sampling_rate=ppg_sampling_rate)
    r_peaks = peaks['PPG_Peaks']

    if len(r_peaks) > 1:
        rr_intervals = np.diff(r_peaks) * (1000 / ppg_sampling_rate)  # Convert to ms
        sdnn = np.std(rr_intervals)  # Standard deviation of RR intervals
        st.write(f"**SDNN (HRV): {sdnn:.2f} ms**")
        st.line_chart(pd.DataFrame({"RR Intervals (ms)": rr_intervals}))
    else:
        st.warning("Not enough PPG peaks to calculate HRV.")

def gsr_ppg_app():
    """Main Streamlit application."""
    st.title("GSR and PPG Data Analysis with Stress Detection and HRV")

    # Sidebar for Live Streaming Options
    st.sidebar.header("Live Streaming Options")
    username = st.sidebar.text_input("Enter your name:", "user")
    ports = list_available_ports()
    selected_port = st.sidebar.selectbox("Select COM port:", ports)

    if 'stop_streaming' not in st.session_state:
        st.session_state['stop_streaming'] = False

    col1, col2 = st.sidebar.columns(2)
    if col1.button("Start Streaming"):
        st.session_state['stop_streaming'] = False
        csv_file_path = run_streaming(username, selected_port)
        st.success(f"Data saved to: {csv_file_path}")

    if col2.button("Stop Streaming"):
        st.session_state['stop_streaming'] = True

    # Upload Existing Data
    st.header("Upload and Analyze Existing Data")
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        if "GSR_Value" in data.columns and "PPG_Value" in data.columns:
            process_data(data)
        else:
            st.error("The uploaded file does not have 'GSR_Value' or 'PPG_Value' columns.")
    else:
        st.info("Upload a file to analyze GSR and PPG data.")

if __name__ == "__main__":
    gsr_ppg_app()
