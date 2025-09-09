import json
import random
from food_patterns import FoodPatterns

class FoodRecommendationEngine:
    def __init__(self, db_path=None):
        import os
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "..", "data", "restaurant.json")
        with open(db_path, "r", encoding="utf-8") as f:
            self.restaurants = json.load(f)
        self.patterns = FoodPatterns()

    def get_recommendation(self, message: str) -> dict:
        prefs = self.patterns.detect(message)

        location = prefs.get("location")
        budget = prefs.get("budget")
        food_type = prefs.get("food_type")

        if not location or not budget:
            return {
                "error": "Tolong sebutkan lokasi (campus/off-campus/delivery) dan budget (low/medium/high).",
                "detected": prefs
            }

        candidates = self.restaurants.get(location, {}).get(budget, [])

        if food_type:
            candidates = [
                r for r in candidates if (
                    (isinstance(r["food_type"], list) and food_type in r["food_type"])
                    or (isinstance(r["food_type"], str) and r["food_type"] == food_type)
                )
            ]

        if not candidates:
            return {
                "error": f"Tidak ditemukan rekomendasi dengan preferensi {prefs}",
                "detected": prefs
            }

        return random.choice(candidates)

    def process(self, user_input: str) -> dict:
        """
        Extract budget, location, and food_type from user input.
        """
        return self.patterns.detect(user_input)
