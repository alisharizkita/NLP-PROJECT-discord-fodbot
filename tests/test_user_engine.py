import sys
import os

# Tambahkan path src agar bisa import UserEngine
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from user_engine import UserEngine

if __name__ == "__main__":
    ue = UserEngine()

    print("=== FoodBot UserEngine Testing ===")
    print("Ketik 'quit' untuk keluar.\n")

    while True:
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