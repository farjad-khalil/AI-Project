from utils.logic import suggest_diet, get_user_profile

if __name__ == "__main__":
    print("=== Welcome to SmartDietAdvisor v5.0 ===")
    user = get_user_profile()
    recommendation = suggest_diet(user)
    print("\nPersonalized Diet & Workout Suggestion:\n")
    print(recommendation)
