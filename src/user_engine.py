import os
import json
import random
from conversation import ConversationEngine

class UserEngine:
    """
    User Interaction Specialist Engine
    Mengurus percakapan, mood detection, time detection, dietary rules,
    serta formatting response agar bisa diintegrasikan ke Discord.
    """
    def __init__(self, db_path=None):
        # otomatis cari file restaurants.json di folder ../data
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # folder src
            db_path = os.path.join(base_dir, "..", "data", "restaurant.json")

        with open(db_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        self.restaurants = []
        for location, budgets in raw_data.items():
            for budget, rest_list in budgets.items():
                for r in rest_list:
                    r["location"] = location
                    r["budget"] = budget
                    self.restaurants.append(r)
        self.conversation_engine = ConversationEngine()

    def process_message(self, user_input: str) -> str:

        return self.conversation_engine.reply(user_input)

    def get_recommendation(self, context: str) -> dict:
        """
        Cari rekomendasi restoran berdasarkan context (mood, time, diet, food_type).
        """
        candidates = []
        for r in self.restaurants:
            if not isinstance(r, dict):
                continue

            # Filter diet
            if context.get("diet") and context["diet"] != "none":
                if r.get("dietary_restriction") and context["diet"] not in r["dietary_restriction"]:
                    continue
            # Filter time
            if context.get("time") and context["time"] != "anytime":
                if "time_based" in r:
                    if isinstance(r["time_based"], list):
                        if context["time"] not in r["time_based"]:
                            continue
                    elif r["time_based"] != context["time"] and r["time_based"] != "24h":
                        continue
            # Filter mood (optional, if you store mood in restaurant)
            if context.get("mood") and context["mood"] != "neutral":
                if "mood" in r:
                    if isinstance(r["mood"], list):
                        if context["mood"] not in r["mood"]:
                            continue
                    elif r["mood"] != context["mood"]:
                        continue
            candidates.append(r)

        if not candidates:
            return {"error": "Tidak ditemukan rekomendasi yang cocok.", "context": context}

        return random.choice(candidates)

# ✅ Interactive Testing
if __name__ == "__main__":
    ue = UserEngine()

    print("=== FoodBot UserEngine Testing ===")
    print("Ketik 'quit' untuk keluar.\n")

    while True:
        # print("\n")
        user_msg = input("USER: ")
        if user_msg.lower() in ["quit", "exit", ""]:
            break

        result = ue.process_message(user_msg)
        print("BOT :", result["reply"])
        print("Meta:", {k: v for k, v in result.items() if k != "reply"})
        print("\n")

        recommendation = ue.get_recommendation(result)
        if "error" in recommendation:
            print("REKOMENDASI:", recommendation["error"])
        else:
            print("REKOMENDASI:", recommendation.get("name", recommendation))
        print("\n")



# ✅ Testing mandiri
# if __name__ == "__main__":
    # ue = UserEngine()

    # test_inputs = [
    #     "aku lagi stress dan pengen makan malam halal",
    #     "gue bosen, ada snack buat midnight?",
    #     "saya vegetarian, mau cari makan siang",
    #     "aku happy banget, mau traktiran!"
    # ]

    # for msg in test_inputs:
    #     result = ue.process_message(msg)
    #     print("\nUSER:", msg)
    #     print("BOT :", result["reply"])
    #     print("Meta:", {k: v for k, v in result.items() if k != "reply"})
