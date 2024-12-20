# Avicenna: Cognitive Load Data Analysis and Chatbot Integration

## Sejong University - Capstone Design Project Report

### Authors
- **Kamran Asad Al Aziz** (Student ID: 20012763)
- **Mirshoir** (Student ID: 21012963)

### Professors
- **Rajendra Dhakal**
- **Abolghasem Sadeghi-Niaraki**

---

## Table of Contents
1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Dashboard Development](#dashboard-development)
4. [Chatbot Integration](#chatbot-integration)
5. [Data Analysis](#data-analysis)
    - [GSR and PPG Analysis](#gsr-and-ppg-analysis)
    - [EMG Analysis](#emg-analysis)
    - [ECG Analysis](#ecg-analysis)
6. [System Implementation](#system-implementation)
7. [Results and Visualization](#results-and-visualization)
8. [Future Work](#future-work)
9. [Conclusion](#conclusion)
10. [References](#references)

---

## Introduction

The **Avicenna project** integrates biosignal data analysis with an AI-driven chatbot to provide insights into users' cognitive load and emotional well-being. The project comprises two main components: a **dashboard** for real-time data collection and analysis, and a **chatbot** for personalized feedback. This report primarily focuses on the dashboard development and data analysis conducted by **Kamran Asad Al Aziz**, while briefly touching upon the chatbot integration by **Mirshoir**.

---

## Project Overview

### Objectives
1. **Develop a dashboard** for real-time data collection using Shimmer devices.
2. **Analyze biosignal data** (GSR, PPG, ECG, and EMG) to assess cognitive load and stress.
3. **Integrate a chatbot** to provide actionable recommendations based on analyzed data.

### Scope
- Real-time and uploaded data analysis for biosignals.
- Visualization of key metrics and trends.
- Cognitive load estimation and stress detection.

---

## Dashboard Development

### Tools and Technologies
- **Streamlit**: Framework for building interactive dashboards.
- **PyShimmer**: Unofficial Python API for Shimmer devices.
- **NeuroKit2**: Library for biosignal processing and analysis.
- **Python**: Core programming language for data handling.

### Features
- **Real-Time Data Streaming**:
  - Devices: Shimmer 3 GSR+ Unit SR48-2, Shimmer 3 EXG Unit SR47-5-1.
  - Channels:
    - GSR: `EChannelType.GSR_RAW`
    - PPG: `EChannelType.INTERNAL_ADC_13`
    - EMG: `EChannelType.EXG_ADS1292R_1_CH1_24BIT`, `EXG_ADS1292R_1_CH2_24BIT`
    - ECG: `EChannelType.EXG_ADS1292R_2_CH1_24BIT`, `EXG_ADS1292R_2_CH2_24BIT`
- **Analysis Modules**:
  - Stress detection from GSR.
  - HRV computation from PPG and ECG.
  - Muscle activation analysis from EMG.
- **Visualization**:
  - Time-series plots for biosignals.
  - Real-time graphs and insights.
- **Data Storage**:
  - All data saved as CSV for future analysis.

---

## Chatbot Integration

**Chatbot.py**:

The chatbot component of the Avicenna project was designed to provide personalized insights and recommendations based on the user’s cognitive load and stress levels. Below are the functionalities of the `chatbot.py` module:

### Features
1. **Conversational Interface**:
   - The chatbot interacts with users, understanding their concerns and providing relevant feedback.
2. **Integration with Dashboard**:
   - Fetches cognitive load metrics and stress analysis results from the dashboard.
3. **AI Models Used**:
   - Leveraged LLaMA and Ollama's Mistral models for robust conversational capabilities.
4. **Personalized Feedback**:
   - Offers tailored advice on stress management and improving focus.

### Technologies Used
- **Streamlit** for seamless integration with the dashboard.
- **Custom NLP Models** for accurate sentiment analysis and response generation.
- **PyTorch** for deploying the LLaMA model.

Sample Chatbot Functionality Code Snippet:
```python
import streamlit as st

def chatbot_interface():
    st.title("Avicenna Chatbot")
    user_input = st.text_input("How can I assist you today?")
    if user_input:
        response = generate_response(user_input)
        st.write("Chatbot:", response)

def generate_response(user_input):
    # Placeholder for AI model integration
    return "I am here to assist you with your cognitive load insights."

if __name__ == "__main__":
    chatbot_interface()
```

---

## Data Analysis

### GSR and PPG Analysis
- **Stress Detection**:
  - GSR thresholds used to identify periods of stress.
- **HRV Metrics**:
  - Computed from PPG peaks.
  - Metrics include SDNN and LF/HF ratio for cognitive load estimation.

### EMG Analysis
- **Muscle Activation**:
  - High muscle activation detected through envelope analysis.
- **Key Outputs**:
  - Percentage of time under high activation.
  - Visualization of amplitude trends.

### ECG Analysis
- **HRV Features**:
  - LF/HF ratio for cognitive load estimation.
  - Stress levels determined from HRV metrics.
- **R-Peak Detection**:
  - Accurate identification of cardiac cycles for analysis.

---

## System Implementation

### Code Structure
- **`app.py`**: Navigation and integration of all modules.
- **`gsr_ppg.py`**: Handles GSR and PPG analysis.
- **`ecg.py`**: Focused on ECG analysis.
- **`emg.py`**: Manages EMG data collection and processing.
- **`chatbot.py`**: Implements chatbot functionality.

---

## Results and Visualization

### Sample Data
#### GSR/PPG:
| Timestamp           | GSR_Value | PPG_Value |
|---------------------|-----------|-----------|
| 2024-12-18 19:29:13| 688       | 1904      |
| 2024-12-18 19:29:14| 688       | 1903      |

#### EMG:
| Timestamp           | EMG_CH1 | EMG_CH2   |
|---------------------|---------|-----------|
| 2024-12-19 09:32:59| 3093    | -4790837  |
| 2024-12-19 09:32:59| 2583    | -4794430  |

#### ECG:
| Timestamp           | ECG_CH1 | ECG_CH2   |
|---------------------|---------|-----------|
| 2024-12-19 08:14:55| 261788  | -4615     |
| 2024-12-19 08:14:56| 261309  | -4727     |

---

## Future Work

1. **Enhance Stress Analysis**:
   - Refine thresholds and algorithms for stress detection.
2. **Expand Cognitive Load Metrics**:
   - Add new features for comprehensive cognitive load assessment.
3. **Mobile Integration**:
   - Develop a companion app for on-the-go analysis.

---

## Conclusion

The Avicenna project bridges biosignal data analysis and conversational AI to provide users with actionable insights into their cognitive and emotional well-being. The modular design ensures scalability, while the integration of real-time data analysis and chatbot functionality delivers a holistic user experience.

---

## References

1. Shimmer Sensing, "Shimmer3 GSR+ User Manual," https://www.shimmersensing.com/documentation.
2. NeuroKit2 Documentation, "NeuroKit2: An Open-Source Python Toolbox for Physiological Signal Processing," https://neurokit2.readthedocs.io/.
3. Python Software Foundation, "Python 3.11 Documentation," https://docs.python.org/3/.
4. Streamlit, "Streamlit Framework Documentation," https://docs.streamlit.io/.
5. Pyshimmer, “Shimmer unofficial API,” https://github.com/seemoo-lab/pyshimmer.


   # Project  and Developer Documentation for Avicenna chatbot

## **Avicenna: Cognitive Load and Biosignal Data Analysis Platform**

### **Introduction**

The Avicenna platform is a Streamlit-based application designed to analyze biosignal data (ECG, EMG, GSR/PPG), evaluate cognitive load, and provide personalized recommendations using an advanced conversational AI chatbot. This document serves as a comprehensive project proposal and developer guide to ensure clarity for future development and scalability.

The integration of biosignal data analysis and conversational AI in a single platform allows users to gain actionable insights into their physiological and emotional states, offering recommendations for stress management and cognitive well-being.

---

### **Project Objectives**

1. To provide a unified platform for analyzing ECG, EMG, and GSR/PPG data.
2. To estimate cognitive load and emotional states using biosignal data.
3. To assist users via a conversational chatbot, delivering professional advice based on their physiological state.
4. To create a scalable and modular system for future extensions.
5. To simplify user interactions through a clean, Streamlit-based interface.

---

### **System Overview**

#### **Core Components**

1. **Streamlit Dashboard**
   - Serves as the frontend for the application.
   - Provides navigation across analysis modules and the chatbot.
2. **Data Analysis Modules**
   - Individual modules for ECG, EMG, and GSR/PPG analysis.
   - Processes uploaded `.csv` files and extracts meaningful insights.
3. **Conversational AI Chatbot**
   - Named "Avicenna," this chatbot uses advanced LLM models (e.g., Ollama's Mistral and LLaMA 3.2) to provide tailored advice.
4. **Result Storage**
   - Saves analyzed data and chatbot interactions for easy retrieval and reporting.

#### **Navigation Workflow**

Users interact with the application through a sidebar navigation menu:

- **Home Page:** Introduces the app and its capabilities.
- **Analysis Pages:** Separate pages for ECG, EMG, and GSR/PPG analysis.
- **Chatbot:** A page dedicated to interacting with the conversational AI.

---

### **Detailed Features**

#### **1. Biosignal Data Analysis**

Each module is tailored to process and analyze data from specific biosignals:

- **ECG Analysis:**

  - Inputs: Uploaded `.csv` file containing raw ECG data.
  - Outputs: Stress levels based on heart rate variability (HRV) and other ECG markers.
  - File: Results are saved in `ecgAnalysisSteps.txt` for easy access.

- **EMG Analysis:**

  - Inputs: Uploaded `.csv` file containing EMG data.
  - Outputs: Percentage of time under high muscle activation and an explanation of muscle activity.
  - File: Results are saved in `emgAnalysisSteps.txt`.

- **GSR/PPG Analysis:**

  - Inputs: `.csv` data containing GSR/PPG readings.
  - Outputs: Emotional states derived from skin conductance and PPG.

#### **2. Cognitive Load Assessment**

- Combines insights from all biosignal modules.
- Outputs cognitive load percentage based on data and provides actionable recommendations.
- Prompt generation includes:
  - Emotional state (e.g., "Anxious," "Calm").
  - Stress level (percentage).
  - Muscle activation levels.

#### **3. Conversational Chatbot**

- **Purpose:** Provide users with professional advice based on their physiological state.
- **Features:**
  - Chain-of-Thought (CoT) reasoning for deep analysis.
  - User-specific responses based on input and analyzed data.
  - Example interaction:
    - **User Input:** "Why am I feeling so stressed?"
    - **Chatbot Response:** "Your ECG stress level is 75%. This may indicate prolonged mental strain. Here are three ways to reduce it: breathing exercises, mindfulness, and short breaks."
- **Integration:** The chatbot uses results from biosignal analysis for response generation.
- **Models:**
  - `Mistral`: Focused on cognitive load estimation.
  - `LLaMA 3.2`: Provides user-specific recommendations.

#### **4. Data Management**

- File upload functionality for `.csv` files.
- Results storage in plain-text files for easy retrieval.
- Chat history saved as downloadable PDF files.

---

### **Implementation Details**

#### **File Structure**

The project is structured into modular Python scripts:

- **`app.py`****\*\*\*\*\*\*\*\*\*\*\*\*:**

  - Manages the Streamlit interface.
  - Navigates between biosignal analysis pages and the chatbot interface.

- **`chatBot.py`****\*\*\*\*\*\*\*\*\*\*\*\*:**

  - Implements the chatbot functionality.
  - Fetches analysis results and generates responses using Ollama LLMs.

- **`requirements.txt`****\*\*\*\*\*\*\*\*\*\*\*\*:**

  - Lists all dependencies for the project, ensuring compatibility across environments.

#### **Key Functions**

1. **In ****************`app.py`****************:**

   - **Navigation Menu:** Handles user navigation using Streamlit’s sidebar.
   - **Module Integration:** Calls individual functions (`ecg_app()`, `emg_app()`, etc.) from imported scripts.

2. **In ****************`chatBot.py`****************:**

   - **Data Fetching:**
     - Reads emotional state, stress levels, and muscle activation percentages from files.
   - **Prompt Creation:**
     - Generates cognitive load and user-specific prompts based on inputs and results.
   - **Chat History Management:**
     - Stores user interactions in `st.session_state`.
   - **Chatbot Models:**
     - Initializes and invokes `Mistral` and `LLaMA 3.2` models.

3. **Result Retrieval:**

   - **ECG:** Fetches the last line of stress level data.
   - **EMG:** Extracts muscle activation percentages and explanations.
   - **GSR/PPG:** Reads emotional states.

#### **Dependencies**

The following libraries are essential for running the project (full list in `requirements.txt`):

- **Core Libraries:**

  - Streamlit (UI).
  - LangChain-Ollama (LLM integration).
  - Neurokit2 (Biosignal analysis).
  - Pandas and NumPy (Data manipulation).

- **Supporting Libraries:**

  - Python-Dotenv (Environment variable management).
  - PyTesseract and OpenCV (for future image data integration).

---

### **Developer Guide**

#### **Setup Instructions**

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**

   ```bash
   streamlit run app.py
   ```

#### **Environment Configuration**

- Ensure API keys for LangChain and Ollama are set in `.env`:
  ```
  LANGSMITH_API_KEY=<your_langchain_api_key>
  OLLAMA_API_KEY_PATH=<path_to_ollama_key>
  ```

#### **Extending the Project**

- **Add New Modules:**

  - Create a new script for the analysis (e.g., `eeg.py`).
  - Update `app.py` to include the module in the navigation menu.

- **Enhance Chatbot:**

  - Train and integrate new models using the LangChain framework.

---

### **Future Enhancements**

1. **Real-Time Data Integration:**
   - Connect directly to Shimmer or similar biosignal devices.
2. **Additional Biosignals:**
   - Add EEG analysis for cognitive fatigue.
3. **Multi-Language Support:**
   - Extend chatbot capabilities to support multiple languages.
4. **Improved Visualization:**
   - Use interactive plots for biosignal data trends.
5. **Mobile App:**
   - Develop a companion app using Streamlit’s mobile features or a dedicated framework.

---

### **Conclusion**

Avicenna integrates advanced LLMs and biosignal data analysis into a single platform, empowering users to gain insights into their cognitive and emotional states. This document outlines the project’s current implementation and provides a roadmap for fuments.

ture enhance

