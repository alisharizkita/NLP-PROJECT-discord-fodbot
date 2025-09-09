# conversation.py
import re
from reflection import reflect
import datetime

class ConversationEngine:
    def __init__(self):
        self.context = {}

    def detect_mood(self, text: str) -> str:
        """
        Deteksi mood / craving user.
        """
        mood_patterns = {
            "stress": r"(stress|pusing|capek|lelah|males)",
            "happy": r"(senang|bahagia|happy|hore)",
            "tired": r"(ngantuk|lelah|capek|letih)",
            "sick": r"(sakit|flu|demam|batuk|masuk angin)",
            "bored": r"(bosen|gabut|bosan|garing)",
            "celebration": r"(ulang tahun|traktir|syukuran|merayakan)"
        }

        for mood, pattern in mood_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return mood
        return "neutral"

    def detect_time(self, text: str, current_hour: int = None) -> str:
        if re.search(r"(pagi|sarapan|breakfast)", text, re.IGNORECASE):
            return "breakfast"
        elif re.search(r"(siang|lunch|makan siang)", text, re.IGNORECASE):
            return "lunch"
        elif re.search(r"(sore|afternoon|makan sore)", text, re.IGNORECASE):
            return "afternoon"
        elif re.search(r"(malam|dinner|makan malam)", text, re.IGNORECASE):
            return "dinner"
        elif re.search(r"(midnight|tengah malam|begadang)", text, re.IGNORECASE):
            return "midnight"
        
        if current_hour is None:
            current_hour = datetime.datetime.now().hour
        elif 5 <= current_hour < 11:
            return "breakfast"
        elif 11 <= current_hour < 15:
            return "lunch"
        elif 15 <= current_hour < 18:
            return "afternoon"
        elif 18 <= current_hour < 22:
            return "dinner"
        elif 22 <= current_hour or current_hour < 5:
            return "midnight"

    def detect_diet(self, text: str) -> str:
        """
        Deteksi dietary restriction.
        """
        if re.search(r"(halal)", text, re.IGNORECASE):
            return "halal"
        elif re.search(r"(vegetarian|vegan|sayur)", text, re.IGNORECASE):
            return "vegetarian"
        elif re.search(r"(allerg(y|i)|alergi)", text, re.IGNORECASE):
            return "allergy"
        return "none"

    def reply(self, user_input: str) -> str:
        """
        Generate jawaban berdasarkan input user.
        """
        reflected = reflect(user_input)
        mood = self.detect_mood(user_input)
        time = self.detect_time(user_input)
        diet = self.detect_diet(user_input)

        response = f"Kamu bilang '{reflected}'. "

        if mood != "neutral":
            response += f"Aku rasa kamu lagi {mood}. "
        if time != "anytime":
            response += f"Sepertinya kamu butuh rekomendasi untuk {time}. "
        if diet != "none":
            response += f"Dan kamu butuh opsi {diet}. "

        if "makan" in user_input or "rekomendasi" in user_input:
            self.context["wants_food"] = True
            response += "Mau aku carikan rekomendasi makanan? "
        else:
            response += "Bisa ceritakan lebih detail tentang craving kamu? "

        if (("mau" in user_input) or ("pengen" in user_input)) and self.context["wants_food"]:
            response += "Mau makanan seperti nasi, mie, western, atau snack?"

        return response

# Test cepat
if __name__ == "__main__":
    bot = ConversationEngine()
    print(bot.reply("aku lagi stress dan pengen makan malam halal"))
