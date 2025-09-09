import re

class FoodPatterns:
    def __init__(self):
        # Budget patterns
        self.budget_patterns = [
            (r'budget\s*([0-9]+)\s*(ribu|rb|k)', self.extract_budget_number),
            (r'([0-9]+)\s*(ribu|rb|k)', self.extract_budget_number),
            (r'murah|hemat|budget\s*kecil|kantong\s*tipis|kantong\s*kering', 'low'),
            (r'sedang|standar|biasa\s*aja|normal|affordable|lumayan\s*banyak', 'medium'), 
            (r'bebas|mahal\s*gpp\s*gapapa|unlimited|banyak\s*uang|self\s*reward|reward|enak', 'high')
        ]

        # Location patterns  
        self.location_patterns = [
            (r'kampus|dalam\s*kampus|area\s*kampus|kantin\s*kampus|di\s*kampus', 'campus'),
            (r'luar\s*kampus|keluar\s*kampus|jauh\s*kampus', 'off-campus'),
            (r'delivery|bisa\s*diantar|mager|males\s*keluar|order\s*online|pesan\s*online|gofood|grabfood|ojol|shopeefood', 'delivery'),
        ]
        
        # Food type patterns
        self.food_type_patterns = [
            (r'nasi|rice|indonesian|makan\s*kenyang', 'rice'),
            (r'mie|noodle|bakmi|mie ayam|kuah', 'noodle'),
            (r'western|burger|pizza|steak|sandwich|pasta', 'western'),
            (r'sushi|ramen|bento|sashimi|takoyaki', 'japanese'),
            (r'minuman|drink|coffee|kopi|jus', 'beverages'),
            (r'dessert|manis|ice\s*cream|sweet|es|gelato', 'desserts')
        ]

    def extract_budget_number(self, match):
        number = int(match.group(1))  # ambil angka
        unit = match.group(2) if match.lastindex and match.lastindex >= 2 else None

        if unit in ['ribu', 'rb', 'k']:
            number *= 1000

        # Kelompokkan ke kategori
        if number < 20000:
            return "low"
        elif 20000 <= number <= 50000:
            return "medium"
        else:
            return "high"

    def detect(self, text: str) -> dict:
        """
        Deteksi budget, lokasi, dan tipe makanan dari input user.
        """
        text = text.lower()
        result = {"budget": None, "location": None, "food_type": None}

        # Budget
        for pattern, label in self.budget_patterns:
            match = re.search(pattern, text)
            if match:
                if callable(label):  # kalau fungsi -> panggil
                    result["budget"] = label(match)
                else:
                    result["budget"] = label
                break

        # Location
        for pattern, label in self.location_patterns:
            if re.search(pattern, text):
                result["location"] = label
                break

        # Food type
        for pattern, label in self.food_type_patterns:
            if re.search(pattern, text):
                result["food_type"] = label
                break

        return result
