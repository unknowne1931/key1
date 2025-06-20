##Everything ok

import os
from pymongo import MongoClient
import subprocess

from PIL import Image, ImageDraw, ImageFont
import calendar
import random
import requests
from io import BytesIO
import sys
import time
import urllib3
import traceback
import math
import io

import pyttsx3

# Setup pyttsx3 with female voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
female_voice = None
for voice in voices:
    if "female" in voice.name.lower() or "female" in voice.id.lower():
        female_voice = voice.id
        break
if female_voice:
    engine.setProperty('voice', female_voice)
else:
    # fallback to first voice if female not found
    engine.setProperty('voice', voices[1].id)

# Set slower speech rate (default is usually 200)
engine.setProperty('rate', 170)


def speak(text):
    engine.say(text)
    engine.runAndWait()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


os.system('cls')

# MongoDB connection
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)





client = MongoClient(MONGODB_URI)
db = client["test"]
collection1 = db["qno_counts"]
collection = db["question datas"]


auto = ''
expected_category = 9
cat_list = []





def calender_crt(total_questions, difficulty_level):
    API_UPLOAD = "https://backend.stawro.com/stawro/upload.php"
    API_POST = "http://localhost/api/question"
    FONT_PATH = "arial.ttf"
    YEAR = 2024
    RETRY_LIMIT = 3

    def draw_calendar(month, year, x_day, hint_day):
        img = Image.new('RGB', (700, 500), color=(37, 35, 35))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_PATH, 20)
        title_font = ImageFont.truetype(FONT_PATH, 30)

        draw.text((250, 20), f"{calendar.month_name[month]} {year}", font=title_font, fill="white")
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(days):
            draw.text((i * 100 + 20, 70), day, font=font, fill="white")

        month_days = calendar.monthcalendar(year, month)
        for row_idx, week in enumerate(month_days):
            for col_idx, day in enumerate(week):
                x = col_idx * 100 + 20
                y = row_idx * 60 + 100
                if day == 0:
                    continue
                bg = "white"
                text = str(day)
                if day == x_day:
                    bg = "red"
                    text = "X"
                elif day == hint_day:
                    bg = "blue"
                draw.rectangle([x-5, y-5, x+50, y+40], fill=bg)
                draw.text((x, y), text, font=font, fill="black" if bg != "white" else "white")
        return img

    def choose_days(max_day, difficulty):
        hint_day = random.randint(5, max_day - 5)
        if difficulty in ["Too Easy", "Easy"]:
            delta = random.choice([-2, -1, 1, 2])
        elif difficulty == "Medium":
            delta = random.choice([-5, -4, -3, 3, 4, 5])
        elif difficulty in ["Tough", "Too Tough"]:
            delta = random.choice(range(-max_day + 7, -7)) + random.choice([0, 7]) if random.random() < 0.5 else random.choice(range(7, max_day - 7))
        else:
            delta = random.choice([-2, -1, 1, 2])
        x_day = max(1, min(max_day, hint_day + delta))
        if x_day == hint_day:
            x_day = x_day + 1 if x_day < max_day else x_day - 1
        return x_day, hint_day

    def get_mcq_options(correct, max_day):
        include_none = random.random() < 0.35
        options = set()
        correct = int(correct)
        if include_none:
            while len(options) < 3:
                d = correct + random.choice([-2, -1, 1, 2])
                if 1 <= d <= max_day and d != correct:
                    options.add(str(d))
            options.add("None of the above")
            return list(options), "None of the above"
        else:
            options.add(str(correct))
            while len(options) < 4:
                d = correct + random.choice([-6, -5, -4, -3, 3, 4, 5, 6])
                if 1 <= d <= max_day:
                    options.add(str(d))
            opts = list(options)
            random.shuffle(opts)
            return opts, str(correct)

    def upload_image(img, attempt=1):
        try:
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            files = {'screenshot': ('calendar.png', buffer, 'image/png')}
            response = requests.post(API_UPLOAD, files=files, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("status") and data.get("path"):
                return f"https://backend.stawro.com/stawro/{data['path']}"
            else:
                raise Exception("Invalid response: " + str(data))
        except Exception as e:
            if attempt < RETRY_LIMIT:
                print(f"⚠️ Retry upload (attempt {attempt}) due to: {e}")
                time.sleep(1)
                return upload_image(img, attempt + 1)
            else:
                print(f"❌ Upload failed after {RETRY_LIMIT} attempts: {e}")
                return None

    def post_question(img_url, options, answer, level, attempt=1):
        try:
            payload = {
                "question": "Which date is marked with 'X'?",
                "answer": answer,
                "a": options[0],
                "b": options[1],
                "c": options[2],
                "d": options[3],
                "language": "English",
                "category": "calender",
                "difficulty": level,
                "type": "Mental Ability",
                "image": img_url,
                "seconds": 10
            }
            response = requests.post(API_POST, json=payload, timeout=10)
            response.raise_for_status()
            return response.ok
        except Exception as e:
            if attempt < RETRY_LIMIT:
                print(f"⚠️ Retry POST (attempt {attempt}) due to: {e}")
                time.sleep(1)
                return post_question(img_url, options, answer, level, attempt + 1)
            else:
                print(f"❌ Post failed after {RETRY_LIMIT} attempts: {e}")
                return False

    success_count = 0
    for i in range(total_questions):
        print(f"\n📌 Creating question {i+1}/{total_questions}...")

        try:
            month = random.randint(1, 12)
            max_day = calendar.monthrange(YEAR, month)[1]
            print(f"📆 Month: {month}, Max Days: {max_day}")

            x_day, hint_day = choose_days(max_day, difficulty_level)
            print(f"📍 X Day: {x_day}, Hint Day: {hint_day}")

            img = draw_calendar(month, YEAR, x_day, hint_day)
            print(f"🖼️ Calendar image drawn successfully.")

            options, answer = get_mcq_options(x_day, max_day)
            print(f"🔢 Options: {options} | ✅ Answer: {answer}")

            time.sleep(0.3)

            image_url = upload_image(img)
            print(f"🌐 Image URL: {image_url}")
            if not image_url:
                print("🚫 Skipping due to image upload failure.")
                continue

            success = post_question(image_url, options, answer, difficulty_level)
            if success:
                print("✅ Question posted successfully!")
                success_count += 1
            else:
                print("❌ Failed to post question.")

        except Exception as e:
            print(f"❌ General error at Question {i+1}: {e}")
            traceback.print_exc()

        time.sleep(0.3)


    print(f"\n📊 Completed: {success_count}/{total_questions} posted.")
    return success_count == total_questions

def clock_crt(num_questions, difficulty):
    def get_random_time(include_seconds=False):
        hour = random.randint(1, 12)
        minute = random.randint(0, 59)
        second = random.randint(0, 59) if include_seconds else 0
        is_pm = random.choice([True, False])
        return {"hour": hour, "minute": minute, "second": second, "isPM": is_pm}

    def format_time(time_data, include_seconds=False):
        hh = str(time_data["hour"]).zfill(2)
        mm = str(time_data["minute"]).zfill(2)
        ss = str(time_data["second"]).zfill(2)
        meridian = "PM" if time_data["isPM"] else "AM"
        return f"{hh}:{mm}:{ss} {meridian}" if include_seconds else f"{hh}:{mm} {meridian}"

    def convert_to_24hour(hour, is_pm):
        if hour == 12 and not is_pm:
            return 0
        elif hour == 12 and is_pm:
            return 12
        return hour + 12 if is_pm else hour

    def draw_clock_image(time_data):
        width, height = 400, 250
        img = Image.new('RGB', (width, height), '#ff5410')
        draw = ImageDraw.Draw(img)

        center = (width // 2, height // 2)
        radius = 100

        draw.ellipse([center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius], outline="#ffbca5", width=8)

        for i in range(1, 13):
            angle = math.radians((i * 30) - 90)
            x = center[0] + math.cos(angle) * (radius - 20)
            y = center[1] + math.sin(angle) * (radius - 20)
            draw.text((x - 5, y - 5), str(i), fill="white")

        hour = time_data["hour"]
        minute = time_data["minute"]
        second = time_data["second"]
        is_pm = time_data["isPM"]

        hour_24 = convert_to_24hour(hour, is_pm)
        hour_angle = ((hour_24 % 12) + minute / 60 + second / 3600) * 30 - 90
        minute_angle = (minute + second / 60) * 6 - 90
        second_angle = second * 6 - 90

        def draw_hand(angle_deg, length, color, width=3):
            angle = math.radians(angle_deg)
            x = center[0] + math.cos(angle) * length
            y = center[1] + math.sin(angle) * length
            draw.line([center, (x, y)], fill=color, width=width)

        draw_hand(hour_angle, 50, "white", 5)
        draw_hand(minute_angle, 70, "gray", 4)
        draw_hand(second_angle, 85, "white", 2)

        draw.ellipse([center[0]-3, center[1]-3, center[0]+3, center[1]+3], fill="white")
        return img

    def generate_distractors(correct, count, include_seconds):
        distractors = set()
        correct_str = format_time(correct, include_seconds)

        while len(distractors) < count:
            offset_min = random.randint(-5, 5)
            offset_sec = random.randint(-5, 5) if include_seconds else 0

            minute = (correct["minute"] + offset_min) % 60
            second = (correct["second"] + offset_sec) % 60 if include_seconds else 0

            hour = correct["hour"]
            if correct["minute"] + offset_min < 0:
                hour = hour - 1 if hour > 1 else 12
            elif correct["minute"] + offset_min >= 60:
                hour = hour + 1 if hour < 12 else 1

            new_time = {"hour": hour, "minute": minute, "second": second, "isPM": correct["isPM"]}
            formatted = format_time(new_time, include_seconds)

            if formatted != correct_str:
                distractors.add(formatted)

        return list(distractors)

    def generate_question():
        include_seconds = random.choice([True, False])
        time_data = get_random_time(include_seconds)
        correct_answer = format_time(time_data, include_seconds)
        distractors = generate_distractors(time_data, 3, include_seconds)
        options = [correct_answer] + distractors
        random.shuffle(options)
        return time_data, correct_answer, options

    def upload_image(image):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        files = {'screenshot': ('clock.png', buffer, 'image/png')}
        try:
            response = requests.post("https://backend.stawro.com/stawro/upload.php", files=files)
            if response.ok:
                return response.json().get("filename")
        except Exception as e:
            print("❌ Upload failed:", e)
        return None

    def post_question(ans, options, filename, difficulty, estimated_seconds):
        url = "http://localhost/api/question"
        body = {
            "question": "Guess the time shown on the clock.",
            "answer": ans,
            "a": options[0],
            "b": options[1],
            "c": options[2],
            "d": options[3],
            "language": "English",
            "category": "clock",
            "difficulty": difficulty,
            "type": "Mental Ability",
            "image": f"https://backend.stawro.com/stawro/uploads/{filename}",
            "seconds": estimated_seconds
        }
        try:
            response = requests.post(url, json=body)
            return response.ok
        except Exception as e:
            print("❌ Post failed:", e)
            return False

    allowed_difficulties = ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]
    if difficulty not in allowed_difficulties:
        print("❌ Invalid difficulty. Use one of:", ", ".join(allowed_difficulties))
        return False

    success_count = 0
    for i in range(num_questions):
        print(f"\n🕐 Creating Question {i+1}/{num_questions}")
        time_data, correct_ans, options = generate_question()
        estimated_seconds = random.randint(8, 15)

        img = draw_clock_image(time_data)
        filename = upload_image(img)
        if filename:
            success = post_question(correct_ans, options, filename, difficulty, estimated_seconds)
            if success:
                print("✅ Question posted successfully.")
                success_count += 1
            else:
                print("❌ Failed to post question.")
        else:
            print("❌ Image upload failed.")

    print(f"\n📊 Finished: {success_count}/{num_questions} posted successfully.")
    return success_count == num_questions

def corect_code_crt(total, level):
    # Configuration
    UPLOAD_URL = "https://backend.stawro.com/stawro/upload.php"
    POST_URL = "http://localhost/api/question"
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
        try:
            response = requests.post(UPLOAD_URL, files=files, verify=False)
            return response.json()
        except Exception as e:
            print("❌ Error uploading image:", e)
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

        try:
            res = requests.post(POST_URL, json=payload)
            return res.status_code == 200
        except Exception as e:
            print("❌ Post API error:", e)
            return False

    def run_auto(total_questions=5, difficulty="Medium"):
        settings = DIFFICULTY_SETTINGS.get(difficulty)
        if not settings:
            print("❌ Invalid difficulty selected.")
            return False

        code_length = settings["code_length"]
        seconds = settings["seconds"]
        success_count = 0

        for i in range(1, total_questions + 1):
            print(f"\n--- Generating Question {i} ---")
            correct = get_random_code(code_length)
            options = generate_options(correct)
            image_buffer = render_code_to_image_bytes(correct)
            upload_result = upload_image_from_bytes(image_buffer)

            if upload_result.get("status") and upload_result.get("path"):
                success = post_question(correct, options, upload_result["path"], difficulty, seconds)
                if success:
                    print("✅ Question posted successfully.")
                    success_count += 1
                else:
                    print("❌ Failed to post question.")
            else:
                print("❌ Upload failed or no path returned.")

        print(f"\n📊 Completed: {success_count}/{total_questions} posted.")
        return success_count == total_questions

    return run_auto(total_questions=total, difficulty=level)

def img_similar_crt(num, difficulty):
    # ---- Configuration ----
    ALL_IMAGES = ["./main_ai/1.png", "./main_ai/2.png", "./main_ai/3.png", "./main_ai/4.png"]
    LABELS = ["A", "B", "C", "D"]
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost/api/question"
    DIFFICULTY_SECONDS = {
        "Too Easy": 10,
        "Easy": 15,
        "Medium": 20,
        "Tough": 25,
        "Too Tough": 30
    }
    FINAL_WIDTH = 400
    FINAL_HEIGHT = 250

    def render_images_to_image_bytes(image_filenames, labels):
        image_size = (int(FINAL_WIDTH / 2 - 15), int(FINAL_HEIGHT / 2 - 15))
        padding = 10
        bg_color = (0, 0, 0)
        label_bg = (0, 0, 0)
        label_color = (255, 255, 255)
        label_font_size = 14

        try:
            font = ImageFont.truetype("arial.ttf", label_font_size)
        except:
            font = ImageFont.load_default()

        final_img = Image.new("RGB", (FINAL_WIDTH, FINAL_HEIGHT), bg_color)
        draw = ImageDraw.Draw(final_img)

        for idx, (filename, label) in enumerate(zip(image_filenames, labels)):
            try:
                img = Image.open(filename).resize(image_size)
            except Exception as e:
                print(f"⚠️ Failed to load {filename}: {e}")
                img = Image.new("RGB", image_size, (128, 128, 128))

            col = idx % 2
            row = idx // 2
            x = padding + col * (image_size[0] + padding)
            y = padding + row * (image_size[1] + padding)

            final_img.paste(img, (x, y))
            draw.rectangle([x + 5, y + 5, x + 35, y + 25], fill=label_bg)
            draw.text((x + 10, y + 8), label.upper(), fill=label_color, font=font)

        buffer = BytesIO()
        final_img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def get_options_and_answer(images, labels):
        seen = {}
        correct_answer = "None of those"

        for idx, img in enumerate(images):
            name = os.path.basename(img)
            if name in seen:
                correct_answer = f"{labels[seen[name]]},{labels[idx]}"
                break
            seen[name] = idx

        all_pairs = [f"{labels[i]},{labels[j]}" for i in range(len(labels)) for j in range(i + 1, len(labels))]
        options = set([correct_answer]) if correct_answer != "None of those" else set()
        while len(options) < 3:
            rand_pair = random.choice(all_pairs)
            if rand_pair != correct_answer:
                options.add(rand_pair)
        options.add("None of those")
        return list(options), correct_answer

    def upload_image(image_buffer):
        files = {"screenshot": ("screenshot.png", image_buffer, "image/png")}
        res = requests.post(UPLOAD_ENDPOINT, files=files)
        res.raise_for_status()
        return res.json()

    def post_question(correct_answer, options, difficulty, image_url):
        payload = {
            "question": "Which Images Match?",
            "answer": correct_answer,
            "a": options[0],
            "b": options[1],
            "c": options[2],
            "d": options[3],
            "language": "English",
            "category": "similar_images",
            "difficulty": difficulty,
            "type": "Mental Ability",
            "image": image_url,
            "seconds": DIFFICULTY_SECONDS.get(difficulty, 15)
        }
        res = requests.post(POST_ENDPOINT, json=payload)
        res.raise_for_status()
        return res.json()

    # ---- Main Question Loop ----
    success_count = 0
    for i in range(1, num + 1):
        print(f"\n🔁 Generating Q{i}/{num}")
        try:
            selected = random.sample(ALL_IMAGES, 3)
            dup = random.choice(selected)
            selected.append(dup)
            random.shuffle(selected)

            image_buffer = render_images_to_image_bytes(selected, LABELS)
            options, correct = get_options_and_answer(selected, LABELS)
            random.shuffle(options)

            print(f"✅ Correct Answer: {correct}")
            print(f"🎯 Options: {options}")

            upload_res = upload_image(image_buffer)
            if upload_res.get("status"):
                image_path = f"https://backend.stawro.com/stawro/uploads/{upload_res['filename']}"
                print("🖼️ Uploaded to:", image_path)
                post_question(correct, options, difficulty, image_path)
                print('\033[92m' + "📤 Question Posted Successfully" + '\033[0m')
                success_count += 1
            else:
                print("❌ Upload failed:", upload_res)
        except Exception as e:
            print("❗ Error:", e)

    print(f"\n📊 Done! {success_count}/{num} questions uploaded.")
    return success_count == num

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
            "Too Easy": 8,
            "Easy": 9,
            "Medium": 10,
            "Tough": 10,
            "Too Tough": 13
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

def leter_count_crt(num_questions, user_input):
    import random, requests, io
    from PIL import Image, ImageDraw

    # === CONFIGURATION ===
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost/api/question"
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 250

    wordBank = [
        "bat", "cat", "dog", "hat", "sun", "bee", "cow", "run", "toy", "fun",
        "apple", "green", "light", "peace", "happy", "quiet", "under", "river", "dance", "mouse",
        "jungle", "planet", "bright", "summer", "market", "school", "garden", "memory", "castle", "cloudy",
        "elephant", "creation", "freedom", "triangle", "umbrella", "solution", "activity", "positive", "strategy", "momentum",
        "transparency", "psychology", "revolutionary", "architecture", "communication", "responsibility", "extraordinary", "transformation"
    ]

    difficulty_map = {
        "Too Easy": {"length_range": (3, 5), "seconds": 16},
        "Easy": {"length_range": (4, 6), "seconds": 18},
        "Medium": {"length_range": (5, 8), "seconds": 20},
        "Tough": {"length_range": (6, 10), "seconds": 22},
        "Too Tough": {"length_range": (8, 100), "seconds": 24}
    }

    def filter_words_by_length(min_len, max_len):
        return [word for word in wordBank if min_len <= len(word) <= max_len]

    def generate_sentence(min_len, max_len):
        eligible_words = filter_words_by_length(min_len, max_len)
        if len(eligible_words) < 10:
            raise ValueError("Not enough words for the selected difficulty.")
        return " ".join(random.choices(eligible_words, k=10))

    def get_random_letter(sentence):
        letters = ''.join(filter(str.isalpha, sentence)).lower()
        return random.choice(letters)

    def generate_options(correct):
        options = {correct}
        while len(options) < 4:
            wrong = correct + random.randint(-2, 2)
            if wrong >= 0:
                options.add(wrong)
        return random.sample(list(options), k=4)

    def generate_image(text):
        img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color="white")
        draw = ImageDraw.Draw(img)

        lines = []
        words = text.split()
        line = ""
        for word in words:
            if len(line + " " + word) < 40:
                line += " " + word
            else:
                lines.append(line.strip())
                line = word
        lines.append(line.strip())

        line_height = 20
        total_text_height = len(lines) * line_height
        y = (IMAGE_HEIGHT - total_text_height) // 2

        for line in lines:
            text_width = draw.textlength(line)
            x = (IMAGE_WIDTH - text_width) // 2
            draw.text((x, y), line, fill="black")
            y += line_height

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf

    def upload_image(image_buf):
        files = {"screenshot": ("screenshot.png", image_buf, "image/png")}
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        if response.status_code == 200 and response.json().get("status"):
            return response.json()["path"]
        else:
            raise Exception("Upload failed: " + response.text)

    def post_question(question_data):
        response = requests.post(POST_ENDPOINT, json=question_data)
        if response.status_code == 200:
            print("✅ Question posted successfully!\n")
            return True
        else:
            print("❌ Failed to post question:", response.text)
            return False

    # === MAIN EXECUTION ===
    difficulty = "Medium"
    for key in difficulty_map:
        if key.lower() in user_input.lower():
            difficulty = key
            break

    diff_data = difficulty_map[difficulty]
    min_len, max_len = diff_data["length_range"]
    seconds = str(diff_data["seconds"])

    success_count = 0

    for i in range(num_questions):
        print(f"\n🔢 Generating question {i + 1}/{num_questions}...")

        try:
            sentence = generate_sentence(min_len, max_len)
            letter = get_random_letter(sentence)
            count = sentence.lower().count(letter)
            options = generate_options(count)

            print(f'Sentence: "{sentence}"')
            print(f'Question: How many times does the letter "{letter}" appear?')
            print("Options:", options)

            image_buf = generate_image(sentence)
            image_path = upload_image(image_buf)

            correct_str = str(count)
            options_str = [str(o) for o in options]
            is_none_correct = correct_str not in options_str

            question_data = {
                "question": f'How many times does the letter "{letter}" appear in the sentence?',
                "answer": "None of the above" if is_none_correct else correct_str,
                "a": options_str[0] if not is_none_correct else "",
                "b": options_str[1] if not is_none_correct else "",
                "c": options_str[2] if not is_none_correct else "",
                "d": "None of the above" if is_none_correct else options_str[3],
                "language": "English",
                "category": "leter_find",
                "difficulty": difficulty,
                "type": "Mental Ability",
                "image": f"https://backend.stawro.com/stawro/{image_path}",
                "seconds": seconds
            }

            if post_question(question_data):
                success_count += 1

        except Exception as e:
            print("❌ Error during question generation or upload:", e)

    return success_count == num_questions

