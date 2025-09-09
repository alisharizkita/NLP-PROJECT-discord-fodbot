import re

reflections = {
    "saya": "kamu",
    "aku": "kamu",
    "gue": "kamu",
    "gua": "kamu",
    "kami": "kalian",
    "kita": "kalian",

    "kamu": "saya",
    "anda": "saya",
    "kalian": "kami",

    "aku ingin": "kamu ingin",
    "saya ingin": "kamu ingin",
    "aku butuh": "kamu butuh",
    "saya butuh": "kamu butuh",

    "punya saya": "punya kamu",
    "punya kamu": "punya saya",
}

def reflect(sentence: str) -> str:
    """
    Ubah kata ganti dalam kalimat agar bot bisa merespons lebih natural.
    """
    words = sentence.lower().split()
    reflected_words = []

    for word in words:
        if word in reflections:
            reflected_words.append(reflections[word])
        else:
            reflected_words.append(word)

    return " ".join(reflected_words)

# Test
if __name__ == "__main__":
    print(reflect("aku butuh rekomendasi makanan"))
    # Output → "kamu butuh rekomendasi makanan"
