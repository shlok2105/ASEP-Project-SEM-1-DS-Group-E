import os
import requests
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, render_template, redirect, url_for, flash

# --- IMPORT YOUR CALCULATIONS ---
# Ensure you have a file named calculations.py in the same folder
try:
    from calculations import calculate_metrics 
except ImportError:
    def calculate_metrics(weight, height, age, goal, gender):
        # Fallback if your file is missing
        bmi = weight / ((height/100)**2)
        return {"bmi": round(bmi, 2), "status": "Active"}

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates"),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ui"),
    static_url_path="/ui"
)
app.secret_key = "kinetic_ai_secret_key"

# --- EMAIL CONFIGURATION ---
# IMPORTANT: Use a "Google App Password", NOT your regular password.
EMAIL_SENDER = "kineticai91@gmail.com"
EMAIL_PASSWORD = "ffkcwdxjxysnmrjl" 
RECEIVER_EMAIL = "kineticai91@gmail.com"

# --- AI HELPER FUNCTIONS ---

def get_ai_7day_plan(goal, weight, age, gender):
    workout_7day = {}
    diet_7day = {}
    clean_goal = goal.replace('_', ' ')
    
    fallback_meals = [
        ["Vegetable Poha", "Dal Tadka & Rice", "Paneer Salad"],
        ["Moong Dal Chilla", "Chicken Curry & Roti", "Sautéed Veggies"],
        ["Oats with Fruit", "Rajma Chawal", "Lentil Soup"],
        ["Idli Sambhar", "Fish Curry & Rice", "Sprouted Salad"],
        ["Dalia Upma", "Paneer Bhurji & Roti", "Boiled Eggs/Soya"],
        ["Stuffed Paratha", "Chole Chawal", "Greek Yogurt"],
        ["Besan Chilla", "Egg Curry & Rice", "Mixed Fruit Bowl"]
    ]

    prompt = (f"Act as an Indian Fitness Coach. Provide a 7-day workout plan for a "
              f"{age}yo {gender}, {weight}kg, Goal: {clean_goal}. "
              f"Give 7 unique exercises. Format: Day 1: Exercise, Day 2: Exercise... "
              f"Max 6 words per exercise.")
    
    try:
        response = requests.post(
            'http://localhost:11434/api/generate', 
            json={"model": "phi3", "prompt": prompt, "stream": False},
            timeout=10 # Reduced timeout for faster feel
        )
        full_text = response.json().get('response', '').strip()
        lines = [line for line in full_text.split('\n') if "Day" in line]
        
        for i in range(1, 8):
            day_key = f"Day {i}"
            workout_7day[day_key] = lines[i-1] if i-1 < len(lines) else "Full Body Stretch"
    except:
        backups = ["Brisk Walk", "Squats", "Yoga", "Plank", "Cycling", "Pushups", "Stretching"]
        for i in range(1, 8):
            workout_7day[f"Day {i}"] = backups[i-1]
            
    for i in range(1, 8):
        diet_7day[f"Day {i}"] = fallback_meals[i-1]

    return workout_7day, diet_7day

def get_ai_bonus_tips(goal, age):
    prompt = (f"Give 3 short Indian diet tips for {goal.replace('_', ' ')} for age {age}. "
              "Max 10 words per tip.")
    try:
        response = requests.post(
            'http://localhost:11434/api/generate', 
            json={"model": "phi3", "prompt": prompt, "stream": False},
            timeout=8
        )
        return response.json().get('response', '').strip()
    except:
        return "• Drink 3-4L water.\n• Prioritize protein.\n• Avoid processed sugar."

# --- ROUTES ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        name = request.form.get("name")
        goal = request.form.get("goal")
        gender = request.form.get("gender") or "male"
        weight = float(request.form.get("weight"))
        height = float(request.form.get("height"))
        age = int(request.form.get("age"))

        metrics = calculate_metrics(weight, height, age, goal, gender)
        workout, diet = get_ai_7day_plan(goal, weight, age, gender)
        tips = get_ai_bonus_tips(goal, age)
        
        return render_template("result.html", 
                               name=name, goal=goal, gender=gender,
                               metrics=metrics, workout=workout, 
                               diet=diet, tips=tips)
    except Exception as e:
        print(f"Error in Generation: {e}")
        return f"Error: {e}", 400

@app.route("/contact", methods=["POST"])
def contact():
    try:
        u_name = request.form.get("name")
        u_email = request.form.get("email")
        u_msg = request.form.get("message")

        # Email Setup
        subject = f"Kinetic AI Inquiry from {u_name}"
        body = f"User Name: {u_name}\nUser Email: {u_email}\n\nMessage:\n{u_msg}"
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = RECEIVER_EMAIL

        # Connection Logic
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, RECEIVER_EMAIL, msg.as_string())

        flash("Message sent successfully!", "success")
    except Exception as e:
        print(f"Email Error: {e}")
        flash("Email failed to send. Check your App Password.", "danger")
        
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)