def maze_crt(NUM_QUESTIONS, DIFFICULTY):
    UPLOAD_URL = "https://backend.stawro.com/stawro/upload.php"
    POST_URL = "http://localhost/api/question"

    difficulty_config = {
        "Too Easy": {"size": 9, "seconds": 10},
        "Easy": {"size": 13, "seconds": 15},
        "Medium": {"size": 17, "seconds": 20},
        "Tough": {"size": 21, "seconds": 25},
        "Too Tough": {"size": 27, "seconds": 30}
    }

    config = difficulty_config.get(DIFFICULTY, difficulty_config["Medium"])
    CELL_SIZE = 25
    COLS = ROWS = config["size"]
    GOAL_POS = (COLS // 2, ROWS // 2)

    class Cell:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.walls = [True, True, True, True]
            self.visited = False

    class MazeGame:
        def __init__(self, force_no=False):
            self.grid = [Cell(x, y) for y in range(ROWS) for x in range(COLS)]
            self.generate_maze()
            self.force_no = force_no
            if self.force_no:
                self.block_path_somewhere()
            self.player = (0, 0)

        def index(self, x, y):
            return y * COLS + x if 0 <= x < COLS and 0 <= y < ROWS else -1

        def generate_maze(self):
            stack = []
            start = self.grid[0]
            start.visited = True
            stack.append(start)

            while stack:
                current = stack[-1]
                neighbors = []
                directions = [(0, -1, 0, 2), (1, 0, 1, 3), (0, 1, 2, 0), (-1, 0, 3, 1)]
                for dx, dy, wall, opp in directions:
                    nx, ny = current.x + dx, current.y + dy
                    idx = self.index(nx, ny)
                    if idx != -1 and not self.grid[idx].visited:
                        neighbors.append((self.grid[idx], wall, opp))
                if neighbors:
                    neighbor, wall, opp_wall = random.choice(neighbors)
                    current.walls[wall] = False
                    neighbor.walls[opp_wall] = False
                    neighbor.visited = True
                    stack.append(neighbor)
                else:
                    stack.pop()

        def block_path_somewhere(self):
            visited = set()
            queue = [(0, 0, [])]
            while queue:
                x, y, path = queue.pop(0)
                visited.add((x, y))
                cell = self.grid[self.index(x, y)]
                if (x, y) == GOAL_POS:
                    if len(path) > 4:
                        bx, by = path[len(path) // 2]
                        for dx, dy, wall, opp_wall in [(0, -1, 0, 2), (1, 0, 1, 3), (0, 1, 2, 0), (-1, 0, 3, 1)]:
                            nx, ny = bx + dx, by + dy
                            if (nx, ny) in path:
                                idx1 = self.index(bx, by)
                                idx2 = self.index(nx, ny)
                                if idx1 != -1 and idx2 != -1:
                                    self.grid[idx1].walls[wall] = True
                                    self.grid[idx2].walls[opp_wall] = True
                                    return
                    return
                for dx, dy, wall in [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]:
                    nx, ny = x + dx, y + dy
                    idx = self.index(nx, ny)
                    if idx != -1 and not cell.walls[wall] and (nx, ny) not in visited:
                        queue.append((nx, ny, path + [(x, y)]))

        def draw_maze(self):
            maze_width = CELL_SIZE * COLS
            maze_height = CELL_SIZE * ROWS
            padding = 20
            img = Image.new("RGB", (maze_width + 2 * padding, maze_height + 2 * padding), "white")
            draw = ImageDraw.Draw(img)

            for cell in self.grid:
                x = cell.x * CELL_SIZE + padding
                y = cell.y * CELL_SIZE + padding
                if cell.walls[0]: draw.line([x, y, x + CELL_SIZE, y], fill="black", width=2)
                if cell.walls[1]: draw.line([x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE], fill="black", width=2)
                if cell.walls[2]: draw.line([x + CELL_SIZE, y + CELL_SIZE, x, y + CELL_SIZE], fill="black", width=2)
                if cell.walls[3]: draw.line([x, y + CELL_SIZE, x, y], fill="black", width=2)

            px, py = self.player
            draw.ellipse([px * CELL_SIZE + 6 + padding, py * CELL_SIZE + 6 + padding,
                          px * CELL_SIZE + CELL_SIZE - 6 + padding, py * CELL_SIZE + CELL_SIZE - 6 + padding], fill="blue")
            gx, gy = GOAL_POS
            draw.rectangle([gx * CELL_SIZE + 4 + padding, gy * CELL_SIZE + 4 + padding,
                            gx * CELL_SIZE + CELL_SIZE - 4 + padding, gy * CELL_SIZE + CELL_SIZE - 4 + padding], fill="red")

            img = img.resize((400, 250))
            return img

        def is_goal_reachable(self):
            visited = set()
            queue = [self.player]
            while queue:
                x, y = queue.pop(0)
                if (x, y) == GOAL_POS:
                    return True
                visited.add((x, y))
                cell = self.grid[self.index(x, y)]
                for dx, dy, wall in [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]:
                    nx, ny = x + dx, y + dy
                    idx = self.index(nx, ny)
                    if idx != -1 and not cell.walls[wall] and (nx, ny) not in visited:
                        queue.append((nx, ny))
            return False

        def upload_image(self, img):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            files = {"screenshot": ("maze.png", buf, "image/png")}
            res = requests.post(UPLOAD_URL, files=files)
            return res.json().get("path", None)

        def post_question(self, img_url, answer):
            payload = {
                "question": "Can the man reach the center of the maze?",
                "answer": answer,
                "a": "Yes",
                "b": "No",
                "c": "----",
                "d": "----",
                "language": "English",
                "category": "Maze Logic",
                "difficulty": DIFFICULTY,
                "type": "Mental Ability",
                "image": f"https://backend.stawro.com/stawro/{img_url}",
                "seconds": str(config["seconds"])
            }
            res = requests.post(POST_URL, json=payload)
            if res.status_code == 200:
                print("✅ Question posted successfully!")
                return True
            else:
                print("❌ Failed to post question:", res.text)
                return False

        def run(self):
            img = self.draw_maze()
            reachable = self.is_goal_reachable()
            answer = "No" if self.force_no else ("Yes" if reachable else "No")
            img_url = self.upload_image(img)
            if img_url:
                print(f"✅ Image uploaded! Answer: {answer}")
                return self.post_question(img_url, answer)
            else:
                print("❌ Image upload failed.")
                return False

    # === MAIN LOOP ===
    success_count = 0
    for i in range(NUM_QUESTIONS):
        print(f"\n--- Generating Maze {i + 1}/{NUM_QUESTIONS} ---")
        make_unsolvable = random.random() < 0.5
        game = MazeGame(force_no=make_unsolvable)
        if game.run():
            success_count += 1

    if success_count == NUM_QUESTIONS:
        return True
    else:
        print(f"✅ {success_count}/{NUM_QUESTIONS} questions posted successfully.")
        return False

def num_100_crt(num_questions, difficulty):
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost/api/question"
    FONT_PATH = "arial.ttf"

    try:
        assert difficulty in ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]
    except Exception as e:
        print(f"Error: {e}")
        return False

    def get_difficulty_params(difficulty):
        if difficulty == "Too Easy":
            return random.randint(2, 3), 10
        elif difficulty == "Easy":
            return random.randint(3, 4), 7
        elif difficulty == "Medium":
            return random.randint(5, 7), 5
        elif difficulty == "Tough":
            return random.randint(6, 10), 3
        elif difficulty == "Too Tough":
            return random.randint(10, 15), 1

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
                return True
            else:
                print(f"❌ Failed to post question. Status code: {res.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error posting question: {e}")
            return False

    # === MAIN LOOP ===
    success_count = 0
    for _ in range(num_questions):
        display_series, correct_answer, options = generate_question()
        image = draw_grid(display_series)
        image_url = upload_image(image)
        if image_url:
            success = post_question(image_url, correct_answer, options)
            if success:
                success_count += 1

    if success_count == num_questions:
        return True
    else:
        print(f"Only {success_count}/{num_questions} questions were successfully posted.")
        return False

def numers_crt(num_questions, difficulty):
    # === CONFIG ===
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost/api/question"
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 250
    FONT_SIZE = 22
    FONT_PATH = None  # Use default font
    IMAGE_PADDING = 15  # Added padding around edges

    DIFFICULTY_CONFIG = {
        "Too Easy": {"option_range": (0, 5), "seconds": 15, "total_numbers": 20},
        "Easy": {"option_range": (0, 6), "seconds": 12, "total_numbers": 30},
        "Medium": {"option_range": (0, 8), "seconds": 10, "total_numbers": 40},
        "Tough": {"option_range": (0, 10), "seconds": 8, "total_numbers": 50},
        "Too Tough": {"option_range": (0, 12), "seconds": 7, "total_numbers": 60},
    }

    def generate_question(difficulty):
        config = DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["Medium"])
        target_number = random.randint(10, 99)
        total_numbers = config["total_numbers"]
        numbers = []
        count = 0

        for _ in range(total_numbers):
            if random.random() < 0.2:
                numbers.append(target_number)
                count += 1
            else:
                rand_num = random.randint(10, 99)
                numbers.append(rand_num)

        include_none = random.random() < 0.4
        options = random.sample(range(config["option_range"][0], config["option_range"][1]), 4)

        correct_answer = str(count)
        if include_none and count not in options:
            correct_answer = "None of the above"
            options[random.randint(0, 3)] = "None of the above"
        else:
            if count not in options:
                options[random.randint(0, 3)] = count

        options = [str(opt) for opt in options]
        random.shuffle(options)

        return {
            "question": f"How many times does the number \"{target_number}\" appear?",
            "answer": correct_answer,
            "target": target_number,
            "options": options[:4],
            "numbers": numbers,
            "correct_count": count,
            "difficulty": difficulty,
            "seconds": config["seconds"]
        }

    def render_image(data):
        img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=(58, 54, 54))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default() if FONT_PATH is None else ImageFont.truetype(FONT_PATH, FONT_SIZE)

        for _ in range(len(data["numbers"])):
            x = random.randint(IMAGE_PADDING, IMAGE_WIDTH - IMAGE_PADDING - 30)
            y = random.randint(IMAGE_PADDING, IMAGE_HEIGHT - IMAGE_PADDING - 30)
            num = random.choice(data["numbers"])
            draw.text((x, y), str(num), fill=(
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            ), font=font)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def upload_image(image_bytes):
        files = {'screenshot': ("screenshot.png", image_bytes, 'image/png')}
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        if response.status_code == 200:
            return response.json().get("path")
        return None

    def post_question(data):
        response = requests.post(POST_ENDPOINT, json=data)
        return response.json()

    def main():
        success_count = 0

        for i in range(num_questions):
            print(f"\nGenerating Question {i+1}/{num_questions}")
            q = generate_question(difficulty)
            image_stream = render_image(q)
            image_path = upload_image(image_stream)
            if not image_path:
                print("❌ Failed to upload image.")
                continue

            post_data = {
                "question": q["question"],
                "answer": q["answer"],
                "a": q["options"][0],
                "b": q["options"][1],
                "c": q["options"][2],
                "d": q["options"][3],
                "language": "English",
                "category": "Counting",
                "difficulty": q["difficulty"],
                "type": "Mental Ability",
                "image": f"https://backend.stawro.com/stawro/{image_path}",
                "seconds": str(q["seconds"])
            }

            result = post_question(post_data)
            print("📥 Response from API:", result)

            if isinstance(result, dict) and (
                "Question added successfully" in result.get("message", "") or
                result.get("message") == "Question added successfully"
            ):
                print("\033[92m✅ Question posted successfully!\033[0m")
                success_count += 1
            else:
                print("⚠️ Failed to post question.")

        if success_count == num_questions:
            return True
        else:
            print(f"✅ {success_count}/{num_questions} questions posted successfully.")
            return False

    return main()

