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

import math
import io

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




def calender_crt(total_questions, difficulty_level):
        
    # === CONFIG ===
    API_UPLOAD = "https://backend.stawro.com/stawro/upload.php"
    API_POST = "http://192.168.31.44/api/question"
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
                print(f"⚠️ Retry image upload (attempt {attempt}) due to error: {e}")
                time.sleep(1)
                return upload_image(img, attempt + 1)
            else:
                print(f"❌ Image upload failed after {RETRY_LIMIT} attempts: {e}")
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
                print(f"⚠️ Retry post (attempt {attempt}) due to error: {e}")
                time.sleep(1)
                return post_question(img_url, options, answer, level, attempt + 1)
            else:
                print(f"❌ Failed to post question after {RETRY_LIMIT} attempts: {e}")
                return False


    def main(total, level):
        for i in range(total):
            print(f"\n📌 Creating question {i+1}/{total}...")
            try:
                month = random.randint(1, 12)
                max_day = calendar.monthrange(YEAR, month)[1]
                x_day, hint_day = choose_days(max_day, level)
                img = draw_calendar(month, YEAR, x_day, hint_day)
                options, answer = get_mcq_options(x_day, max_day)
                image_url = upload_image(img)
                if not image_url:
                    print("❌ Skipping due to image upload failure.")
                    continue
                success = post_question(image_url, options, answer, level)
                if success:
                    print("✅ Question posted successfully!")
                else:
                    print("❌ Skipped due to post failure.")
                time.sleep(0.3)

            except Exception as e:
                print(f"❌ Unexpected error on question {i+1}: {e}")
                continue


    if __name__ == "__main__":
        try:
            # total_questions = int(sys.argv[1]) if len(sys.argv) > 1 else int(input("Enter number of questions: "))
            # difficulty_level = sys.argv[2] if len(sys.argv) > 2 else input("Enter difficulty: ")
            main(int(total_questions), difficulty_level)
        except Exception as e:
            print(f"❌ Startup Error: {e}")
            sys.exit(1)



def clock_crt( num_questions,difficulty):
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

        # Draw clock border
        draw.ellipse([center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius], outline="#ffbca5", width=8)

        # Draw numbers
        for i in range(1, 13):
            angle = math.radians((i * 30) - 90)
            x = center[0] + math.cos(angle) * (radius - 20)
            y = center[1] + math.sin(angle) * (radius - 20)
            draw.text((x - 5, y - 5), str(i), fill="white")

        # Draw hands
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
        response = requests.post("https://backend.stawro.com/stawro/upload.php", files=files)

        if response.ok:
            data = response.json()
            print("✅ Image uploaded:", data["path"])
            return data["filename"]
        else:
            print("❌ Upload failed:", response.status_code)
            return None

    def post_question(ans, options, filename, difficulty="Tough", estimated_seconds=10):
        url = "http://192.168.31.44/api/question"
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
        response = requests.post(url, json=body)
        if response.ok:
            print(f"✅ Question posted with {estimated_seconds} seconds!")
        else:
            print("❌ Failed to post question:", response.status_code, response.text)

    # === Main Execution ===
    if __name__ == "__main__":
        try:
            # num_questions = int(input("📌 How many clock questions do you want to generate? "))
            # difficulty = input("📌 Enter difficulty level (Too Easy / Easy / Medium / Tough / Too Tough): ").strip()
            allowed_difficulties = ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]

            if difficulty not in allowed_difficulties:
                print("❌ Invalid difficulty. Use one of:", ", ".join(allowed_difficulties))
                exit()
        except ValueError:
            print("❌ Please enter a valid number.")
            exit()

        for i in range(num_questions):
            print(f"\n🕐 Creating Question {i+1}/{num_questions}")
            time_data, correct_ans, options = generate_question()
            estimated_seconds = random.randint(8, 15)

            print("Answer:", correct_ans)
            print("Options:", options)
            print("Estimated Time:", estimated_seconds, "seconds")

            img = draw_clock_image(time_data)
            uploaded_file = upload_image(img)
            if uploaded_file:
                post_question(correct_ans, options, uploaded_file, difficulty=difficulty, estimated_seconds=estimated_seconds)



def corect_code_crt(total, level):
    
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
            # total = int(input("How many questions to generate? "))
            # level = input("Enter difficulty (Too Easy / Easy / Medium / Tough / Too Tough): ").strip()
            run_auto(total_questions=total, difficulty=level)
        except Exception as e:
            print("❌ Invalid input:", e)



