import random
import requests
from PIL import Image, ImageDraw
import io
import time
from PIL import Image, ImageDraw, ImageFont

def int_char_mix_crt(num_questions, difficulty):    

    # === CONFIG ===
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost/api/question"
    FONT_PATH = "arial.ttf"

    # === UTILITY FUNCTIONS ===
    def get_random_string(length=25):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choice(chars) for _ in range(length))

    def count_letters(s):
        return sum(c.isalpha() for c in s)

    def count_numbers(s):
        return sum(c.isdigit() for c in s)

    def get_seconds_for_difficulty(difficulty):
        return {
            "Too Easy": 11,
            "Easy": 12,
            "Medium": 13,
            "Tough": 16,
            "Too Tough": 16
        }.get(difficulty, 10)

    def generate_image(text):
        img = Image.new("RGB", (400, 250), color="#e44507")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(FONT_PATH, 20)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (400 - text_width) // 2
        y = (250 - text_height) // 2

        draw.text((x, y), text, fill="white", font=font)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def upload_image(image_buffer):
        files = {"screenshot": ("screenshot.png", image_buffer, "image/png")}
        try:
            response = requests.post(UPLOAD_ENDPOINT, files=files, timeout=10)
            response.raise_for_status()
            json_data = response.json()
            if json_data.get("status"):
                return f"https://backend.stawro.com/stawro/{json_data['path']}"
            else:
                print("❌ Upload failed (status false):", json_data)
                return None
        except requests.exceptions.RequestException as e:
            print("❌ Upload error:", e)
            return None

    def post_question(question, answer, options, image_url, difficulty):
        payload = {
            "question": question,
            "answer": str(answer),
            "a": str(options[0]),
            "b": str(options[1]),
            "c": str(options[2]),
            "d": str(options[3]),
            "language": "English",
            "category": "Character Count",
            "difficulty": difficulty,
            "type": "Mental Ability",
            "image": image_url,
            "seconds": get_seconds_for_difficulty(difficulty)
        }
        try:
            response = requests.post(POST_ENDPOINT, json=payload, timeout=10)
            response.raise_for_status()
            print('\033[92m' + "✅ Question posted successfully!" + '\033[0m')
            return True
        except requests.exceptions.RequestException as e:
            print("❌ Post error:", e)
            return False

    # === MAIN EXECUTION ===
    success_count = 0

    if difficulty not in ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]:
        print("⚠️ Invalid difficulty. Using Medium.")
        difficulty = "Medium"

    for i in range(num_questions):
        print(f"\n🧠 Generating Question {i + 1}/{num_questions}")

        # Adjust string length based on difficulty
        length = {
            "Too Easy": 15,
            "Easy": 18,
            "Medium": 20,
            "Tough": 25,
            "Too Tough": 30
        }.get(difficulty, 25)

        random_string = get_random_string(length)
        mode = random.choice(["letters", "numbers"])
        correct_answer = count_letters(random_string) if mode == "letters" else count_numbers(random_string)
        question_text = f"How many {mode} are in the string above?"

        # Generate options
        options = {correct_answer}
        while len(options) < 4:
            offset = random.randint(-5, 5)
            wrong = correct_answer + offset
            if wrong >= 0:
                options.add(wrong)
        options = list(options)
        random.shuffle(options)

        try:
            img_buffer = generate_image(random_string)
            image_url = upload_image(img_buffer)
            if image_url:
                if post_question(question_text, correct_answer, options, image_url, difficulty):
                    success_count += 1
                    print(f"✅ Uploaded Question {i + 1}")
                else:
                    print(f"❌ Skipped Question {i + 1} (post failed)")
            else:
                print(f"❌ Skipped Question {i + 1} (upload failed)")
        except Exception as e:
            print(f"❌ Error on Question {i + 1}: {e}")

        time.sleep(0.5)

    print(f"\n📊 Done! {success_count}/{num_questions} questions uploaded.")
    return success_count == num_questions


int_char_mix_crt(10, "Too Tough")