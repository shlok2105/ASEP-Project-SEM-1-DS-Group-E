def calculate_metrics(weight, height, age, goal, gender):
    """
    Calculates fitness metrics based on physical attributes.
    Formula: Mifflin-St Jeor Equation
    """
    # 1. Body Mass Index (BMI)
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 1)

    # 2. Basal Metabolic Rate (BMR)
    if gender.lower() == "male":
        bmr = int((10 * weight) + (6.25 * height) - (5 * age) + 5)
    else:
        bmr = int((10 * weight) + (6.25 * height) - (5 * age) - 161)

    # 3. Total Daily Energy Expenditure (TDEE) - Moderate Activity baseline
    maintenance_calories = int(bmr * 1.55)

    # 4. Target Calories based on the User's Goal
    if goal == "weight_loss":
        tdee = maintenance_calories - 500
    elif goal == "muscle_gain":
        tdee = maintenance_calories + 300
    else:
        tdee = maintenance_calories

    # 5. Determine BMI Status for UI badge
    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi < 25:
        status = "Normal"
    elif 25 <= bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"

    # Updated keys to match exactly what result.html expects
    return {
        "bmi": bmi,
        "bmr": bmr,
        "calories": tdee,  # Key renamed from 'tdee' to 'calories'
        "status": status
    }