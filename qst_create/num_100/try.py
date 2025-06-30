import random
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# === CONFIG ===
UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
POST_ENDPOINT = "http://192.168.31.44/api/question"
FONT_PATH = "arial.ttf"  # You can change this if needed

# === Ask for user inputs ===
try:
    num_questions = int(input("How many questions do you want to generate? "))
    difficulty = input("Enter difficulty (Too Easy, Easy, Medium, Tough, Too Tough): ").strip()
    assert difficulty in ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]
except Exception as e:
    print(f"Error: {e}")
    exit()

def get_difficulty_params(difficulty):
    """Return number of wrong items and how confusing they are"""
    if difficulty == "Too Easy":
        return random.randint(2, 3), 10  # Big gaps
    elif difficulty == "Easy":
        return random.randint(3, 4), 7
    elif difficulty == "Medium":
        return random.randint(5, 7), 5
    elif difficulty == "Tough":
        return random.randint(6, 10), 3
    elif difficulty == "Too Tough":
        return random.randint(10, 15), 1  # Very close numbers

def generate_question():
    correct_series = list(range(1, 101))
    display_series = correct_series[:]

    wrong_count, confusion_range = get_difficulty_params(difficulty)
    wrong_indexes = set()

    while len(wrong_indexes) < wrong_count:
        idx = random.randint(0, 99)
        wrong_indexes.add(idx)

    for idx in wrong_indexes:
        while True:
            offset = random.randint(-confusion_range, confusion_range)
            wrong = correct_series[idx] + offset
            if 1 <= wrong <= 100 and wrong != correct_series[idx]:
                display_series[idx] = wrong
                break

    correct_answer = wrong_count
    options = {correct_answer}
    while len(options) < 4:
        offset = random.randint(-2, 2)
        opt = correct_answer + offset
        if 1 <= opt <= 100:
            options.add(opt)
    options = sorted(list(options))
    
    return display_series, correct_answer, options

def draw_grid(display_series):
    img_width, img_height = 400, 250
    image = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)

    font_size = 14
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except:
        font = ImageFont.load_default()

    cols = 10
    rows = 10
    margin = 5
    box_width = (img_width - 2 * margin) // cols
    box_height = (img_height - 2 * margin) // rows

    for i, num in enumerate(display_series):
        row = i // cols
        col = i % cols
        x = margin + col * box_width
        y = margin + row * box_height
        draw.rectangle([x, y, x + box_width - 2, y + box_height - 2], fill="#b1def5", outline="black")
        draw.text((x + 8, y + 8), str(num), fill="black", font=font)
    return image

def upload_image(image):
    buffer = io.BytesIO()
    image.save(buffer, format="WEBP")
    buffer.seek(0)

    files = {'screenshot': ('screenshot.webp', buffer, 'image/webp')}
    try:
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        data = response.json()
        if data.get("status") and data.get("path"):
            return f"https://backend.stawro.com/stawro/{data['path']}"
        else:
            print("❌ Upload failed.")
            return None
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def post_question(image_path, correct_answer, options):
    payload = {
        "question": "How many wrong numbers are present in the grid?",
        "answer": str(correct_answer),
        "a": str(options[0]),
        "b": str(options[1]),
        "c": str(options[2]),
        "d": str(options[3]),
        "language": "English",
        "category": "Counting_100",
        "difficulty": difficulty,
        "type": "Mental Ability",
        "image": image_path,
        "seconds": "10"
    }
    try:
        res = requests.post(POST_ENDPOINT, json=payload)
        if res.status_code == 200:
            print("✅ Question posted to database!")
        else:
            print(f"❌ Failed to post question. Status code: {res.status_code}")
    except Exception as e:
        print(f"❌ Error posting question: {e}")

# === MAIN LOOP ===
for _ in range(num_questions):
    display_series, correct_answer, options = generate_question()
    image = draw_grid(display_series)
    image_url = upload_image(image)
    if image_url:
        post_question(image_url, correct_answer, options)
