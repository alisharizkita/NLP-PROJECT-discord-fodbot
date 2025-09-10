import re

class FoodPatterns:
    def __init__(self):
        # Location patterns
        self.location_patterns = [
            (r'\b(?:luar|keluar|di\s*luar|luar\s*kampus|keluar\s*kampus|jauh\s*kampus)\b', 'off-campus'),
            (r'\b(?:delivery|bisa\s*diantar|mager|males\s*keluar|order\s*online|pesan\s*online|gofood|grabfood|ojol|shopeefood)\b', 'delivery'),
            (r'\b(?:dalam\s*kampus|di\s*kampus|area\s*kampus|kantin\s*kampus|kampus)\b', 'campus'),
        ]

        # Food type patterns
        self.food_type_patterns = [
            (r'\b(?:japanese|sushi|ramen|bento|sashimi|takoyaki|yakiniku)\b', 'japanese'),
            (r'\b(?:nasi|rice|indonesian|makan\s*kenyang)\b', 'rice'),
            (r'\b(?:mie|noodle|bakmi|mie\s*ayam|kuah|mi)\b', 'noodle'),
            (r'\b(?:western|burger|pizza|steak|sandwich|pasta)\b', 'western'),
            (r'\b(?:minuman|drink|coffee|kopi|jus|es|seger|juice)\b', 'beverages'),
            (r'\b(?:dessert|manis|ice\s*cream|sweet|es|gelato)\b', 'desserts'),
            (r'\b(?:gudeg|jawa|nusantara|tradisional|traditional)\b', 'traditional'),
            (r'\b(?:korean|samgyeopsal|bbq)\b', 'korean'),
        ]

        # Budget patterns
        self.budget_patterns = [
            (r'([0-9]+)', self.extract_budget_number),
            (r'budget\s*([0-9]+)\s*(ribu|rb|k)', self.extract_budget_number),
            (r'([0-9]+)\s*(ribu|rb|k)', self.extract_budget_number),
            (r'murah|hemat|budget\s*kecil|kantong\s*tipis|kantong\s*kering', 'low'),
            (r'sedang|standar|biasa\s*aja|normal|affordable|lumayan\s*banyak', 'medium'),
            (r'bebas|mahal\s*gpp|gapapa|unlimited|banyak\s*uang|self\s*reward|reward|traktir', 'high'),
        ]

        # Mood patterns
        self.mood_patterns = [
            (r'stress|pusing|capek\s*kuliah', 'stress'),
            (r'tired|lelah|ngantuk', 'tired'),
            (r'happy|senang|bahagia', 'happy'),
            (r'neutral|biasa\s*aja', 'neutral'),
            (r'bored|gabut|bosan|sedih', 'bored'),
            (r'celebration|merayakan|ulang\s*tahun|traktiran|traktir|party', 'celebration'),
            (r'sakit|flu|kurang\s*enak', 'sick'),
            (r'casual|santai|nongkrong', 'casual'),
        ]

        # Time based patterns
        self.time_patterns = [
            (r'breakfast|sarapan|pagi', 'breakfast'),
            (r'lunch|siang|makan\s*siang', 'lunch'),
            (r'afternoon|sore', 'afternoon'),
            (r'dinner|malam|makan\s*malam', 'dinner'),
            (r'midnight|tengah\s*malam|larut\s*malam', 'midnight'),
            (r'24h|sepanjang\s*hari|kapan\s*saja', '24h'),
        ]

        # Dietary restriction patterns
        self.dietary_patterns = [
            (r'halal', 'halal'),
            (r'vegetarian|veggie', 'vegetarian options'),
            (r'vegan', 'vegan'),
            (r'dairy\s*free|bebas\s*susu', 'dairy-free sorbet options'),
            (r'vegetarian\s*friendly', 'vegetarian-friendly options'),
        ]

    def extract_budget_number(self, match):
        amount = int(match.group(1))
        unit = match.group(2).lower() if match.lastindex >= 2 and match.group(2) else ""

        # Convert based on unit
        if unit in ["k", "rb", "ribu"]:
            amount *= 1000
        if amount <= 15000:
            return "low"
        elif amount <= 30000:
            return "medium"
        else:
            return "high"

    def detect(self, text):
        result = {}

        for patterns, key in [
            (self.location_patterns, "location"),
            (self.food_type_patterns, "food_type"),
            (self.budget_patterns, "budget"),
            (self.mood_patterns, "mood"),
            (self.time_patterns, "time_based"),
            (self.dietary_patterns, "dietary_restriction"),
        ]:
            for pattern, value in patterns:
                match = re.search(pattern, text, flags=re.IGNORECASE)
                if match:
                    if callable(value):
                        result[key] = value(match)
                    else:
                        result[key] = value
                    break  # stop at first match per category

        return result
