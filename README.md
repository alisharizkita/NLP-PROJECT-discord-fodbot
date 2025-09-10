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

- Language: Python 3.11+
- Platform: Discord (discord.py)
- NLP: Regex patterns
- Database: JSON-based restaurant data

## 📦 *Setup*

1. Clone repository

```bash
git clone https://github.com/alisharizkita/NLP-PROJECT-discord-fodbot.git
cd NLP-PROJECT-discord-fodbot
```

2. Buat virtual environment (opsional tapi disarankan)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Atur environment variable
Buat file .env di root folder:

```bash
DISCORD_TOKEN=your
```

## ▶️ *Run*

Untuk menjalankan bot Discord:

```bash
python src/discord_bot.py
```