def img_similar_crt(num ,difficulty):
    # ---- Configuration ----
    ALL_IMAGES = ["1.png", "2.png", "3.png", "4.png"]  # Ensure these files exist
    LABELS = ["A", "B", "C", "D"]
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://192.168.31.44/api/question"
    DIFFICULTY_SECONDS = {
        "Too Easy": 10,
        "Easy": 15,
        "Medium": 20,
        "Tough": 25,
        "Too Tough": 30
    }
    FINAL_WIDTH = 400
    FINAL_HEIGHT = 250

    # ---- Render the images with labels into a single image ----
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

        cols = 2
        rows = 2
        final_img = Image.new("RGB", (FINAL_WIDTH, FINAL_HEIGHT), bg_color)
        draw = ImageDraw.Draw(final_img)

        for idx, (filename, label) in enumerate(zip(image_filenames, labels)):
            try:
                img = Image.open(filename).resize(image_size)
            except Exception as e:
                print(f"⚠️ Failed to load {filename}: {e}")
                img = Image.new("RGB", image_size, (128, 128, 128))

            col = idx % cols
            row = idx // cols
            x = padding + col * (image_size[0] + padding)
            y = padding + row * (image_size[1] + padding)

            final_img.paste(img, (x, y))

            draw.rectangle([x + 5, y + 5, x + 35, y + 25], fill=label_bg)
            draw.text((x + 10, y + 8), label.upper(), fill=label_color, font=font)

        buffer = BytesIO()
        final_img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    # ---- Get options and correct answer ----
    def get_options_and_answer(images, labels):
        seen = {}
        correct_answer = "None of those"

        for idx, img in enumerate(images):
            if img in seen:
                correct_answer = f"{labels[seen[img]]},{labels[idx]}"
                break
            seen[img] = idx

        all_pairs = [f"{labels[i]},{labels[j]}" for i in range(len(labels)) for j in range(i+1, len(labels))]
        options = set([correct_answer]) if correct_answer != "None of those" else set()
        while len(options) < 3:
            rand_pair = random.choice(all_pairs)
            if rand_pair != correct_answer:
                options.add(rand_pair)
        options.add("None of those")
        return list(options), correct_answer

    # ---- Upload image ----
    def upload_image(image_buffer):
        files = {"screenshot": ("screenshot.png", image_buffer, "image/png")}
        res = requests.post(UPLOAD_ENDPOINT, files=files)
        res.raise_for_status()
        return res.json()

    # ---- Post question ----
    def post_question(correct_answer, options, difficulty, image_url):
        payload = {
            "question": "Which Pictures Are the Same?",
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

    # ---- Run Multiple Questions ----
    def run_multiple_quiz_generations():
        # num = int(input("Enter number of questions to generate: "))
        # difficulty = input("Enter difficulty (Too Easy, Easy, Medium, Tough, Too Tough): ").strip()

        for i in range(1, num + 1):
            print(f"\n🔁 Generating Q{i}/{num}")
            selected = random.sample(ALL_IMAGES, 3)
            dup = random.choice(selected)
            selected.append(dup)
            random.shuffle(selected)

            image_buffer = render_images_to_image_bytes(selected, LABELS)
            options, correct = get_options_and_answer(selected, LABELS)
            random.shuffle(options)

            print(f"✅ Correct Answer: {correct}")
            print(f"🎯 Options: {options}")

            try:
                upload_res = upload_image(image_buffer)
                if upload_res.get("status"):
                    image_path = f"https://backend.stawro.com/stawro/uploads/{upload_res['filename']}"
                    print("🖼️ Uploaded to:", image_path)
                    post_result = post_question(correct, options, difficulty, image_path)
                    print("📤 Question posted:", post_result)
                else:
                    print("❌ Upload failed:", upload_res)
            except Exception as e:
                print("❗ Error:", e)

        print("\n🎉 Done generating all questions!")

    # ---- Main Entry Point ----
    if __name__ == "__main__":
        run_multiple_quiz_generations()




























































































expected_group = 3

tough = ['Too Easy', 'Easy', 'Medium', 'Tough', 'Too Tough']
cat_list = []

data = collection.find({})


for index, dat in enumerate(data):
    print('\033[92m' + '>'*index + " " + '\033[0m')
    if dat['category'] not in cat_list:
        cat_list.append(dat['category'])
    os.system('cls')

    


if len(cat_list) < 10:
    print('Wee need more Questions')
elif len(cat_list) == 10:
    print("Everything ok with Question")
else:
    print("I Found more Questions")
    img_similar_crt(int("20"), "Easy")

print(len(cat_list))






























































