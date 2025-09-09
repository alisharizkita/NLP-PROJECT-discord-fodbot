import re

class FoodPatterns:
    def __init__(self):
        # Budget patterns
        self.budget_patterns = [
            (r'budget\s*([0-9]+)\s*(ribu|rb|k)', self.extract_budget_number),
            (r'([0-9]+)\s*(ribu|rb|k)', self.extract_budget_number),
            (r'murah|hemat|budget\s*kecil|kantong\s*tipis|kantong\s*kering', 'low'),
            (r'sedang|standar|biasa\s*aja|normal|affordable|lumayan\*banyak', 'medium'), 
            (r'bebas|mahal\s*gpp\s*gapapa|unlimited|banyak\s*uang|self\*reward|reward', 'high')
        ]

        def extract_budget_number(self, match):
            number = int(match.group(1))  # ambil angka
            unit = match.group(2) if match.lastindex >= 2 else None  # ambil satuan (ribu, rb, k)

            if unit in ['ribu', 'rb', 'k']:
                number *= 1000

            # Kelompokkan ke kategori
            if number < 20000:
                return "low"
            elif 20000 <= number <= 50000:
                return "medium"
            else:
                return "high"
        
        # Location patterns  
        self.location_patterns = [
            (r'kampus|dalam\s*kampus|area\s*kampus|kantin\*kampus|di\*kampus', 'campus'),
            (r'luar\s*kampus|keluar\s*kampus|jauh\s*kampus', 'off-campus'),
            (r'delivery|bisa\*diantar|mager|males\*keluar|order\*online|pesan\s*online|gofood|grabfood|ojol|shopeefood', 'delivery'),
        ]
        
        # Food type patterns
        self.food_type_patterns = [
            (r'nasi|rice|indonesian|makan\*kenyang', 'rice'),
            (r'mie|noodle|bakmi|mie\*ayam|kuah|', 'noodles'),
            (r'western|burger|pizza|steak|sandwich|pasta', 'western'),
            (r'minuman|drink|coffee|kopi|jus', 'beverages'),
            (r'dessert|manis|ice\s*cream|sweet|es|gelato', 'desserts')
        ]

        # Mood Patterns
        # isi disini iaa gab ttg mood

        # Time Patterns

        # Dietary Patterns