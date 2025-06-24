import random
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# === CONFIGURATION ===
UPLOAD_URL = "https://backend.stawro.com/stawro/upload.php"
POST_URL = "http://localhost/api/question"
CATEGORY = "OMR Challenge"
DIFFICULTY = "Medium"
LANGUAGE = "English"
TYPE = "Mental Ability"
SECONDS = "10"

# === 1. Generate Correct Number ===
def generate_random_number():
    return str(random.randint(1000000000, 9999999999))

# === 2. Generate Options with Center Digit Change ===
def generate_center_challenge_options(correct):
    options = [correct]
    center_indexes = [4, 5]
    used = {correct}
    while len(options) < 4:
        arr = list(correct)
        i = random.choice(center_indexes)
        new_digit = (int(arr[i]) + 1 + random.randint(0, 7)) % 10
        arr[i] = str(new_digit)
        new_option = ''.join(arr)
        if new_option not in used:
            options.append(new_option)
            used.add(new_option)
    random.shuffle(options)
    return options

# === 3. Render OMR Image ===
def create_omr_image(number):
    width, height = 400, 250
    col_width = width // len(number)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for idx, digit in enumerate(number):
        x = idx * col_width + col_width // 2
        for i in range(10):
            y = 20 + i * 20
            r = 8
            color = "#282c34" if str(i) == digit else "#dddddd"
            draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline="black")
            draw.text((x - 4, y - 5), str(i), fill="white" if str(i) == digit else "black", font=font)

    return img

# === 4. Upload Screenshot Image ===
def upload_image(image: Image.Image):
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        buffer.seek(0)
        files = {'screenshot': ("omr.png", buffer, 'image/png')}
        response = requests.post(UPLOAD_URL, files=files)
        return response.json()

# === 5. POST the Question ===
def post_question(correct, options, image_path):
    data = {
        "question": "What is the number shown in the OMR sheet?",
        "answer": correct,
        "a": options[0],
        "b": options[1],
        "c": options[2],
        "d": options[3],
        "language": LANGUAGE,
        "category": CATEGORY,
        "difficulty": DIFFICULTY,
        "type": TYPE,
        "image": f"https://backend.stawro.com/stawro/{image_path}",
        "seconds": SECONDS
    }
    response = requests.post(POST_URL, json=data)
    return response.json()

# === MAIN EXECUTION FLOW ===
if __name__ == "__main__":
    try:
        correct_number = generate_random_number()
        options = generate_center_challenge_options(correct_number)
        image = create_omr_image(correct_number)

        print(f"Correct: {correct_number}")
        print("Options:")
        for o in options:
            mark = "✅" if o == correct_number else "❌"
            print(f"  {o} {mark}")

        print("\n📤 Uploading image...")
        upload_response = upload_image(image)

        if upload_response.get("status") == "success":
            print("✅ Image uploaded!")
            image_path = upload_response.get("path")
            print("🌐 Image URL:", f"https://backend.stawro.com/stawro/{image_path}")
            print("📨 Posting question...")
            post_response = post_question(correct_number, options, image_path)
            print("✅ Question posted!", post_response)
        else:
            print("❌ Upload failed:", upload_response)

    except Exception as e:
        print("❌ Error:", e)
