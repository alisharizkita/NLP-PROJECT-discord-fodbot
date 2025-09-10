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

        # Mulai filter
        candidates = []

        # Filter lokasi dan budget dulu, tapi jika kosong ambil semua
        locations_to_check = [location] if location else self.restaurants.keys()
        for loc in locations_to_check:
            loc_bucket = self.restaurants.get(loc, {})
            budgets_to_check = [budget] if budget else loc_bucket.keys()
            for b in budgets_to_check:
                candidates.extend(loc_bucket.get(b, []))

        # Filter lainnya hanya jika ada
        if food_type:
            candidates = [
                r for r in candidates
                if (isinstance(r["food_type"], list) and food_type in r["food_type"])
                or (isinstance(r["food_type"], str) and r["food_type"] == food_type)
            ]
        if mood:
            candidates = [
                r for r in candidates
                if (isinstance(r["mood"], list) and mood in r["mood"])
                or (isinstance(r["mood"], str) and r["mood"] == mood)
            ]
        if time_based:
            candidates = [
                r for r in candidates
                if (isinstance(r["time_based"], list) and time_based in r["time_based"])
                or (isinstance(r["time_based"], str) and r["time_based"] == time_based)
            ]
        if dietary_restriction:
            candidates = [
                r for r in candidates
                if (isinstance(r.get("dietary_restriction", ""), list) and dietary_restriction in r.get("dietary_restriction", ""))
                or (isinstance(r.get("dietary_restriction", ""), str) and dietary_restriction in r.get("dietary_restriction", ""))
            ]

        if not candidates:
            return {"error": f"Tidak ada restoran yang cocok dengan kriteria {prefs}", "matches": []}

        return {"matches": [r["name"] for r in candidates], "restaurants": candidates}
