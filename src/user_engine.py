# user_engine.py
from conversation import ConversationEngine

class UserEngine:
    """
    User Interaction Specialist Engine
    Mengurus percakapan, mood detection, time detection, dietary rules,
    serta formatting response agar bisa diintegrasikan ke Discord.
    """
    def __init__(self):
        self.conversation_engine = ConversationEngine()

    def process_message(self, user_input: str) -> dict:
        """
        Proses pesan dari user → kembalikan structured response
        untuk diintegrasikan dengan Discord bot.
        """
        reply_text = self.conversation_engine.reply(user_input)

        # Simpan konteks (jika dibutuhkan untuk memory)
        mood = self.conversation_engine.detect_mood(user_input)
        time = self.conversation_engine.detect_time(user_input)
        diet = self.conversation_engine.detect_diet(user_input)

        response = {
            "reply": reply_text,
            "mood": mood,
            "time": time,
            "diet": diet,
            "raw_input": user_input
        }

        return response

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
