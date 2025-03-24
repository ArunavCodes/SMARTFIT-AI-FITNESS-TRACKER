import tkinter as tk
from tkinter import messagebox, Label, ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Scale
from fpdf import FPDF  # For generating PDFs
import datetime
from PIL import Image, ImageTk
import cv2  # For video processing
import os  # For opening the PDF automatically

# Load models and scaler
calories_model = joblib.load('models/calories_model.pkl')
bmi_model = joblib.load('models/bmi_model.pkl')
heart_rate_model = joblib.load('models/heart_rate_model.pkl')
running_speed_model = joblib.load('models/running_speed_model.pkl')
scaler = joblib.load('models/scaler.pkl')

# Function to predict calories burned
def predict_calories():
    try:
        input_data = np.array([[int(age_slider.get()), int(gender_var.get()), float(height_slider.get()),
                                float(weight_slider.get()), float(running_time_slider.get()),
                                float(running_speed_slider.get()), float(distance_slider.get()),
                                float(heart_rate_slider.get())]])
        input_data = scaler.transform(input_data)
        calories_burned = calories_model.predict(input_data)[0]
        messagebox.showinfo("Calories Burned", f"Calories Burned: {calories_burned:.2f}")
        return calories_burned
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return 0

# Function to calculate BMI
def calculate_bmi():
    try:
        height = float(height_slider.get()) / 100  # Convert cm to m
        weight = float(weight_slider.get())
        bmi = weight / (height ** 2)
        messagebox.showinfo("BMI", f"Your BMI: {bmi:.2f}")
        return bmi
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return 0

# Function to show data analysis
def show_analysis():
    df = pd.read_csv('calories_burned_data.csv')
    fig, ax = plt.subplots()
    df['Calories Burned'].plot(kind='hist', ax=ax, title='Calories Burned Distribution')
    
    # Clear previous graph if it exists
    if hasattr(show_analysis, 'canvas'):
        show_analysis.canvas.get_tk_widget().destroy()
    
    # Create a canvas for the graph and place it on the right side
    show_analysis.canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    show_analysis.canvas.draw()
    show_analysis.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Function to calculate running speed
def calculate_running_speed():
    try:
        distance = float(distance_slider.get())
        time = float(running_time_slider.get())
        if time > 0:
            speed = distance / (time / 60)  # km/h
            messagebox.showinfo("Running Speed", f"Running Speed: {speed:.2f} km/h")
        else:
            messagebox.showerror("Error", "Running time must be greater than 0")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to calculate workout intensity
