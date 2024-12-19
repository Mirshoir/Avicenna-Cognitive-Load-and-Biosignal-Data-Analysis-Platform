import os
import time
import csv
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
import streamlit as st
from sklearn.preprocessing import StandardScaler
from serial import Serial
from pyshimmer import ShimmerBluetooth, DEFAULT_BAUDRATE, DataPacket, EChannelType
from serial.tools import list_ports
from queue import Queue

# ------------------------------------------
# Global Variables and Setup
# ------------------------------------------
DATA_STORAGE_DIR = 'uploaded_data_emg'
if not os.path.exists(DATA_STORAGE_DIR):
    os.makedirs(DATA_STORAGE_DIR)

EMG_SAMPLING_RATE = 1000  # Hz
data_queue = Queue()

# ------------------------------------------
# Functions
# ------------------------------------------

def list_available_ports():
    """List and return all available COM ports."""
    ports = list_ports.comports()
    return [port.device for port in ports]

def handler(pkt: DataPacket, csv_writer):
    """Handle incoming data packets and save them to a CSV."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emg_ch1 = pkt[EChannelType.EXG_ADS1292R_1_CH1_24BIT]
        emg_ch2 = pkt[EChannelType.EXG_ADS1292R_1_CH2_24BIT]
        csv_writer.writerow([timestamp, emg_ch1, emg_ch2])
        data_queue.put((timestamp, emg_ch1, emg_ch2))
    except KeyError:
        pass

def run_streaming(username, selected_port):
    """Start live streaming from the device."""
    csv_file_path = os.path.join(DATA_STORAGE_DIR, f"{username}_emg_data.csv")
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Timestamp", "EMG_CH1", "EMG_CH2"])

        try:
            serial_conn = Serial(selected_port, DEFAULT_BAUDRATE)
            shimmer = ShimmerBluetooth(serial_conn)
            shimmer.initialize()
            shimmer.start_streaming()
            shimmer.add_stream_callback(lambda pkt: handler(pkt, csv_writer))

            st.info("Streaming... Click 'Stop Streaming' to stop.")
            while not st.session_state.get('stop_streaming', False):
                time.sleep(1)
            shimmer.stop_streaming()
            shimmer.shutdown()
        except Exception as e:
            st.error(f"Error: {e}")
    return csv_file_path

def process_data(data):
    """Process and analyze EMG data to identify stress."""
    st.subheader("EMG Analysis")

    # Combine EMG channels
    emg_signal = data[['EMG_CH1', 'EMG_CH2']].mean(axis=1)

    # Clean the EMG signal
    emg_cleaned = nk.emg_clean(emg_signal, sampling_rate=EMG_SAMPLING_RATE)

    # Compute EMG envelope (amplitude)
    emg_amplitude = nk.emg_amplitude(emg_cleaned)

    # Plot EMG signal
    st.subheader("Raw EMG Signal")
    fig, ax = plt.subplots()
    ax.plot(emg_signal, label="Raw EMG", color="blue", alpha=0.6)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    st.pyplot(fig)

    # Plot EMG envelope
    st.subheader("EMG Envelope")
    fig, ax = plt.subplots()
    ax.plot(emg_amplitude, label="EMG Envelope", color="red")
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    st.pyplot(fig)

    # Stress Analysis
    activation_threshold = emg_amplitude.mean() + emg_amplitude.std()
    high_activation = emg_amplitude > activation_threshold
    high_activation_percentage = np.mean(high_activation) * 100

    st.subheader("Stress Analysis")
    st.write(f"**High Activation Threshold**: {activation_threshold:.2f}")
    st.write(f"**Percentage of High Activation**: {high_activation_percentage:.2f}%")

    if high_activation_percentage > 30:
        st.error("High Stress Detected!")
    else:
        st.success("Low Stress Levels")

def emg_app():
    """Streamlit app for EMG data collection and stress analysis."""
    st.title("EMG Data Analysis and Stress Detection")

    # Sidebar for live streaming options
    st.sidebar.header("Live Streaming Options")
    username = st.sidebar.text_input("Enter your name:", "user")
    ports = list_available_ports()
    selected_port = st.sidebar.selectbox("Select COM port:", ports)

    if 'stop_streaming' not in st.session_state:
        st.session_state['stop_streaming'] = False

    start_button = st.sidebar.button("Start Streaming")
    stop_button = st.sidebar.button("Stop Streaming")

    if start_button:
        st.session_state['stop_streaming'] = False
        csv_file_path = run_streaming(username, selected_port)
        st.success(f"Data saved to: {csv_file_path}")

    if stop_button:
        st.session_state['stop_streaming'] = True

    # Upload and analyze existing data
    st.header("Upload and Analyze Data")
    uploaded_file = st.file_uploader("Upload EMG CSV file", type="csv")

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Sample:", data.head())
        process_data(data)

if __name__ == "__main__":
    emg_app()
