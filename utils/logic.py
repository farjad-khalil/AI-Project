import json

def load_diet_rules():
    with open("data/diet_rules.json", "r") as f:
        return json.load(f)

def get_user_profile():
    print("\nPlease provide the following details:")

    gender = input("Gender(male, female): ").strip().lower()

    body_type = input("Body Type(skinny, muscular, overweight): ").strip().lower()

    activity_level = input("Activity Level(light, moderate, intense): ").strip().lower()

    workout_type = input("Workout Type(cardio, weight training, mixed): ").strip().lower()

    current_diet = input("Current Diet(normal, vegetarian, high-fat, low-carb, high-protein): ").strip().lower()

    goal = input("Fitness Goal(bulk, lean, strength): ").strip().lower()

    user = {
        "name": input("Name: "),
        "age": int(input("Age: ")),
        "gender": gender,
        "height": float(input("Height (in cm): ")),
        "weight": float(input("Weight (in kg): ")),
        "body_type": body_type,
        "activity_level": activity_level,
        "workout_type": workout_type,
        "current_diet": current_diet,
        "goal": goal
    }

    return user

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
        workout_comment = should_change_workout(workout_type, goal)

        return f"""
Name: {user['name']} ({user['age']} y/o {user['gender']})
Height: {user['height']} cm
Weight: {user['weight']} kg

Goal: {goal.upper()}
Body Type: {body_type}
Activity Level: {activity}
Workout Type: {workout_type}
Current Diet: {user['current_diet']}

--- DIET PLAN ---
Diet Type: {plan['diet_type']}
Example Meal: {plan['meal']}

--- WORKOUT SUGGESTION ---
{workout_comment}
Suggested frequency: {activity.capitalize()} level = 4 to 6 days per week
"""
    except KeyError:
        return "Sorry, no plan available for the selected combination. Try adjusting your inputs."