# Test Run
# numers_crt(3, "Tough")



cat_grp_ary = [calender_crt, clock_crt, corect_code_crt, img_similar_crt, int_char_mix_crt, leter_count_crt, maze_crt, num_100_crt, numers_crt]


# Counting_100 = num_100_crt()
# clock = clock_crt()
# leter_find = 








def create_cate_and_qst(expected_group):
    os.system('cls')
    # data = calender_crt(1, "Too Easy")
    # print(f"Status : {data}")

    tough_dif = ['Too Easy', 'Easy', 'Medium', "Tough", 'Too Tough', 'Too Easy', 'Easy', 'Medium', "Tough",] #make add another one 9 category exist
    
    for i in range(expected_group):
        random.shuffle(tough_dif)
        random.shuffle(cat_grp_ary)
        
        for dif, cat in zip(tough_dif, cat_grp_ary):

            data = cat(1, dif)
            if data is True:
                print('\033[92m' + f' ------------------------------------------------ {i+1} Group {dif} Category {cat.__name__} -------------------------------------------' + '\033[0m')
            else:
                speak(f"Group {i+1} is not created")
                print('\033[91m' + f' ------------------------------------------------ {i+1} Group {dif} Category {cat.__name__} -------------------------------------------' + '\033[0m')
                time.sleep(5)
                dat = cat(1, dif)
                if dat is True:
                    print('\033[92m' + f' ------------------------------------------------ {i+1} Group {dif} Category {cat.__name__} -------------------------------------------' + '\033[0m')
                else:
                    speak(f"Group {i+1} is not created")
                    print('\033[91m' + f' ------------------------ {i+1} Group {dif} Category {cat.__name__} -------------------------------------------' + '\033[0m')
                    exit()


        speak(f"Group {i+1} is created")
        print('\033[92m' + f' ------------------------------------------------ {i+1} Group -------------------------------------------' + '\033[0m')
        print('\033[92m' + f' ------------------------------------------------ {i+1} Group -------------------------------------------' + '\033[0m')
        print('\033[92m' + f' ------------------------------------------------ {i+1} Group -------------------------------------------' + '\033[0m')
        print('\033[92m' + f' ------------------------------------------------ {i+1} Group -------------------------------------------' + '\033[0m')
        time.sleep(3)
        os.system('cls')









