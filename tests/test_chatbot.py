import sys, os

# Tambahkan path ke src biar bisa import modul di sana
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from food_engine import FoodRecommendationEngine
from food_patterns import FoodPatterns

def run_case(case_name, test_inputs):
    print(f"\n===== {case_name} =====")
    engine = FoodRecommendationEngine()
    patterns = FoodPatterns()
    prefs = {}

    for msg, key in test_inputs:
        parsed = patterns.detect(msg)
        if parsed.get(key):
            prefs[key] = parsed[key]
        print(f"USER : {msg}")
        print(f"PARSED: {parsed}")

    result = engine.get_recommendation(prefs)
    print("Final Prefs:", prefs)
    print("Recommendation Result:", result)


def test_chatbot_logic():
    cases = [
        (
            "Case 1 - Halal Dinner",
            [
                ("aku pengen makan nasi goreng", "food_type"),
                ("off-campus", "location"),
                ("30000", "budget"),
                ("lagi capek banget", "mood"),
                ("makan malam", "time_based"),
                ("halal", "dietary_restriction"),
            ],
        ),
        (
            "Case 2 - Midnight Bakso",
            [
                ("gue pengen bakso", "food_type"),
                ("campus", "location"),
                ("15000", "budget"),
                ("gabut banget", "mood"),
                ("makan malam", "time_based"),
                ("", "dietary_restriction"),
            ],
        ),
        (
            "Case 3 - Vegetarian Lunch",
            [
                ("saya mau makan halal", "dietary_restriction"),
                ("mau makan mie ayam", "food_type"),
                ("campus", "location"),
                ("25000", "budget"),
                ("lagi semangat", "mood"),
                ("makan siang", "time_based"),
            ],
        ),
        (
            "Case 4 - Cheap Breakfast",
            [
                ("pengen bubur ayam", "food_type"),
                ("delivery", "location"),
                ("murah", "budget"),
                ("baru bangun", "mood"),
                ("sarapan", "time_based"),
                ("halal", "dietary_restriction"),
            ],
        ),
        (
            "Case 5 - Traktiran Happy",
            [
                ("aku happy banget, mau traktiran", "mood"),
                ("pengen makan seafood", "food_type"),
                ("off-campus", "location"),
                ("100000", "budget"),
                ("makan malam", "time_based"),
                ("", "dietary_restriction"),
            ],
        ),
        (
            "Case 6 - Diet Friendly",
            [
                ("lagi diet vegetarian", "dietary_restriction"),
                ("mau makan ayam", "food_type"),
                ("delivery", "location"),
                ("bebas berapa", "budget"),
                ("lagi sehat", "mood"),
                ("makan siang", "time_based"),
            ],
        ),
    ]



    for case_name, inputs in cases:
        run_case(case_name, inputs)


if __name__ == "__main__":
    test_chatbot_logic()
