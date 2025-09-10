# 🍜 *Discord Campus Food Recommendation Bot*

A rule-based chatbot with pronoun reflection that provides personalized food recommendations for university students around UGM campus area.

## 📋 *Project Overview*

This chatbot helps students make quick food decisions based on their budget, location preferences, mood, and time constraints. Built using regex pattern matching and natural language processing techniques with Indonesian language support.

## 🎯 *Key Features*

- Rule-based recommendation using regex pattern matching
- Pronoun reflection for natural Indonesian conversations
- Multi-factor analysis (budget, location, mood, time)
- Discord integration for easy accessibility
- UGM campus-focused restaurant database

## 🔧 *Technology Stack*

- Language: Python 3.8+
- Platform: Discord (discord.py)
- NLP: Regex patterns + Pronoun reflection
- Database: JSON-based restaurant data
-

## 📦 *Setup*

1. Clone repository

git clone https://github.com/alisharizkita/NLP-PROJECT-discord-fodbot.git
cd NLP-PROJECT-discord-fodbot


2. Buat virtual environment (opsional tapi disarankan)

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows


3. Install dependencies

pip install -r requirements.txt


4. Atur environment variable
Buat file .env di root folder:

DISCORD_TOKEN=your_discord_bot_token

## ▶️ *Run*

Untuk menjalankan bot Discord:

python src/discord_bot.py

## 💡 *Example Usage*

User di Discord:

!start


FoodBot Response:

Halo👋! Aku food chatbot yang siap bantu kasih rekomendasi makanan🍽️
Kamu bisa ketik '!start' atau '!mulai' kapan saja untuk mulai ulang ➡️
Kamu lagi pengen makan apa nih?😁


User di Discord:

nasi


FoodBot Response:

Kamu sekarang lagi di mana?📍


User di Discord:

di kampus


FoodBot Response:

Berapa budget yang kamu punya?💸


User di Discord:

20000


FoodBot Response:

Mood kamu lagi gimana sekarang?💓

User di Discord:

biasa aja


FoodBot Response:

Mau buat sarapan, makan siang, atau makan malam nih?⏰


User di Discord:

mau makan siang


FoodBot Response:

Apa dietary restriction kamu?🚫


User di Discord:

gak ada


FoodBot Response:

🍽️ Rekomendasi restoran:
- Warmindo Sami Asih (Nasi Orak Arik)
- Kedai Den Bagoes (Nasi Goreng Tuna)
- SGPC Bu Wiryo 1959 (Nasi Pecel (SGPC))
