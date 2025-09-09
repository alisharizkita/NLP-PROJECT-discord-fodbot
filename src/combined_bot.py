import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from user_engine import UserEngine
from food_engine import FoodRecommendationEngine

class CombinedBot:
    def __init__(self):
        self.user_engine = UserEngine()
        self.food_engine = FoodRecommendationEngine()

    def process_message(self, user_input: str) -> dict:
        # Extract mood, time, diet
        context1 = self.user_engine.conversation_engine.reply(user_input)
        # Extract budget, location, food_type
        context2 = self.food_engine.process(user_input)

        # Merge contexts
        merged_context = {**context1, **context2}

        # Get recommendation using merged context
        recommendation = self.user_engine.get_recommendation(merged_context)

        return {
            "reply": context1["reply"],
            "meta": merged_context,
            "recommendation": recommendation
        }

if __name__ == "__main__":
    bot = CombinedBot()
    print("=== Combined FoodBot ===")
    print("Ketik 'quit' untuk keluar.\n")
    while True:
        user_msg = input("USER: ")
        if user_msg.lower() in ["quit", "exit", ""]:
            break
        result = bot.process_message(user_msg)
        print("BOT :", result["reply"])
        print("Meta:", result["meta"])
        if "error" in result["recommendation"]:
            print("REKOMENDASI:", result["recommendation"]["error"])
        else:
            print("REKOMENDASI:", result["recommendation"].get("name", result["recommendation"]))
        print("\n")