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

    def get_recommendation(self, prefs: dict) -> dict:
        location = prefs.get("location")
        budget = prefs.get("budget")
        food_type = prefs.get("food_type")
        mood = prefs.get("mood")
        time_based = prefs.get("time_based")
        dietary_restriction = prefs.get("dietary_restriction")

        # Mulai dari semua restoran (flat list)
        candidates = self.restaurants

        # Filter location & budget
        if location:
            candidates = [r for r in candidates if r.get("location") == location]
        if budget:
            candidates = [r for r in candidates if r.get("budget") == budget]

        # Filter food_type
        if food_type:
            candidates = [
                r for r in candidates
                if (isinstance(r["food_type"], list) and food_type in r["food_type"])
                or (isinstance(r["food_type"], str) and r["food_type"] == food_type)
            ]

        # Filter mood
        if mood:
            candidates = [
                r for r in candidates
                if (isinstance(r["mood"], list) and mood in r["mood"])
                or (isinstance(r["mood"], str) and r["mood"] == mood)
            ]

        # Filter time_based
        if time_based:
            candidates = [
                r for r in candidates
                if (
                    (isinstance(r["time_based"], list) and (time_based in r["time_based"] or "24h" in r["time_based"]))
                    or (isinstance(r["time_based"], str) and (r["time_based"] == time_based or r["time_based"] == "24h"))
                )
            ]

        # Filter dietary_restriction
        if dietary_restriction:
            candidates = [
                r for r in candidates
                if (r.get("dietary_restriction") == dietary_restriction)
                or (dietary_restriction.lower() in str(r.get("dietary_restriction","")).lower())
            ]

        if not candidates:
            return {"error": f"Tidak ada restoran yang cocok dengan kriteria {prefs}", "matches": []}

        return {"matches": [r["name"] for r in candidates], "restaurants": candidates}

