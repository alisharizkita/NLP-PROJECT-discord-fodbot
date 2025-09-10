import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from food_engine import FoodRecommendationEngine
from food_patterns import FoodPatterns

# Load token dari .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

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

@bot.command(name="start", aliases=["mulai"])
async def start_chat(ctx):
    user_id = ctx.author.id

    # Reset session lama jika ada
    if user_id in user_sessions:
        del user_sessions[user_id]

    # Buat session baru
    user_sessions[user_id] = {"step": 0, "prefs": {}}

    await ctx.send("Halo👋! Aku food chatbot yang siap bantu kasih rekomendasi makanan🍽️")
    await ctx.send("Kamu bisa ketik '!start' atau '!mulai' kapan saja untuk mulai ulang ➡️")
    await ctx.send(questions[0][1])

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Abaikan pesan yang merupakan command
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)  # tetap jalankan command
        return

    user_id = message.author.id
    content = message.content.strip()

    # Kalau user belum mulai chat → abaikan
    if user_id not in user_sessions:
        return

    session = user_sessions[user_id]
    step = session["step"]

    # Tangani pertanyaan saat ini
    if step < len(questions):
        key, _ = questions[step]
        content = message.content.strip()

        # Skip jika user ketik "\" atau enter
        if key == "dietary_restriction" and content in ["", "\\"]:
            session["prefs"][key] = "none"
        else:
            parsed = patterns.detect(content)
            if key in parsed:
                session["prefs"][key] = parsed[key]
            else:
                session["prefs"][key] = content


        # Naik ke pertanyaan berikutnya
        session["step"] += 1

        if session["step"] < len(questions):
            await message.channel.send(questions[session["step"]][1])
        else:
            # Semua pertanyaan selesai → kasih rekomendasi
            result = engine.get_recommendation(session["prefs"])
            if "error" in result:
                await message.channel.send(f"❌ {result['error']}")
            else:
                await message.channel.send("🍽️ Rekomendasi restoran:")
                for r in result["restaurants"]:
                    await message.channel.send(f"- {r['name']} ({r['specialty']})")
            # Reset session
            del user_sessions[user_id]

if __name__ == "__main__":
    bot.run(TOKEN)