speak("I need length to Create total Number of Groups")
expected_group = int(input("Expected category Groups [ex : 2, 10, 40] : "))  #Expected category Groups

if collection.count_documents({}) > 0:
    speak("Can i Delete all Questions Data And Reupload frome first")
    delet = input("Can i Delete all Questions Data And Reupload frome first ['Yes', 'Y', 'y'] : ") #If Yes It will Delete All "question datas" 
    if delet == "Yes" or "y" or "Y":
        delete_result = collection.delete_many({})
        print(f"Deleted {delete_result.deleted_count} documents from 'question datas'.")
    else:
        print("I will not delete any data")



data = collection.find({})


for index, dat in enumerate(data):
    print('\033[92m' + '>'*index + " " + '\033[0m')
    if dat['category'] not in cat_list:
        cat_list.append(dat['category'])
    os.system('cls')

    


if len(cat_list) < expected_category:
    print('Wee need more Category')
    speak(f"I Have found : {len(cat_list)} Category , i Need : {expected_category - len(cat_list)} more Category")
    print(f"\033[93mI Have found : {len(cat_list)} Category , i Need : {expected_category - len(cat_list)}\033[0m")
    auto = input("Can I Run All Automatic 'Yes', 'yes' ,'Y', 'y' or 'No', 'N', 'n'   : ")
    if auto == "Y" or 'Yes' or 'yes' or 'y':
        create_cate_and_qst(expected_group)
    else:
        ask_per1 = input("Can i create a Questions 'yes', 'y' : ")
        if ask_per1 == "Yes" or 'y':
            create_cate_and_qst(expected_group)


elif len(cat_list) == expected_category:
    print('\033[92m' + "Everything OK" + '\033[0m')
else:
    print("I Found More Category")













    # leter_count_crt(int('20'), "Easy")
    # int_char_mix_crt(int("20"), "Easy")
    # maze_crt(int("20"), "Easy")
    # num_100_crt(int("20"), "Easy")
    # numers_crt(int('20'), 'Easy')
        
# print(len(cat_list))







