import os
import random
from flask import Flask, request, render_template

# Setup base directory correctly to find templates one level up
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

app = Flask(
    __name__,
    template_folder=os.path.join(ROOT_DIR, "templates"),
    static_folder=os.path.join(ROOT_DIR, "ui")
)

def get_varied_plan(goal):
    workout_pool = {
        "weight_loss": ["HIIT Cardio", "Tabata Circuit", "Steady State Run", "Jump Rope & Abs"],
        "muscle_gain": ["Bench Press & Triceps", "Deadlifts & Back", "Squats & Quads"],
        "maintenance": ["Light Jogging", "Pilates Flow", "Bodyweight Circuit"]
    }
    
    breakfasts = ["Oatmeal with Walnuts", "Greek Yogurt & Honey", "Scrambled Eggs on Toast"]
    lunches = ["Grilled Chicken Salad", "Quinoa & Black Beans", "Turkey & Avocado Wrap"]
    dinners = ["Baked Salmon", "Tofu Stir-fry", "Lean Beef & Broccoli"]

    workout_7day = {}
    diet_7day = {}

    for i in range(1, 8):
        day = f"Day {i}"
        if i == 7:
            workout_7day[day] = "Rest & Active Recovery Walk"
        else:
            workout_7day[day] = random.choice(workout_pool.get(goal, workout_pool["maintenance"]))
        
        diet_7day[day] = [
            f"Breakfast: {random.choice(breakfasts)}",
            f"Lunch: {random.choice(lunches)}",
            f"Dinner: {random.choice(dinners)}"
        ]
    
    return workout_7day, diet_7day

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    name = request.form.get("name")
    goal = request.form.get("goal")
    
    # Ensure variables aren't empty
    if not name or not goal:
        return "Please fill out the form!", 400

    user_info = {"name": name, "goal": goal}
    workout, diet = get_varied_plan(goal)
    
    return render_template("result.html", user=user_info, workout=workout, diet=diet)

if __name__ == "__main__":
    app.run(debug=True)