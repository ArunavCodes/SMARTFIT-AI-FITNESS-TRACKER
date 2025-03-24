# SMARTFIT: AI-Powered Fitness Tracker

## Overview
The **SMARTFIT AI Fitness Tracker** is a Python-based application designed to help users monitor and improve their fitness levels using AI and machine learning. It predicts key fitness metrics such as calories burned, BMI, heart rate, and running speed, and provides personalized suggestions and detailed reports.

---

## Features
- **AI-Driven Predictions**: Predicts calories burned, BMI, heart rate, and running speed using machine learning models.
- **Personalized Reports**: Generates detailed PDF reports summarizing fitness metrics and suggestions.
- **Data Visualization**: Provides visualizations (e.g., histograms) for better understanding of fitness data.
- **User-Friendly Interface**: Modern and intuitive GUI built using Tkinter and ttkbootstrap.
- **No Hardware Dependency**: Works on standard desktops/laptops without requiring wearable devices.

---

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ArunavCodes/SMARTFIT-AI-FITNESS-TRACKER.git
   cd SMARTFIT-AI-FITNESS-TRACKER

2. **Install Dependencies**:
Ensure you have Python 3.x installed. Then, install the required libraries:
-pip install pandas scikit-learn joblib matplotlib fpdf ttkbootstrap opencv-python

4. **Run the Application**:
Execute the following command to start the application:
-python app.py

## Usage
1. **Input Your Data**:
   - Enter your age, gender, height, weight, running time, running speed, distance, and heart rate using the sliders and input fields.

2. **Get Predictions**:
   - Click on the buttons to predict calories burned, calculate BMI, analyze workout intensity, and more.

3. **View Results**:
   - Results are displayed in message boxes and visualizations.
   - A detailed PDF report is generated and saved as `fitness_report.pdf`.

# File Structure

- SMARTFIT-AI-FITNESS-TRACKER/
  - models/
    - calories_model.pkl
    - bmi_model.pkl
    - heart_rate_model.pkl
    - running_speed_model.pkl
    - scaler.pkl
  - dist/
  - build/
  - app.py
  - README.md
  - requirements.txt

## Machine Learning Models
The application uses the following pre-trained models:

| Model Name             | Purpose                         |
|------------------------|--------------------------------|
| `calories_model.pkl`   | Predicts calories burned       |
| `bmi_model.pkl`        | Calculates BMI                 |
| `heart_rate_model.pkl` | Predicts workout intensity     |
| `running_speed_model.pkl` | Predicts running speed  |
| `scaler.pkl`          | Preprocesses input data        |

## Future Work
- **Wearable Integration**: Add support for devices like Fitbit and Apple Watch.
- **Mobile Application**: Develop iOS and Android versions.
- **Expanded Dataset**: Use a larger, more diverse dataset to improve model accuracy.
- **Advanced Features**: Include meal tracking, hydration tracking, and sleep analysis.
- **Cloud Integration**: Enable data synchronization across devices.



   