def calculate_workout_intensity():
    try:
        heart_rate = float(heart_rate_slider.get())
        max_heart_rate = 220 - int(age_slider.get())
        intensity = (heart_rate / max_heart_rate) * 100
        messagebox.showinfo("Workout Intensity", f"Workout Intensity: {intensity:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to classify BMI
def classify_bmi():
    try:
        height = float(height_slider.get()) / 100  # Convert cm to m
        weight = float(weight_slider.get())
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        messagebox.showinfo("BMI Classification", f"Your BMI: {bmi:.2f} ({category})")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to set goals
def set_goals():
    global goal_calories, goal_steps
    goal_calories = float(goal_calories_entry.get())
    goal_steps = float(goal_steps_entry.get())
    messagebox.showinfo("Goals Set", f"Calories Goal: {goal_calories}, Steps Goal: {goal_steps}")

# Function to track progress
def track_progress():
    try:
        calories_burned = predict_calories()
        steps_taken = float(steps_entry.get())
        calories_progress = (calories_burned / goal_calories) * 100
        steps_progress = (steps_taken / goal_steps) * 100
        messagebox.showinfo("Progress", f"Calories Progress: {calories_progress:.2f}%, Steps Progress: {steps_progress:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to provide suggestions
def provide_suggestions():
    try:
        bmi = calculate_bmi()
        intensity = calculate_workout_intensity()
        if bmi < 18.5:
            suggestion = "Consider increasing your calorie intake and strength training."
        elif 18.5 <= bmi < 25:
            suggestion = "Maintain your current routine. Keep up the good work!"
        elif 25 <= bmi < 30:
            suggestion = "Consider incorporating more cardio and a balanced diet."
        else:
            suggestion = "Consult a healthcare provider for a tailored fitness plan."
        messagebox.showinfo("Suggestions", suggestion)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to compare user inputs with dataset averages
def compare_with_dataset():
    try:
        # Load the dataset
        df = pd.read_csv('calories_burned_data.csv')

        # Calculate dataset averages
        avg_calories_burned = df['Calories Burned'].mean()
        avg_bmi = (df['Weight(kg)'] / ((df['Height(cm)'] / 100) ** 2)).mean()
        avg_running_speed = df['Running Speed(km/h)'].mean()
        avg_heart_rate = df['Average Heart Rate'].mean()

        # Get user inputs
        user_calories_burned = predict_calories()
        user_bmi = calculate_bmi()
        user_running_speed = float(running_speed_slider.get())
        user_heart_rate = float(heart_rate_slider.get())

        # Create a comparison report
        comparison_report = (
            f"Comparison with Dataset Averages:\n"
            f"----------------------------------------\n"
            f"Calories Burned:\n"
            f"  Your Value: {user_calories_burned:.2f}\n"
            f"  Dataset Average: {avg_calories_burned:.2f}\n"
            f"----------------------------------------\n"
            f"BMI:\n"
            f"  Your Value: {user_bmi:.2f}\n"
            f"  Dataset Average: {avg_bmi:.2f}\n"
            f"----------------------------------------\n"
            f"Running Speed:\n"
            f"  Your Value: {user_running_speed:.2f} km/h\n"
            f"  Dataset Average: {avg_running_speed:.2f} km/h\n"
            f"----------------------------------------\n"
            f"Average Heart Rate:\n"
            f"  Your Value: {user_heart_rate:.2f} bpm\n"
            f"  Dataset Average: {avg_heart_rate:.2f} bpm\n"
            f"----------------------------------------\n"
        )

        # Display the comparison report in a new window
        comparison_window = tk.Toplevel(root)
        comparison_window.title("Comparison with Dataset Averages")
        comparison_label = tk.Label(comparison_window, text=comparison_report, justify=tk.LEFT)
        comparison_label.pack(padx=20, pady=20)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to generate report
def generate_report():
    try:
        # Collect data
        age = int(age_slider.get())
        gender = "Female" if int(gender_var.get()) == 0 else "Male"
        height = float(height_slider.get())
        weight = float(weight_slider.get())
        running_time = float(running_time_slider.get())
        running_speed = float(running_speed_slider.get())
        distance = float(distance_slider.get())
        heart_rate = float(heart_rate_slider.get())

        # Calculate metrics
        bmi = weight / ((height / 100) ** 2)
        calories_burned = predict_calories()
        workout_intensity = (heart_rate / (220 - age)) * 100

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Fitness Tracker Report", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        pdf.cell(200, 10, txt="----------------------------------------", ln=True, align="C")

        pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
        pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
        pdf.cell(200, 10, txt=f"Height: {height} cm", ln=True)
        pdf.cell(200, 10, txt=f"Weight: {weight} kg", ln=True)
        pdf.cell(200, 10, txt=f"Running Time: {running_time} min", ln=True)
        pdf.cell(200, 10, txt=f"Running Speed: {running_speed} km/h", ln=True)
        pdf.cell(200, 10, txt=f"Distance: {distance} km", ln=True)
        pdf.cell(200, 10, txt=f"Average Heart Rate: {heart_rate} bpm", ln=True)
        pdf.cell(200, 10, txt="----------------------------------------", ln=True, align="C")

        pdf.cell(200, 10, txt=f"BMI: {bmi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Calories Burned: {calories_burned:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Workout Intensity: {workout_intensity:.2f}%", ln=True)
        pdf.cell(200, 10, txt="----------------------------------------", ln=True, align="C")

        pdf.cell(200, 10, txt="Suggestions:", ln=True)
        if bmi < 18.5:
            suggestion = "Consider increasing your calorie intake and strength training."
        elif 18.5 <= bmi < 25:
            suggestion = "Maintain your current routine. Keep up the good work!"
        elif 25 <= bmi < 30:
            suggestion = "Consider incorporating more cardio and a balanced diet."
        else:
            suggestion = "Consult a healthcare provider for a tailored fitness plan."
        pdf.cell(200, 10, txt=suggestion, ln=True)

        # Save PDF
        pdf.output("fitness_report.pdf")
        messagebox.showinfo("Report Generated", "Fitness report has been saved as 'fitness_report.pdf'")

        # Open the PDF automatically
        if os.name == "nt":  # For Windows
            os.startfile("fitness_report.pdf")
        elif os.name == "posix":  # For macOS or Linux
            os.system("open fitness_report.pdf")  # macOS
            # os.system("xdg-open fitness_report.pdf")  # Linux
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window with ttkbootstrap theme
root = ttk.Window(themename="cosmo")
root.title("Fitness Tracker")

# Maximize the window
root.state('zoomed')  # Maximize the window to full screen

# Create a frame for the graph
graph_frame = ttk.Frame(root)
graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a canvas and a scrollbar for the main content
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

# Configure the canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Add input fields, sliders, and buttons
ttk.Label(scrollable_frame, text="Age:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
age_slider = Scale(scrollable_frame, from_=10, to=100, orient=tk.HORIZONTAL, length=400)
age_slider.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
age_value_label = Label(scrollable_frame, text="10")
age_value_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

def update_age_value(val):
    age_value_label.config(text=f"{int(float(val))}")

age_slider.config(command=update_age_value)

ttk.Label(scrollable_frame, text="Gender (0=Female, 1=Male):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
gender_var = tk.IntVar()
gender_entry = ttk.Entry(scrollable_frame, textvariable=gender_var)
gender_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

ttk.Label(scrollable_frame, text="Height (cm):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
height_slider = Scale(scrollable_frame, from_=100, to=250, orient=tk.HORIZONTAL, length=400)
height_slider.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
height_value_label = Label(scrollable_frame, text="100")
height_value_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")

def update_height_value(val):
    height_value_label.config(text=f"{int(float(val))}")

height_slider.config(command=update_height_value)

ttk.Label(scrollable_frame, text="Weight (kg):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
weight_slider = Scale(scrollable_frame, from_=30, to=150, orient=tk.HORIZONTAL, length=400)
weight_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
weight_value_label = Label(scrollable_frame, text="30")
weight_value_label.grid(row=3, column=2, padx=10, pady=5, sticky="w")

def update_weight_value(val):
    weight_value_label.config(text=f"{int(float(val))}")

weight_slider.config(command=update_weight_value)

# Running Time Slider
ttk.Label(scrollable_frame, text="Running Time (min):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
running_time_slider = Scale(scrollable_frame, from_=0, to=120, orient=tk.HORIZONTAL, length=400)
running_time_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
running_time_value_label = Label(scrollable_frame, text="0")
running_time_value_label.grid(row=4, column=2, padx=10, pady=5, sticky="w")

def update_running_time_value(val):
    running_time_value_label.config(text=f"{int(float(val))}")

running_time_slider.config(command=update_running_time_value)

# Running Speed Slider (updated to 40 km/h)
ttk.Label(scrollable_frame, text="Running Speed (km/h):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
running_speed_slider = Scale(scrollable_frame, from_=0, to=40, orient=tk.HORIZONTAL, length=400)  # Updated to 40 km/h
running_speed_slider.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
running_speed_value_label = Label(scrollable_frame, text="0")
running_speed_value_label.grid(row=5, column=2, padx=10, pady=5, sticky="w")

def update_running_speed_value(val):
    running_speed_value_label.config(text=f"{int(float(val))}")

running_speed_slider.config(command=update_running_speed_value)

# Distance Slider
ttk.Label(scrollable_frame, text="Distance (km):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
distance_slider = Scale(scrollable_frame, from_=0, to=50, orient=tk.HORIZONTAL, length=400)
distance_slider.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
distance_value_label = Label(scrollable_frame, text="0")
distance_value_label.grid(row=6, column=2, padx=10, pady=5, sticky="w")

def update_distance_value(val):
    distance_value_label.config(text=f"{int(float(val))}")

distance_slider.config(command=update_distance_value)

# Average Heart Rate Slider
ttk.Label(scrollable_frame, text="Average Heart Rate (bpm):").grid(row=7, column=0, padx=10, pady=5, sticky="w")
heart_rate_slider = Scale(scrollable_frame, from_=50, to=200, orient=tk.HORIZONTAL, length=400)
heart_rate_slider.grid(row=7, column=1, padx=10, pady=5, sticky="ew")
heart_rate_value_label = Label(scrollable_frame, text="50")
heart_rate_value_label.grid(row=7, column=2, padx=10, pady=5, sticky="w")

def update_heart_rate_value(val):
    heart_rate_value_label.config(text=f"{int(float(val))}")

heart_rate_slider.config(command=update_heart_rate_value)

# Create buttons for various actions
ttk.Button(scrollable_frame, text="Predict Calories Burned", command=predict_calories, bootstyle=PRIMARY).grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Calculate BMI", command=calculate_bmi, bootstyle=SUCCESS).grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Show Data Analysis", command=show_analysis, bootstyle=INFO).grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Calculate Running Speed", command=calculate_running_speed, bootstyle=WARNING).grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Calculate Workout Intensity", command=calculate_workout_intensity, bootstyle=WARNING).grid(row=12, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Classify BMI", command=classify_bmi, bootstyle=SUCCESS).grid(row=13, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Set Goals", command=set_goals, bootstyle=INFO).grid(row=14, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Track Progress", command=track_progress, bootstyle=INFO).grid(row=15, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Provide Suggestions", command=provide_suggestions, bootstyle=INFO).grid(row=16, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Generate Report", command=generate_report, bootstyle=INFO).grid(row=17, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
ttk.Button(scrollable_frame, text="Compare with Dataset", command=compare_with_dataset, bootstyle=INFO).grid(row=18, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Add new entry fields for goals
ttk.Label(scrollable_frame, text="Goal Calories:").grid(row=19, column=0, padx=10, pady=5, sticky="w")
goal_calories_entry = ttk.Entry(scrollable_frame)
goal_calories_entry.grid(row=19, column=1, padx=10, pady=5, sticky="ew")

ttk.Label(scrollable_frame, text="Goal Steps:").grid(row=20, column=0, padx=10, pady=5, sticky="w")
goal_steps_entry = ttk.Entry(scrollable_frame)
goal_steps_entry.grid(row=20, column=1, padx=10, pady=5, sticky="ew")

ttk.Label(scrollable_frame, text="Steps Taken:").grid(row=21, column=0, padx=10, pady=5, sticky="w")
steps_entry = ttk.Entry(scrollable_frame)
steps_entry.grid(row=21, column=1, padx=10, pady=5, sticky="ew")

# Run the app
root.mainloop()