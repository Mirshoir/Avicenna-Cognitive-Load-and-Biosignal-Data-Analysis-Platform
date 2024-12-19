# Avicenna: Cognitive Load Data and biosignal data Analysis and Chatbot Integration

## Overview
The **Avicenna** project is a capstone design initiative aimed at integrating biosignal data analysis with an AI-driven chatbot to provide actionable insights into users' cognitive load and emotional well-being. This repository contains the code, data, and documentation for the dashboard and chatbot components of the project.

---

## Features

### 1. **Dashboard**
- **Real-Time Data Streaming**: 
  - Collects data from Shimmer devices (e.g., GSR, PPG, ECG, EMG).
  - Devices used: 
    - Shimmer 3 GSR+ Unit SR48-2.
    - Shimmer 3 EXG Unit SR47-5-1.
  - Data Channels:
    - GSR: `EChannelType.GSR_RAW`
    - PPG: `EChannelType.INTERNAL_ADC_13`
    - EMG: `EChannelType.EXG_ADS1292R_1_CH1_24BIT`, `EXG_ADS1292R_1_CH2_24BIT`
    - ECG: `EChannelType.EXG_ADS1292R_2_CH1_24BIT`, `EXG_ADS1292R_2_CH2_24BIT`

- **Biosignal Analysis**:
  - Stress detection using GSR.
  - Cognitive load estimation using HRV (PPG and ECG).
  - Muscle activation analysis using EMG.

- **Data Visualization**:
  - Real-time graphs for all biosignals.
  - HRV and cognitive load metrics.

- **Data Export**: Stores collected data in CSV format.

### 2. **Chatbot**
- **Conversational Interface**:
  - Provides feedback based on analyzed data.
  - AI models: Ollama’s Mistral, LLaMA 3.2.
- **User Insights**:
  - Offers suggestions to manage stress and improve cognitive performance.

---

## Installation

### Prerequisites
- Python 3.11+
- Shimmer devices with Bluetooth connectivity

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/avicenna.git
   cd avicenna
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Open the app in your browser using the URL provided by Streamlit.

---

## Usage

### Dashboard
- **Start Streaming**: Connect your Shimmer device via Bluetooth and begin streaming biosignal data.
- **Upload Data**: Analyze pre-recorded CSV files for GSR, PPG, EMG, or ECG data.
- **View Insights**: Real-time metrics and visualizations will appear on the dashboard.

### Chatbot
- **Feedback**: After analysis, the chatbot provides suggestions based on cognitive load and stress levels.

---

## Project Structure
```
📂 avicenna
├── 📂 data                # Sample and collected datasets
├── 📂 images              # Screenshots and visuals
├── 📂 scripts             # Modular analysis scripts
│   ├── gsr_ppg.py         # GSR and PPG analysis
│   ├── emg.py             # EMG analysis
│   └── ecg.py             # ECG analysis
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## Sample Data
| Timestamp           | GSR_Value | PPG_Value | EMG_CH1 | EMG_CH2   | ECG_CH1 | ECG_CH2   |
|---------------------|-----------|-----------|---------|-----------|---------|-----------|
| 2024-12-18 19:29:13| 688       | 1904      | 3093    | -4790837  | 261788  | -4615     |

---

## Contributors
- **Kamran Asad Al Aziz** (Dashboard Development, Data Analysis)
- **Mirshoir** (Chatbot Integration)

---

## References
1. [Shimmer Sensing Documentation](https://www.shimmersensing.com/documentation)
2. [NeuroKit2](https://neurokit2.readthedocs.io/)
3. [Streamlit Framework](https://docs.streamlit.io/)

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
