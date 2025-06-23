import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# === User Input ===
def get_user_input():
    try:
        num_questions = int(input("How many questions to generate? "))
        difficulty = input("Enter difficulty (Too Easy, Easy, Medium, Tough, Too Tough): ").strip().title()
        return num_questions, difficulty
    except Exception as e:
        print("❌ Invalid input:", e)
        exit()

# === Difficulty Settings ===
def get_difficulty_settings(level):
    settings = {
        "Too Easy":     {"common": 6, "extra": 2, "base": 50,  "set_len": 8,  "seconds": 8},
        "Easy":         {"common": 5, "extra": 3, "base": 60,  "set_len": 9,  "seconds": 10},
        "Medium":       {"common": 4, "extra": 4, "base": 80,  "set_len": 10, "seconds": 12},
        "Tough":        {"common": 4, "extra": 5, "base": 100, "set_len": 12, "seconds": 14},
        "Too Tough":    {"common": 4, "extra": 8, "base": 150, "set_len": 20, "seconds": 16}
    }
    return settings.get(level, settings["Medium"])

# === Set Generator ===
def generate_sets(settings, difficulty):
    base_numbers = list(range(1, settings["base"] + 1))
    common = random.sample(base_numbers, settings["common"])
    used = set(common)
    extra_pool = list(set(base_numbers) - used)

    def noisy_set():
        fake_commons = []
        if difficulty == "Too Tough":
            fake_commons = random.sample(extra_pool, 2)
        items = common + random.sample(extra_pool, settings["extra"]) + fake_commons
        return sorted(random.sample(items, min(settings["set_len"], len(items))))

    return noisy_set(), noisy_set(), noisy_set(), common

# === Option Generator ===
def generate_options(correct_common, extra_pool, difficulty):
    correct = sorted(random.sample(correct_common, min(4, len(correct_common))))
    options = [correct]

    attempts = 0
    while len(options) < 4 and attempts < 20:
        if difficulty == "Too Tough":
            wrong = sorted(random.sample(correct_common + extra_pool, 4))
        else:
            wrong = sorted(random.sample(correct_common, 2) + random.sample(extra_pool, 2))

        if wrong not in options:
            options.append(wrong)
        attempts += 1

    random.shuffle(options)
    return correct, options

# === Image Generator ===
def create_image(setA, setB, setC, q_no, difficulty):
    img = Image.new('RGB', (420, 280), color=(240, 244, 248))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 18)
        set_font = ImageFont.truetype("arial.ttf", 14)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        set_font = ImageFont.load_default()
        small_font = ImageFont.load_default()


    sets = [
        (setA, (249, 155, 130), 50),
        (setB, (125, 201, 255), 115),
        (setC, (142, 224, 149), 180),
    ]
    for items, color, y in sets:
        draw.rounded_rectangle([10, y, 410, y + 45], radius=8, fill=color, outline="black", width=2)
        display_text = " ".join(map(str, sorted(items)))
        draw.text((20, y + 5), display_text, fill="black", font=set_font)

    draw.text((280, 260), "Made by staWro", font=small_font, fill="gray")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# === Upload Screenshot ===
def upload_image(image_buffer):
    files = {'screenshot': ("screenshot.png", image_buffer, "image/png")}
    try:
        res = requests.post("https://backend.stawro.com/stawro/upload.php", files=files)
        if res.status_code == 200 and res.json().get("status") == "success":
            return f"https://backend.stawro.com/stawro/{res.json()['path']}"
        else:
            print("❌ Upload failed:", res.text)
            return None
    except Exception as e:
        print("❌ Upload error:", e)
        return None

# === Post Question to Server ===
def post_question(correct, options, difficulty, image_url, seconds):
    body = {
        "question": "Find numbers that are common to all 3 sets.",
        "answer": ", ".join(map(str, correct)),
        "a": ", ".join(map(str, options[0])),
        "b": ", ".join(map(str, options[1])),
        "c": ", ".join(map(str, options[2])),
        "d": ", ".join(map(str, options[3])),
        "language": "English",
        "category": "Set_Theory",
        "difficulty": difficulty,
        "type": "Mental Ability",
        "image": image_url,
        "seconds": str(seconds)
    }

    try:
        res = requests.post("http://localhost/api/question", json=body)
        if res.ok:
            print(f"✅ Q Posted — {difficulty} ({seconds}s)")
        else:
            print("❌ Error posting:", res.text)
    except Exception as e:
        print("❌ Exception posting:", e)

# === Main Controller ===
def main():
    num_questions, difficulty = get_user_input()
    settings = get_difficulty_settings(difficulty)
    seconds = settings["seconds"]

    for i in range(1, num_questions + 1):
        setA, setB, setC, common = generate_sets(settings, difficulty)
        extra_pool = list(set(setA + setB + setC) - set(common))
        correct, options = generate_options(common, extra_pool, difficulty)
        image_buffer = create_image(setA, setB, setC, i, difficulty)
        image_url = upload_image(image_buffer)

        if image_url:
            post_question(correct, options, difficulty, image_url, seconds)

if __name__ == "__main__":
    main()
