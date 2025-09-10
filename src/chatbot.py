from food_engine import FoodRecommendationEngine
from food_patterns import FoodPatterns

def run_chatbot():
    print("Halo👋! Aku food chatbot yang siap bantu kasih rekomendasi makanan🍽️")
    print("Kamu bisa kasih tau aku apa yang kamu mau, misal nasi, mie, sushi, minuman segar, dll.")
    print("Kalau mau skip pertanyaan, ketik '\\' atau enter ➡️")

    engine = FoodRecommendationEngine()
    patterns = FoodPatterns()

    prefs = {}

    # Step 1: Food type
    answer_food = input("\nKamu lagi pengen makan apa nih?😁 ")
    parsed = patterns.detect(answer_food)
    if parsed.get("food_type"):
        prefs["food_type"] = parsed["food_type"]

    # Step 2: Location
    answer_location = input("Kamu sekarang lagi di mana?📍 ")
    if answer_location.strip() not in ["", "\\"]:
        parsed = patterns.detect(answer_location)
        if parsed.get("location"):
            prefs["location"] = parsed["location"]

    # Step 3: Budget
    answer_budget = input("Berapa budget yang kamu punya?💸 ")
    if answer_budget.strip() not in ["", "\\"]:
        parsed = patterns.detect(answer_budget)
        if parsed.get("budget"):
            prefs["budget"] = parsed["budget"]

    # Step 4: Mood
    answer_mood = input("Mood kamu lagi gimana sekarang?💓 ")
    if answer_mood.strip() not in ["", "\\"]:
        parsed = patterns.detect(answer_mood)
        if parsed.get("mood"):
            prefs["mood"] = parsed["mood"]

    # Step 5: Time
    answer_time = input("Mau buat sarapan, makan siang, atau makan malam nih?⏰ ")
    if answer_time.strip() not in ["", "\\"]:
        parsed = patterns.detect(answer_time)
        if parsed.get("time_based"):
            prefs["time_based"] = parsed["time_based"]

    # Step 6: Dietary restriction
    answer_diet = input("Apa dietary restriction kamu?🚫 ")
    if answer_diet.strip() not in ["", "\\"]:
        parsed = patterns.detect(answer_diet)
        if parsed.get("dietary_restriction"):
            prefs["dietary_restriction"] = parsed["dietary_restriction"]

    # Rekomendasi
    result = engine.get_recommendation(prefs)
    if "error" in result:
        print(result["error"])
    else:
        print("Restoran yang cocok dengan preferensimu:")
        for r in result["restaurants"]:
            print(f"- {r['name']}")

if __name__ == "__main__":
    run_chatbot()
