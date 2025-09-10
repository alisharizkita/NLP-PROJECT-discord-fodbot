import discord
from discord.ext import commands
from food_engine import FoodRecommendationEngine
from food_patterns import FoodPatterns

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Engine & patterns
engine = FoodRecommendationEngine()
patterns = FoodPatterns()

# Session tiap user
user_sessions = {}

# Pertanyaan berurutan
questions = [
    ("food_type", "Kamu lagi pengen makan apa nih?😁 "),
    ("location", "Kamu sekarang lagi di mana?📍 "),
    ("budget", "Berapa budget yang kamu punya?💸 "),
    ("mood", "Mood kamu lagi gimana sekarang?💓 "),
    ("time_based", "Mau buat sarapan, makan siang, atau makan malam nih?⏰ "),
    ("dietary_restriction", "Apa dietary restriction kamu?🚫 "),
]

@bot.event
async def on_ready():
    print(f"✅ Bot sudah login sebagai {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    content = message.content.strip()

    # Kalau user ketik "mulai" → reset sesi
    if content.lower() == "mulai":
        user_sessions[user_id] = {"step": 0, "prefs": {}}
        await message.channel.send("Halo👋! Aku food chatbot yang siap bantu kasih rekomendasi makanan🍽️")
        await message.channel.send("Kamu bisa ketik 'mulai' kapan saja untuk mulai ulang.")
        await message.channel.send(questions[0][1])
        return

    # Kalau user belum mulai → abaikan
    if user_id not in user_sessions:
        return

    session = user_sessions[user_id]
    step = session["step"]

    if step < len(questions):
        key, qtext = questions[step]

        # Kalau user skip ("" atau "\") → langsung next
        if content not in ["", "\\"]:
            parsed = patterns.detect(content)
            if parsed.get(key):
                session["prefs"][key] = parsed[key]

        # Naik ke pertanyaan berikutnya
        session["step"] += 1
        if session["step"] < len(questions):
            next_q = questions[session["step"]][1]
            await message.channel.send(next_q)
        else:
            # Semua pertanyaan selesai → kasih rekomendasi
            result = engine.get_recommendation(session["prefs"])
            if "error" in result:
                await message.channel.send(result["error"])
            else:
                await message.channel.send("Restoran yang cocok dengan preferensimu:")
                for r in result["restaurants"]:
                    await message.channel.send(f"- {r['name']}")

            # Reset sesi setelah rekomendasi
            del user_sessions[user_id]
