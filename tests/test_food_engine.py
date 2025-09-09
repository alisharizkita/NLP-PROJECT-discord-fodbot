# src/food_engine.py
import json
import os
import re
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from food_patterns import FoodPatterns

class FoodRecommendationEngine:
    def __init__(self):
        # Load database restaurants.json dari folder data
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(root_dir, "data", "restaurant.json")
        with open(db_path, "r", encoding="utf-8") as f:
            self.restaurants = json.load(f)
        
        # Load regex patterns
        self.patterns = FoodPatterns()

    def detect_budget(self, text: str) -> str:
        for pattern, result in self.patterns.budget_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if callable(result):
                    return result(match)
                else:
                    return result
        return "medium"  # default

    def detect_location(self, text: str) -> str:
        for pattern, loc in self.patterns.location_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return loc
        return "off-campus"  # default

    def detect_food_type(self, text: str) -> str:
        for pattern, ftype in self.patterns.food_type_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return ftype
        return "rice"  # default

    def process(self, user_input: str) -> dict:
        """
        Ambil input user, deteksi budget, lokasi, food type.
        Kembalikan dict dengan parsed info.
        """
        budget = self.detect_budget(user_input)
        location = self.detect_location(user_input)
        food_type = self.detect_food_type(user_input)

        # Ambil rekomendasi restoran sesuai kriteria
        matched_restaurants = []
        if location in self.restaurants and budget in self.restaurants[location]:
            for resto in self.restaurants[location][budget]:
                # Cek food type
                types = resto["food_type"]
                if isinstance(types, str):
                    types = [types]
                if food_type in types:
                    matched_restaurants.append(resto["name"])

        return {
            "budget": budget,
            "location": location,
            "food_type": food_type,
            "matches": matched_restaurants
        }

# =======================
# Bagian testing interaktif
# =======================
if __name__ == "__main__":
    engine = FoodRecommendationEngine()
    print("=== Food Recommendation Engine ===")
    print("Ketik 'exit' untuk keluar.\n")

    while True:
        user_input = input("Tulis pesanmu: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Terima kasih! Sampai jumpa.")
            break
        result = engine.process(user_input)
        print("\nParsed result:", result)
        if result["matches"]:
            print("Rekomendasi restoran:", ", ".join(result["matches"]))
        else:
            print("Tidak ada restoran yang cocok dengan kriteria.\n")
        print("-" * 50)
