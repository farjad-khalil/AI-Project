import json

def load_diet_rules():
    with open("data/diet_rules.json", "r") as f:
        return json.load(f)

def get_valid_input(prompt, valid_options):
    while True:
        value = input(f"{prompt} ({', '.join(valid_options)}): ").strip().lower()
        if value in valid_options:
            return value
        print(f"Invalid input. Please enter one of: {', '.join(valid_options)}")

def get_user_profile():
    print("\nPlease provide the following details:")

    gender = get_valid_input("Gender", ["male", "female", "other"])
    body_type = get_valid_input("Body Type", ["skinny", "muscular", "overweight"])
    activity_level = get_valid_input("Activity Level", ["light", "moderate", "intense"])
    workout_type = get_valid_input("Workout Type", ["cardio", "weight training", "mixed"])
    current_diet = get_valid_input("Current Diet", ["normal", "vegetarian", "high-fat", "low-carb", "high-protein"])
    goal = get_valid_input("Fitness Goal", ["bulk", "lean", "strength"])

    name = input("Name: ")

    while True:
        try:
            age = int(input("Age: "))
            break
        except ValueError:
            print("Please enter a valid number for age.")

    while True:
        try:
            height = float(input("Height (in cm): "))
            break
        except ValueError:
            print("Please enter a valid number for height.")

    while True:
        try:
            weight = float(input("Weight (in kg): "))
            break
        except ValueError:
            print("Please enter a valid number for weight.")

    user = {
        "name": name,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "body_type": body_type,
        "activity_level": activity_level,
        "workout_type": workout_type,
        "current_diet": current_diet,
        "goal": goal
    }

    return user

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
    return round(bmi, 1), category

def calculate_calories(user):
    if user["gender"] == "male":
        bmr = 10 * user["weight"] + 6.25 * user["height"] - 5 * user["age"] + 5
    else:
        bmr = 10 * user["weight"] + 6.25 * user["height"] - 5 * user["age"] - 161

    activity_multipliers = {
        "light": 1.375,
        "moderate": 1.55,
        "intense": 1.725
    }
    calories = bmr * activity_multipliers[user["activity_level"]]

    if user["goal"] == "bulk":
        calories += 500
    elif user["goal"] == "lean":
        calories -= 500

    return round(calories)

def calculate_macros(calories):
    protein = round((calories * 0.3) / 4)
    carbs = round((calories * 0.4) / 4)
    fat = round((calories * 0.3) / 9)
    return protein, carbs, fat

def should_change_workout(current, goal):
    if goal == "bulk" and current == "cardio":
        return "Recommendation: Switch to weight training or mixed for effective bulking."
    elif goal == "lean" and current == "weight training":
        return "Recommendation: Add cardio or switch to mixed for fat burning."
    elif goal == "strength" and current != "weight training":
        return "Recommendation: Switch to weight training to build strength efficiently."
    return "Your workout type aligns with your goal."

def suggest_diet(user):
    rules = load_diet_rules()
    goal = user["goal"]
    body_type = user["body_type"]
    activity = user["activity_level"]
    workout_type = user["workout_type"]

    try:
        plan = rules[goal][body_type][activity]
        bmi, bmi_cat = calculate_bmi(user["weight"], user["height"])
        calories = calculate_calories(user)
        protein, carbs, fat = calculate_macros(calories)
        workout_comment = should_change_workout(workout_type, goal)

        return f"""
Name: {user['name']} ({user['age']} y/o {user['gender']})
Height: {user['height']} cm
Weight: {user['weight']} kg
BMI: {bmi} ({bmi_cat})

Goal: {goal.upper()}
Body Type: {body_type}
Activity Level: {activity}
Workout Type: {workout_type}
Current Diet: {user['current_diet']}

--- DAILY MEAL PLAN ---
Diet Type: {plan['diet_type']}
Meals:
- Breakfast: {plan['meals']['breakfast']}
- Lunch: {plan['meals']['lunch']}
- Dinner: {plan['meals']['dinner']}
- Snack: {plan['meals']['snack']}

--- CALORIC NEEDS ---
Estimated Daily Calories: {calories} kcal
Macronutrient Split:
- Protein: {protein}g
- Carbs: {carbs}g
- Fat: {fat}g

--- WORKOUT SUGGESTION ---
{workout_comment}
Suggested frequency: {activity.capitalize()} level = 4 to 6 days per week
"""

    except KeyError:
        return "Sorry, no plan available for the selected combination. Try adjusting your inputs."
