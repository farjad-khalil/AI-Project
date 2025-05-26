import streamlit as st
import json

def load_diet_rules():
    with open("data/diet_rules.json", "r") as f:
        return json.load(f)

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
        return "Switch to weight training or mixed for effective bulking."
    elif goal == "lean" and current == "weight training":
        return "Add cardio or switch to mixed for better fat burning."
    elif goal == "strength" and current != "weight training":
        return "Switch to weight training for optimal strength gains."
    return "Your workout type aligns well with your goal."

# --- UI Starts ---
st.set_page_config(page_title="SmartDietAdvisor", layout="centered")
st.title("SmartDietAdvisor")
st.caption("Your AI-powered fitness & nutrition assistant")

with st.form("user_input_form"):
    st.subheader("👤 Personal Information")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=10, max_value=100)
    gender = st.selectbox("Gender", ["male", "female"])
    height = st.number_input("Height (in cm)", min_value=100, max_value=250)
    weight = st.number_input("Weight (in kg)", min_value=30, max_value=200)

    st.subheader("⚙️ Fitness Profile")
    body_type = st.selectbox("Body Type", ["skinny", "muscular", "overweight"])
    activity_level = st.selectbox("Activity Level", ["light", "moderate", "intense"])
    workout_type = st.selectbox("Workout Type", ["cardio", "weight training", "mixed"])
    current_diet = st.selectbox("Current Diet", ["normal", "vegetarian", "high-fat", "low-carb", "high-protein"])
    goal = st.selectbox("Fitness Goal", ["bulk", "lean", "strength"])

    submitted = st.form_submit_button("🎯 Generate My Plan")

if submitted:
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

    rules = load_diet_rules()
    bmi, bmi_cat = calculate_bmi(user["weight"], user["height"])
    calories = calculate_calories(user)
    protein, carbs, fat = calculate_macros(calories)

    try:
        plan = rules[goal][body_type][activity_level]
        meals = plan["meals"]

        st.success(f"Hi {user['name']}, here's your personalized fitness & diet plan!")

        st.subheader("📊 Health Summary")
        col1, col2 = st.columns(2)
        col1.metric("BMI", f"{bmi}", delta=bmi_cat)
        col2.metric("Daily Calories", f"{calories} kcal")

        st.markdown(f"""
        **Macronutrient Split:**
        - **Protein**: {protein}g  
        - **Carbs**: {carbs}g  
        - **Fat**: {fat}g
        """)

        st.subheader("🥗 Meal Plan")
        st.info(f"**Diet Type:** {plan['diet_type']}")
        st.markdown(f"""
        - **Breakfast**: {meals['breakfast']}
        - **Lunch**: {meals['lunch']}
        - **Dinner**: {meals['dinner']}
        - **Snack**: {meals['snack']}
        """)

        st.subheader("💪 Workout Recommendation")
        st.warning(should_change_workout(workout_type, goal))

    except KeyError:
        st.error("⚠️ No plan found for this combination. Try a different input.")
