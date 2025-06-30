# everything ok

import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
UPLOAD_URL = "https://backend.stawro.com/stawro/upload.php"
POST_URL = "http://192.168.31.44/api/question"
CHARS = "abcdefghijklmnopqrstuvwxyz"

# Difficulty Configs
DIFFICULTY_SETTINGS = {
    "Too Easy": {"code_length": 6, "seconds": 10},
    "Easy": {"code_length": 8, "seconds": 12},
    "Medium": {"code_length": 12, "seconds": 16},
    "Tough": {"code_length": 16, "seconds": 18},
    "Too Tough": {"code_length": 20, "seconds": 18}
}

def get_random_code(length):
    return ''.join(random.choice(CHARS) for _ in range(length))

def get_new_char(exclude):
    while True:
        ch = random.choice(CHARS)
        if ch != exclude:
            return ch

def mutate_two_letters(original):
    arr = list(original)
    first_index = random.randint(0, len(arr) - 1)
    second_index = first_index
    while second_index == first_index:
        second_index = random.randint(0, len(arr) - 1)
    arr[first_index] = get_new_char(arr[first_index])
    arr[second_index] = get_new_char(arr[second_index])
    return ''.join(arr)

def generate_options(correct):
    opts = [correct]
    while len(opts) < 4:
        mutated = mutate_two_letters(correct)
        if mutated not in opts:
            opts.append(mutated)
    random.shuffle(opts)
    return opts

def render_code_to_image_bytes(code):
    width, height = 400, 250
    bg_color = (0, 0, 0)
    text_color = (255, 255, 255)
    font_size = 30

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), code, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), code, fill=text_color, font=font)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def upload_image_from_bytes(image_buffer):
    files = {'screenshot': ('screenshot.png', image_buffer, 'image/png')}
    response = requests.post(UPLOAD_URL, files=files, verify=False)
    try:
        result = response.json()
        print("🔍 Upload response:", result)
        return result
    except Exception as e:
        print("❌ Error parsing upload response:", str(e))
        return {}

def post_question(correct, options, image_path, difficulty, seconds):
    image_url = f"https://backend.stawro.com/stawro/{image_path}"
    payload = {
        "question": "Guess the correct code",
        "answer": correct,
        "a": options[0],
        "b": options[1],
        "c": options[2],
        "d": options[3],
        "language": "English",
        "category": "Code Guessing",
        "difficulty": difficulty,
        "type": "Mental Ability",
        "image": image_url,
        "seconds": str(seconds)
    }

    print("📤 Payload to POST:", payload)
    res = requests.post(POST_URL, json=payload)
    return res.status_code == 200

def run_auto(total_questions=5, difficulty="Medium"):
    settings = DIFFICULTY_SETTINGS.get(difficulty)
    if not settings:
        print("❌ Invalid difficulty selected.")
        return

    code_length = settings["code_length"]
    seconds = settings["seconds"]

    for i in range(1, total_questions + 1):
        print(f"\n--- Generating Question {i} ---")

        correct = get_random_code(code_length)
        options = generate_options(correct)

        image_buffer = render_code_to_image_bytes(correct)
        upload_result = upload_image_from_bytes(image_buffer)

        if upload_result.get("status"):
            uploaded_path = upload_result.get("path", "")
            if not uploaded_path:
                print("⚠️ Upload success but no path returned.")
                continue

            success = post_question(correct, options, uploaded_path, difficulty, seconds)
            if success:
                print("✅ Question posted successfully.")
            else:
                print("❌ Failed to post question to API.")
        else:
            print("❌ Image upload failed or invalid response.")

# 🔘 Ask user input and run
if __name__ == "__main__":
    try:
        total = int(input("How many questions to generate? "))
        level = input("Enter difficulty (Too Easy / Easy / Medium / Tough / Too Tough): ").strip()
        run_auto(total_questions=total, difficulty=level)
    except Exception as e:
        print("❌ Invalid input:", e)
