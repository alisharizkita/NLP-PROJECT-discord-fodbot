import os
import discord
from food_engine import FoodRecommendationEngine
from food_patterns import FoodPatterns
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)
engine = FoodRecommendationEngine()
patterns = FoodPatterns()

# Track user states: {user_id: {"step": int, "prefs": dict}}
user_states = {}

questions = [
    ("food_type", "Kamu lagi pengen makan apa nih?😁"),
    ("location", "Kamu sekarang lagi di mana?📍"),
    ("budget", "Berapa budget yang kamu punya?💸"),
    ("mood", "Mood kamu lagi gimana sekarang?💓"),
    ("time_based", "Mau buat sarapan, makan siang, atau makan malam nih?⏰"),
    ("dietary_restriction", "Apa dietary restriction kamu?🚫"),
]

@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user or not message.guild:
        return

    user_id = str(message.author.id)
    content = message.content.strip()

    # Start new conversation if user not in state or says "mulai"
    if user_id not in user_states or content.lower() in ["mulai", "start", "halo", "hi"]:
        user_states[user_id] = {"step": 0, "prefs": {}}
        await message.channel.send(
            "Halo👋! Aku food chatbot yang siap bantu kasih rekomendasi makanan🍽️\n"
            "Kamu bisa ketik 'mulai' kapan saja untuk mulai ulang.\n\n"
            + questions[0][1]
        )
        return

    state = user_states[user_id]
    step = state["step"]
    prefs = state["prefs"]

    key, question = questions[step]

    # Handle skip
    if content.strip() in ["", "\\"]:
        step += 1
        if step < len(questions):
            state["step"] = step
            await message.channel.send(questions[step][1])
            return
    else:
        parsed = patterns.detect(content)
        if parsed.get(key):
            prefs[key] = parsed[key]

        step += 1
        if step < len(questions):
            state["step"] = step
            await message.channel.send(questions[step][1])
            return

    # All questions answered → recommendation
    result = engine.get_recommendation(prefs)
    if "error" in result:
        await message.channel.send(result["error"])
    else:
        reply = "Restoran yang cocok dengan preferensimu:\n"
        for r in result["restaurants"]:
            reply += f"- {r['name']}\n"
        await message.channel.send(reply)

    # Reset session
    user_states.pop(user_id, None)

if __name__ == "__main__":
    client.run(TOKEN)