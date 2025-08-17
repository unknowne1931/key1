import os
import time
from pymongo import MongoClient
from collections import defaultdict
from bson.objectid import ObjectId

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


# Main --- Connect to MongoDB ---
# MONGODB_URI = os.getenv(
#     "MONGODB_URI",
#     "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata _try"
# )



# Proto --- Connect to MongoDB ---
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
    # "mongodb+srv://instasecur24:kick@stawroprototypecluster.0xbx0u5.mongodb.net/?retryWrites=true&w=majority&appName=staWroprototypecluster"
)

client = MongoClient(MONGODB_URI)
db = client["test"]
collection = db["qno_counts"]
start_stop_db = db["start_stops"]
sec_data = db['seconds_cals']

# ✅ System control function
def stop_start(new_status):
    start_stop = start_stop_db.find_one({})
    if not start_stop:
        start_stop_db.insert_one({"Status": new_status})
        print(f"\033[93m⚠️ Created Status Document with value: {new_status}\033[0m")
        return

    current_status = start_stop.get("Status", "on")

    if current_status.lower() != new_status.lower():
        start_stop_db.update_one({"_id": start_stop["_id"]}, {"$set": {"Status": new_status}})
        if new_status != "on":
            print(f"\033[91m⛔ Game stopped. Status changed to: {new_status}\033[0m")
        else:
            print("\033[92m✅ Game is running...\033[0m")
    else:
        print("\033[91m⛔ System is stopped. Please start it to continue.\033[0m")


# --- Configuration ---
expected_range = 300

# def seT1(one, two, num):
#     def get_difficulty_settings(level):
#         settings = {
#             "Too Easy":     {"common": 6, "extra": 2, "base": 50,  "set_len": 8,  "seconds": 8},
#             "Easy":         {"common": 5, "extra": 3, "base": 60,  "set_len": 9,  "seconds": 10},
#             "Medium":       {"common": 4, "extra": 4, "base": 80,  "set_len": 10, "seconds": 12},
#             "Tough":        {"common": 4, "extra": 5, "base": 100, "set_len": 12, "seconds": 14},
#             "Too Tough":    {"common": 4, "extra": 8, "base": 150, "set_len": 20, "seconds": 16}
#         }
#         return settings.get(level.title(), settings["Medium"])

#     def generate_sets(settings, difficulty):
#         base_numbers = list(range(1, settings["base"] + 1))
#         common = random.sample(base_numbers, settings["common"])
#         used = set(common)
#         extra_pool = list(set(base_numbers) - used)

#         def noisy_set():
#             fake_commons = []
#             if difficulty == "Too Tough":
#                 fake_commons = random.sample(extra_pool, 2)
#             items = common + random.sample(extra_pool, settings["extra"]) + fake_commons
#             return sorted(random.sample(items, min(settings["set_len"], len(items))))

#         return noisy_set(), noisy_set(), noisy_set(), common

#     def generate_options(correct_common, extra_pool, difficulty):
#         correct = sorted(random.sample(correct_common, min(4, len(correct_common))))
#         options = [correct]

#         attempts = 0
#         while len(options) < 4 and attempts < 20:
#             if difficulty == "Too Tough":
#                 wrong = sorted(random.sample(correct_common + extra_pool, 4))
#             else:
#                 wrong = sorted(random.sample(correct_common, 2) + random.sample(extra_pool, 2))
#             if wrong not in options:
#                 options.append(wrong)
#             attempts += 1

#         random.shuffle(options)
#         return correct, options

#     def create_image(setA, setB, setC, q_no, difficulty):
#         img = Image.new('RGB', (420, 280), color=(240, 244, 248))
#         draw = ImageDraw.Draw(img)

#         try:
#             title_font = ImageFont.truetype("arialbd.ttf", 18)
#             set_font = ImageFont.truetype("arial.ttf", 14)
#             small_font = ImageFont.truetype("arial.ttf", 12)
#         except:
#             title_font = ImageFont.load_default()
#             set_font = ImageFont.load_default()
#             small_font = ImageFont.load_default()

#         sets = [
#             (setA, (249, 155, 130), 50),
#             (setB, (125, 201, 255), 115),
#             (setC, (142, 224, 149), 180),
#         ]
#         for items, color, y in sets:
#             draw.rounded_rectangle([10, y, 410, y + 45], radius=8, fill=color, outline="black", width=2)
#             display_text = " ".join(map(str, sorted(items)))
#             draw.text((20, y + 5), display_text, fill="black", font=set_font)

#         draw.text((280, 260), "Made by staWro", font=small_font, fill="gray")

#         buffer = BytesIO()
#         img.save(buffer, format="PNG")
#         buffer.seek(0)
#         return buffer

#     def upload_image(image_buffer):
#         files = {'screenshot': ("screenshot.png", image_buffer, "image/png")}
#         try:
#             res = requests.post("https://backend.stawro.com/stawro/upload.php", files=files)
#             if res.status_code == 200 and res.json().get("status") == "success":
#                 return f"https://backend.stawro.com/stawro/{res.json()['path']}"
#             else:
#                 print("❌ Upload failed:", res.text)
#                 return None
#         except Exception as e:
#             print("❌ Upload error:", e)
#             return None

#     def post_question(correct, options, difficulty, image_url, seconds):
#         body = {
#             'qno': num,
#             "Questio": "Find numbers that are common to all 3 sets.",
#             "Ans": ", ".join(map(str, correct)),
#             "a": ", ".join(map(str, options[0])),
#             "b": ", ".join(map(str, options[1])),
#             "c": ", ".join(map(str, options[2])),
#             "d": ", ".join(map(str, options[3])),
#             "lang": "English",
#             "sub_lang": "Set_Theory",
#             "tough": difficulty,
#             "img": image_url,
#             "seconds": str(seconds),
#         }

#         try:
#             res = requests.post("http://localhost:81/api/question/change", json=body)
#             if res.ok:
#                 print(f"✅ Q Posted — {difficulty} ({seconds}s)")
#                 return True
#             else:
#                 print("❌ Error posting:", res.text)
#                 return False
#         except Exception as e:
#             print("❌ Exception posting:", e)
#             return False

#     # === Main Controller ===
#     try:
#         num_questions = int(one)
#         difficulty = two.strip().title()
#         settings = get_difficulty_settings(difficulty)
#         seconds = settings["seconds"]

#         for i in range(1, num_questions + 1):
#             setA, setB, setC, common = generate_sets(settings, difficulty)
#             extra_pool = list(set(setA + setB + setC) - set(common))
#             correct, options = generate_options(common, extra_pool, difficulty)
#             image_buffer = create_image(setA, setB, setC, i, difficulty)
#             image_url = upload_image(image_buffer)

#             if not image_url:
#                 return "No"
#             if not post_question(correct, options, difficulty, image_url, seconds):
#                 return "No"

#         return True
#     except Exception as e:
#         print("❌ Exception occurred:", e)
#         return "No"

# def seT(one, two, num):
#     def get_difficulty_settings(level):
#         settings = {
#             "Too Easy": {"common": 6, "extra": 2, "base": 20, "set_len": 5, "seconds": 18},
#             "Easy": {"common": 5, "extra": 3, "base": 20, "set_len": 7, "seconds": 28},
#             "Medium": {"common": 4, "extra": 4, "base": 20, "set_len": 9, "seconds": 35},
#             "Tough": {"common": 4, "extra": 5, "base": 20, "set_len": 12, "seconds": 45},
#             "Too Tough": {"common": 4, "extra": 8, "base": 20, "set_len": 15, "seconds": 50}
#         }
#         return settings.get(level.title(), settings["Medium"])

#     def generate_sets(settings, difficulty):
#         base_numbers = list(range(1, settings["base"] + 1))
#         common = random.sample(base_numbers, settings["common"])
#         used = set(common)
#         extra_pool = list(set(base_numbers) - used)

#         def build_set():
#             fake_commons = random.sample(extra_pool, 2) if difficulty == "Too Tough" else []
#             extras = random.sample(extra_pool, settings["extra"])
#             items = list(set(common + extras + fake_commons))  # ensure uniqueness
#             random.shuffle(items)
#             return items[:settings["set_len"]]

#         # Force common to be in all 3 sets
#         def enforce_common(s):
#             # Make sure all common elements are in the set
#             missing = [x for x in common if x not in s]
#             if missing:
#                 s = s[:max(0, settings["set_len"] - len(missing))] + missing
#             return sorted(s)

#         setA = enforce_common(build_set())
#         setB = enforce_common(build_set())
#         setC = enforce_common(build_set())

#         return setA, setB, setC, common


#     def generate_options(correct_common, extra_pool, difficulty):
#         correct = sorted(random.sample(correct_common, min(4, len(correct_common))))
#         correct_len = len(correct)
#         options = [correct]
#         attempts = 0

#         while len(options) < 4 and attempts < 50:
#             # Try to generate a wrong option with same length as correct
#             if difficulty == "Too Tough":
#                 pool = correct_common + extra_pool
#             else:
#                 pool = correct_common * 2 + extra_pool * 2

#             wrong = sorted(random.sample(pool, min(correct_len, len(pool))))
#             if wrong not in options and wrong != correct:
#                 options.append(wrong)
#             attempts += 1

#         random.shuffle(options)
        
#         # ✅ For debugging: print each option
#         for idx, opt in enumerate(options):
#             label = chr(65 + idx)  # A, B, C, D
#             print(f"  {label}: {opt}")

#         return correct, options




#     def create_image(setA, setB, setC, q_no, difficulty):
#         img = Image.new('RGB', (420, 280), color=(240, 244, 248))
#         draw = ImageDraw.Draw(img)

#         try:
#             title_font = ImageFont.truetype("arialbd.ttf", 18)
#             set_font = ImageFont.truetype("arial.ttf", 14)
#             small_font = ImageFont.truetype("arial.ttf", 12)
#         except:
#             title_font = set_font = small_font = ImageFont.load_default()

#         sets = [
#             (setA, (249, 155, 130), 50),
#             (setB, (125, 201, 255), 115),
#             (setC, (142, 224, 149), 180),
#         ]
#         for items, color, y in sets:
#             draw.rounded_rectangle([10, y, 410, y + 45], radius=8, fill=color, outline="black", width=2)
#             display_text = " ".join(map(str, sorted(items)))
#             draw.text((20, y + 5), display_text, fill="black", font=set_font)

#         draw.text((280, 260), "Made by staWro", font=small_font, fill="gray")

#         buffer = BytesIO()
#         img.save(buffer, format="PNG")
#         buffer.seek(0)
#         return buffer

#     def upload_image(image_buffer):
#         files = {'screenshot': ("screenshot.png", image_buffer, "image/png")}
#         try:
#             res = requests.post("https://backend.stawro.com/stawro/upload.php", files=files)
#             if res.status_code == 200 and res.json().get("status") == "success":
#                 return f"https://backend.stawro.com/stawro/{res.json()['path']}"
#             else:
#                 print("❌ Upload failed:", res.text)
#                 return None
#         except Exception as e:
#             print("❌ Upload error:", e)
#             return None

#     def post_question(correct, options, difficulty, image_url, seconds):
#         body = {
#             'qno': num,
#             "Questio": "Find numbers that are common to all 3 sets.",
#             "Ans": ", ".join(map(str, correct)),
#             "a": ", ".join(map(str, options[0])),
#             "b": ", ".join(map(str, options[1])),
#             "c": ", ".join(map(str, options[2])),
#             "d": ", ".join(map(str, options[3])),
#             "lang": "English",
#             "sub_lang": "Set_Theory",
#             "tough": difficulty,
#             "img": image_url,
#             "seconds": str(seconds),
#         }

#         try:
#             res = requests.post("http://localhost:81/api/question/change", json=body)
#             if res.ok:
#                 print(f"✅ Q Posted — {difficulty} ({seconds}s)")
#                 return True
#             else:
#                 print("❌ Error posting:", res.text)
#                 return False
#         except Exception as e:
#             print("❌ Exception posting:", e)
#             return False

#     # === Main Execution ===
#     try:
#         num_questions = int(one)
#         difficulty = two.strip().title()
#         settings = get_difficulty_settings(difficulty)
#         seconds = settings["seconds"]

#         for i in range(1, num_questions + 1):
#             attempts = 0
#             while attempts < 10:
#                 setA, setB, setC, _ = generate_sets(settings, difficulty)
#                 true_common = sorted(list(set(setA) & set(setB) & set(setC)))

#                 if len(true_common) >= 1:
#                     extra_pool = list(set(setA + setB + setC) - set(true_common))
#                     correct, options = generate_options(true_common, extra_pool, difficulty)
#                     image_buffer = create_image(setA, setB, setC, i, difficulty)
#                     image_url = upload_image(image_buffer)

#                     if not image_url or not post_question(correct, options, difficulty, image_url, seconds):
#                         return "No"
#                     break  # break the while loop if successful
#                 else:
#                     attempts += 1
#                     print(f"⚠️ Retry {attempts}: No valid common found.")
#             else:
#                 print("❌ Failed to generate valid question after multiple attempts.")
#                 return "No"


#         return True

#     except Exception as e:
#         print("❌ Exception occurred:", e)
#         return "No"

#done
def generate_pattern_mcq_post(num, difficulty, qno):
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost:81/api/question/change"

    # get_sec = sec_data.find_one({"category": "Pattern_Lock", "Tough": difficulty}) or {}

    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0

    final_sec = 0



    def get_grid_size(difficulty):
        if difficulty == "Too Tough":
            return 5
        elif difficulty == "Tough":
            return 4
        else:
            return 3
        # return 5 if difficulty == "Too Tough" else 4 if difficulty == "Tough" else 3

    def get_path_length(difficulty):
        return {
            "Too Easy": random.randint(2, 5),
            "Easy": random.randint(4, 7),
            "Medium": random.randint(7, 9),
            "Tough": random.randint(10, 13),
            "Too Tough": random.randint(14, 17)
        }.get(difficulty, 7)

    def get_time(difficulty):
        return "19" if difficulty in ["Tough", "Too Tough"] else "15"

    for qno in range(1, num + 1):
        try:
            grid_size = get_grid_size(difficulty)
            total_dots = grid_size * grid_size
            points = [(x, y) for y in range(grid_size) for x in range(grid_size)]
            used = set()

            path_len = get_path_length(difficulty)

            def get_inline_passes(p1, p2):
                x1, y1 = points[p1]
                x2, y2 = points[p2]
                if abs(x1 - x2) % 2 == 0 and abs(y1 - y2) % 2 == 0:
                    mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                    try:
                        return points.index((mid_x, mid_y))
                    except:
                        return None
                return None

            indices = list(range(total_dots))
            random.shuffle(indices)
            path = [indices.pop()]
            used.add(path[0])

            while len(path) < path_len and indices:
                random.shuffle(indices)
                for next_dot in indices:
                    if next_dot in used:
                        continue
                    pass_through = get_inline_passes(path[-1], next_dot)
                    if pass_through and pass_through not in used:
                        path.append(pass_through)
                        used.add(pass_through)
                    path.append(next_dot)
                    used.add(next_dot)
                    indices.remove(next_dot)
                    break

            # Generate image
            width, height = 400, 250
            padding_x, padding_y = 50, 30
            spacing_x = (width - 2 * padding_x) // (grid_size - 1)
            spacing_y = (height - 2 * padding_y) // (grid_size - 1)
            radius = 8 if grid_size >= 5 else 10

            def get_coords(index):
                x, y = points[index]
                return (padding_x + x * spacing_x, padding_y + y * spacing_y)

            img = Image.new("RGB", (width, height), "#000000")
            draw = ImageDraw.Draw(img)

            for i in range(total_dots):
                x, y = get_coords(i)
                fill_color = "#FFFFFF" if i in path else None
                draw.ellipse((x - radius, y - radius, x + radius, y + radius),
                             fill=fill_color, outline="#A9A9A9", width=2)

            for i in range(len(path) - 1):
                x1, y1 = get_coords(path[i])
                x2, y2 = get_coords(path[i + 1])
                draw.line((x1, y1, x2, y2), fill="#FFFFFF", width=4)

            # Save image
            buffer = io.BytesIO()
            img.save(buffer, format="WEBP")
            buffer.seek(0)

            # Upload image
            files = {'screenshot': ('pattern.webp', buffer, 'image/webp')}
            res = requests.post(UPLOAD_ENDPOINT, files=files)
            data = res.json()
            if not (data.get("status") and data.get("path")):
                print(f"❌ Upload failed for Q{qno}")
                continue
            img_url = f"https://backend.stawro.com/stawro/{data['path']}"

            # Generate options
            correct = len(path)
            options = {correct}
            while len(options) < 4:
                fake = random.randint(max(3, correct - 3), min(total_dots, correct + 3))
                options.add(fake)
            options = list(options)
            random.shuffle(options)

            # ans = ''

            # if options[0] == correct:
            #     ans = 'a'
            # elif options[1] == correct: 
            #     ans = 'b'
            # elif options[2] == correct:
            #     ans = 'c'
            # else:
            #     ans = 'd'

            # sec = ""

            if final_sec:
                if difficulty in ['Tough', "Too Tough"]:
                    sec = str(final_sec)
                elif difficulty in ['Medium', "Easy"]:
                    sec = str(final_sec)
                else:
                    sec = "25"
            else:
                if difficulty in ['Tough', 'Too Tough']:
                    sec = "12"
                else:
                    sec = "10"



            # Prepare payload for new API format
            payload = {
                "qno": qno,
                "Questio": "How many dots are connected in the pattern?",
                "Ans": str(correct),
                "a": str(options[0]),
                "b": str(options[1]),
                "c": str(options[2]),
                "d": str(options[3]),
                "lang": "English",
                "sub_lang": "Pattern_Lock",
                "tough": difficulty,
                "img": img_url,
                "seconds" : sec
                # "seconds": str(final_sec) if final_sec else ("10" if difficulty in ["Tough", "Too Tough"] else "12")
            }


            post_res = requests.post(POST_ENDPOINT, json=payload)
            if post_res.status_code == 200:
                print(f"✅ Q{qno} posted ({difficulty})")
            else:
                print(f"❌ Q{qno} failed: {post_res.status_code}")

        except Exception as e:
            print(f"❌ Exception in Q{qno}: {e}")

# done
def clock_crt(num_questions, difficulty, num):
    # get_sec = sec_data.find_one({"category": "clock", "Tough": difficulty}) or {}

    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0

    final_sec = 0

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

    def post_question(correct_answer, options, filename, difficulty):
        if final_sec:
            if difficulty in ['Tough', "Too Tough"]:
                sec = str(final_sec)
            elif difficulty in ['Medium', "Easy"]:
                sec = str(final_sec)
            else:
                sec = "25"
        else:
            if difficulty in ['Tough', 'Too Tough']:
                sec = "30"
            else:
                sec = "25"

        url = "http://localhost:81/api/question/change"

        body = {
            'qno': num,
            "Questio": "Guess the time shown on the clock.",
            "Ans": str(correct_answer),  # ✅ actual correct time, not option letter
            "a": options[0],
            "b": options[1],
            "c": options[2],
            "d": options[3],
            "lang": "English",
            "sub_lang": "clock",
            "tough": difficulty,
            "img": f"https://backend.stawro.com/stawro/uploads/{filename}",
            "seconds": sec
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
        img = draw_clock_image(time_data)
        filename = upload_image(img)
        if filename:
            success = post_question(correct_ans, options, filename, difficulty)
            if success:
                print("✅ Question posted successfully.")
                success_count += 1
            else:
                print("❌ Failed to post question.")
        else:
            print("❌ Image upload failed.")

    print(f"\n📊 Finished: {success_count}/{num_questions} posted successfully.")
    return success_count == num_questions

def corect_code_crt(total, level, num):
    UPLOAD_URL = "https://backend.stawro.com/stawro/upload.php"
    POST_URL = "http://localhost:81/api/question/change"
    CHARS = "abcdefghijklmnopqrstuvwxyz"

    # get_sec = sec_data.find_one({"category": "Code Guessing", "Tough": level}) or {}
    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0

    final_sec = 0

    DIFFICULTY_SETTINGS = {
        "Too Easy": {"code_length": 6, "seconds": 11},
        "Easy": {"code_length": 8, "seconds": 13},
        "Medium": {"code_length": 12, "seconds": 17},
        "Tough": {"code_length": 16, "seconds": 19},
        "Too Tough": {"code_length": 20, "seconds": 23}
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
        options = [correct]
        while len(options) < 4:
            mutated = mutate_two_letters(correct)
            if mutated not in options:
                options.append(mutated)
        random.shuffle(options)
        return options

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

    def post_question(correct_code, opts, image_path, difficulty, seconds):
        image_url = f"https://backend.stawro.com/stawro/{image_path}"
        option_keys = ['a', 'b', 'c', 'd']
        options_dict = dict(zip(option_keys, opts))

        if final_sec:
            if difficulty in ['Tough', "Too Tough"]:
                sec = str(final_sec)
            elif difficulty in ['Medium', "Easy"]:
                sec = str(final_sec)
            else:
                sec = str(seconds)
        else:
            sec = str(seconds)

        payload = {
            'qno': num,
            'Questio': "Guess the correct code",
            'Ans': correct_code,  # ✅ actual code, not option key
            'a': options_dict['a'],
            'b': options_dict['b'],
            'c': options_dict['c'],
            'd': options_dict['d'],
            'lang': "English",
            'sub_lang': "Code Guessing",
            'tough': difficulty,
            'img': image_url,
            "seconds": sec
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
                    print(f"✅ Q{i}: Posted Successfully!")
                    success_count += 1
                else:
                    print(f"❌ Q{i}: Failed to post.")
            else:
                print(f"❌ Q{i}: Image upload failed.")

        print(f"\n📊 Finished: {success_count}/{total_questions} successfully posted.")
        return success_count == total_questions

    return run_auto(total_questions=total, difficulty=level)

# done
def img_similar_crt(num, difficulty, qnoo):
    import os, random, requests
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO

    ALL_IMAGES = ["./main_ai/1.png", "./main_ai/2.png", "./main_ai/3.png", "./main_ai/4.png"]
    LABELS = ["A", "B", "C", "D"]
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost:81/api/question/change"

    # get_sec = sec_data.find_one({"category": "similar_images", "Tough": difficulty}) or {}
    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0

    final_sec = 0

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
        if final_sec:
            if difficulty in ['Tough', "Too Tough"]:
                sec = str(final_sec)
            elif difficulty in ['Medium', "Easy"]:
                sec = str(final_sec)
            else:
                sec = "25"
        else:
            sec = "25"

        payload = {
            "qno": qnoo,
            "Questio": "Which Pictures Are the Same?",
            "Ans": correct_answer,  # ✅ now direct answer, not option letter
            "a": options[0],
            "b": options[1],
            "c": options[2],
            "d": options[3],
            "lang": "English",
            "sub_lang": "similar_images",
            "tough": difficulty,
            "img": image_url,
            "seconds": sec
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

def int_char_mix_crt(num_questions, difficulty, num):
    # === CONFIG ===
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost:81/api/question/change"
    FONT_PATH = "arial.ttf"

    # get_sec = sec_data.find_one({"category": "Character Count", "Tough": difficulty}) or {}
    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0

    final_sec = 0

    type_q = ''

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
            "Too Easy": 15 if "numbers" in type_q else 20,
            "Easy": 16 if "numbers" in type_q else 25,
            "Medium": 15 if "numbers" in type_q else 22,
            "Tough": 15 if "numbers" in type_q else 26,
            "Too Tough": 17 if "numbers" in type_q else 25
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

    def post_question(question, correct_answer, options, image_url, difficulty):
        if final_sec:
            if difficulty in ['Tough', "Too Tough"]:
                sec = str(final_sec)
            elif difficulty in ['Medium', "Easy"]:
                sec = str(final_sec)
            else:
                sec = get_seconds_for_difficulty(difficulty)
        else:
            sec = get_seconds_for_difficulty(difficulty)

        payload = {
            "qno": num,
            "Questio": question,
            "Ans": str(correct_answer),  # ✅ actual value instead of a/b/c/d
            "a": str(options[0]),
            "b": str(options[1]),
            "c": str(options[2]),
            "d": str(options[3]),
            "lang": "English",
            "sub_lang": "Character Count",
            "tough": difficulty,
            "img": image_url,
            "seconds": sec
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

        length = {
            "Too Easy": 15,
            "Easy": 18,
            "Medium": 20,
            "Tough": 25,
            "Too Tough": 30
        }.get(difficulty, 25)

        random_string = get_random_string(length)
        mode = random.choice(["letters", "numbers"])
        type_q = mode
        correct_answer = count_letters(random_string) if mode == "letters" else count_numbers(random_string)
        question_text = f"How many {mode} are in the text below?"

        options_set = {correct_answer}
        while len(options_set) < 4:
            offset = random.randint(-5, 5)
            wrong = correct_answer + offset
            if wrong >= 0:
                options_set.add(wrong)
        options_list = list(options_set)
        random.shuffle(options_list)

        try:
            img_buffer = generate_image(random_string)
            image_url = upload_image(img_buffer)
            if image_url:
                if post_question(question_text, correct_answer, options_list, image_url, difficulty):
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

# done
def leter_count_crt(num_questions, user_input, num):
    import random, requests, io, time
    from PIL import Image, ImageDraw, ImageFont

    # === CONFIGURATION ===
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost:81/api/question/change"
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 250
    FONT_PATH = "arial.ttf"

    # get_sec = sec_data.find_one({"category": "leter_find", "Tough": user_input}) or {}
    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0

    final_sec = 0

    wordBank = [
        "bat", "cat", "dog", "hat", "sun", "bee", "cow", "run", "toy", "fun",
        "apple", "green", "light", "peace", "happy", "quiet", "under", "river", "dance", "mouse",
        "jungle", "planet", "bright", "summer", "market", "school", "garden", "memory", "castle", "cloudy",
        "elephant", "creation", "freedom", "triangle", "umbrella", "solution", "activity", "positive", "strategy", "momentum",
        "transparency", "psychology", "revolutionary", "architecture", "communication", "responsibility", "extraordinary", "transformation"
    ]

    difficulty_map = {
        "Too Easy": {"length_range": (3, 5), "seconds": 11},
        "Easy": {"length_range": (4, 6), "seconds": 11},
        "Medium": {"length_range": (5, 8), "seconds": 12},
        "Tough": {"length_range": (6, 10), "seconds": 13},
        "Too Tough": {"length_range": (8, 100), "seconds": 14}
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

    def generate_image(text):
        img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color="white")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(FONT_PATH, 18)
        except:
            font = ImageFont.load_default()

        words = text.split()
        lines, line = [], ""
        for word in words:
            if len(line + " " + word) < 40:
                line += " " + word
            else:
                lines.append(line.strip())
                line = word
        lines.append(line.strip())

        line_height = 22
        y = (IMAGE_HEIGHT - len(lines) * line_height) // 2

        for line in lines:
            text_width = draw.textlength(line, font=font)
            x = (IMAGE_WIDTH - text_width) // 2
            draw.text((x, y), line, fill="black", font=font)
            y += line_height

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf

    def upload_image(image_buf):
        files = {"screenshot": ("screenshot.png", image_buf, "image/png")}
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        if response.status_code == 200 and response.json().get("status"):
            return f"https://backend.stawro.com/stawro/{response.json()['path']}"
        else:
            raise Exception("Upload failed: " + response.text)

    def post_question(question_text, correct_value, option_map, image_url, difficulty):
        sec = ""
        if final_sec:
            sec = str(final_sec)
        else:
            sec = difficulty_map[difficulty]['seconds']

        payload = {
            "qno": num,
            "Questio": question_text,
            "Ans": str(correct_value),  # Correct number instead of option key
            "a": option_map["a"],
            "b": option_map["b"],
            "c": option_map["c"],
            "d": option_map["d"],
            "lang": "English",
            "sub_lang": "leter_find",
            "tough": difficulty,
            "img": image_url,
            "seconds": sec
        }

        try:
            response = requests.post(POST_ENDPOINT, json=payload, timeout=10)
            response.raise_for_status()
            print("✅ Question posted successfully!")
            return True
        except requests.exceptions.RequestException as e:
            print("❌ Post error:", e)
            return False

    success_count = 0
    difficulty = next((k for k in difficulty_map if k.lower() in user_input.lower()), "Medium")
    min_len, max_len = difficulty_map[difficulty]["length_range"]

    for i in range(num_questions):
        print(f"\n🔢 Generating question {i + 1}/{num_questions}...")

        try:
            sentence = generate_sentence(min_len, max_len)
            letter = get_random_letter(sentence)
            count = sentence.lower().count(letter)

            options = {count}
            while len(options) < 4:
                val = count + random.randint(-3, 3)
                if val >= 0:
                    options.add(val)

            options_list = list(map(str, options))
            random.shuffle(options_list)

            option_keys = ['a', 'b', 'c', 'd']
            option_map = {k: options_list[i] for i, k in enumerate(option_keys)}

            question_text = f'How many times does the letter "{letter}" appear in the sentence?'

            img_buffer = generate_image(sentence)
            image_url = upload_image(img_buffer)

            if post_question(question_text, count, option_map, image_url, difficulty):
                success_count += 1
                print(f"✅ Uploaded Question {i + 1}")
            else:
                print(f"❌ Skipped Question {i + 1} (post failed)")
        except Exception as e:
            print(f"❌ Error on Question {i + 1}: {e}")

        time.sleep(0.5)

    print(f"\n📊 Done! {success_count}/{num_questions} questions uploaded.")
    return success_count == num_questions

# done
def maze_crt(NUM_QUESTIONS, DIFFICULTY, num):
    UPLOAD_URL = "https://backend.stawro.com/stawro/upload.php"
    POST_URL = "http://localhost:81/api/question/change"

    # Get seconds config from DB
    # get_sec = sec_data.find_one({"category": "Maze Logic", "Tough": DIFFICULTY}) or {}
    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0

    final_sec = 0

    # Difficulty config for maze size & default seconds
    difficulty_config = {
        "Too Easy": {"size": 9, "seconds": 13},
        "Easy": {"size": 13, "seconds": 10},
        "Medium": {"size": 17, "seconds": 18},
        "Tough": {"size": 21, "seconds": 15},
        "Too Tough": {"size": 27, "seconds": 25}
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
            self.force_no = force_no
            self.player = (0, 0)

            attempt = 0
            while True:
                self.grid = [Cell(x, y) for y in range(ROWS) for x in range(COLS)]
                self.generate_maze()
                if self.force_no:
                    self.block_middle_path()
                reachable = self.is_goal_reachable()
                if self.force_no and not reachable:
                    break
                if not self.force_no and reachable:
                    break
                attempt += 1
                if attempt > 5:
                    break

        def index(self, x, y):
            return y * COLS + x if 0 <= x < COLS and 0 <= y < ROWS else -1

        def generate_maze(self):
            for cell in self.grid:
                cell.visited = False
                cell.walls = [True, True, True, True]
            stack = [self.grid[0]]
            self.grid[0].visited = True

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

        def block_middle_path(self):
            visited = set()
            queue = [(0, 0, [])]
            while queue:
                x, y, path = queue.pop(0)
                visited.add((x, y))
                if (x, y) == GOAL_POS and len(path) > 6:
                    bx, by = path[len(path) // 2]
                    for dx, dy, wall, opp_wall in [(0, -1, 0, 2), (1, 0, 1, 3), (0, 1, 2, 0), (-1, 0, 3, 1)]:
                        nx, ny = bx + dx, by + dy
                        if (nx, ny) in path and (nx, ny) != (0, 0):
                            idx1 = self.index(bx, by)
                            idx2 = self.index(nx, ny)
                            if idx1 != -1 and idx2 != -1:
                                self.grid[idx1].walls[wall] = True
                                self.grid[idx2].walls[opp_wall] = True
                                return
                    return
                cell = self.grid[self.index(x, y)]
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
            # ✅ Ans now stores actual value ("Yes"/"No")
            sec = ""
            if final_sec:
                if DIFFICULTY in ['Tough', "Too Tough", 'Medium', "Easy"]:
                    sec = str(final_sec)
                else:
                    sec = str(config['seconds'])
            else:
                sec = str(config['seconds'])

            payload = {
                "Questio": "Can blue reach red in this puzzle?",
                "Ans": answer,
                "a": "Yes",
                "b": "No",
                "c": "",
                "d": "",
                "qno": str(num),
                "lang": "English",
                "sub_lang": "Maze Logic",
                "tough": DIFFICULTY,
                "img": f"https://backend.stawro.com/stawro/{img_url}",
                "seconds": sec
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

# def num_100_crt(num_questions, difficulty, num):
#     UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
#     POST_ENDPOINT = "http://localhost:81/api/question/change"
#     FONT_PATH = "arial.ttf"

#     try:
#         assert difficulty in ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]
#     except Exception as e:
#         print(f"Error: {e}")
#         return False

#     def get_difficulty_params(difficulty):
#         if difficulty == "Too Easy":
#             return random.randint(2, 3), 10
#         elif difficulty == "Easy":
#             return random.randint(3, 4), 7
#         elif difficulty == "Medium":
#             return random.randint(5, 7), 5
#         elif difficulty == "Tough":
#             return random.randint(6, 10), 3
#         elif difficulty == "Too Tough":
#             return random.randint(10, 15), 1

#     def generate_question():
#         correct_series = list(range(1, 101))
#         display_series = correct_series[:]
#         wrong_count, confusion_range = get_difficulty_params(difficulty)
#         wrong_indexes = set()

#         while len(wrong_indexes) < wrong_count:
#             idx = random.randint(0, 99)
#             wrong_indexes.add(idx)

#         for idx in wrong_indexes:
#             while True:
#                 offset = random.randint(-confusion_range, confusion_range)
#                 wrong = correct_series[idx] + offset
#                 if 1 <= wrong <= 100 and wrong != correct_series[idx]:
#                     display_series[idx] = wrong
#                     break

#         correct_answer = wrong_count
#         options = {correct_answer}
#         while len(options) < 4:
#             offset = random.randint(-2, 2)
#             opt = correct_answer + offset
#             if 1 <= opt <= 100:
#                 options.add(opt)
#         options = sorted(list(options))
#         return display_series, correct_answer, options

#     def draw_grid(display_series):
#         img_width, img_height = 400, 250
#         image = Image.new("RGB", (img_width, img_height), "white")
#         draw = ImageDraw.Draw(image)

#         font_size = 14
#         try:
#             font = ImageFont.truetype(FONT_PATH, font_size)
#         except:
#             font = ImageFont.load_default()

#         cols = 10
#         rows = 10
#         margin = 5
#         box_width = (img_width - 2 * margin) // cols
#         box_height = (img_height - 2 * margin) // rows

#         for i, num in enumerate(display_series):
#             row = i // cols
#             col = i % cols
#             x = margin + col * box_width
#             y = margin + row * box_height
#             draw.rectangle([x, y, x + box_width - 2, y + box_height - 2], fill="#b1def5", outline="black")
#             draw.text((x + 8, y + 8), str(num), fill="black", font=font)
#         return image

#     def upload_image(image):
#         buffer = io.BytesIO()
#         image.save(buffer, format="WEBP")
#         buffer.seek(0)
#         files = {'screenshot': ('screenshot.webp', buffer, 'image/webp')}
#         try:
#             response = requests.post(UPLOAD_ENDPOINT, files=files)
#             data = response.json()
#             if data.get("status") and data.get("path"):
#                 return f"https://backend.stawro.com/stawro/{data['path']}"
#             else:
#                 print("❌ Upload failed.")
#                 return None
#         except Exception as e:
#             print(f"❌ Upload error: {e}")
#             return None
    
#     sec = ""

#     if difficulty in ['Too Easy', "Easy", "Medium", "Tough"]:
#         sec = "55" 
#     else:
#         sec = "60"
    

#     def post_question(image_path, correct_answer, options):
#         # payload = {
#         #     "question": "How many wrong numbers are in the table?",
#         #     "answer": str(correct_answer),
#         #     "a": str(options[0]),
#         #     "b": str(options[1]),
#         #     "c": str(options[2]),
#         #     "d": str(options[3]),
#         #     "language": "English",
#         #     "category": "Counting_100",
#         #     "difficulty": difficulty,
#         #     "type": "Mental Ability",
#         #     "image": image_path,
#         #     "seconds": "10"
#         # }

#         payload = {                
#             "img": image_path,
#             "Questio": "How many wrong numbers are present in the Table?",
#             "qno": num,
#             "a": str(options[0]),
#             "b": str(options[1]),
#             "c": str(options[2]),
#             "d": str(options[3]),
#             "Ans": str(correct_answer),
#             "lang": "English",
#             "tough": difficulty,
#             "seconds": sec,
#             "sub_lang": "Counting_100",

#         }


#         try:
#             res = requests.post(POST_ENDPOINT, json=payload)
#             if res.status_code == 200:
#                 print("✅ Question posted to database!")
#                 return True
#             else:
#                 print(f"❌ Failed to post question. Status code: {res.status_code}")
#                 return False
#         except Exception as e:
#             print(f"❌ Error posting question: {e}")
#             return False

#     # === MAIN LOOP ===
#     success_count = 0
#     for _ in range(num_questions):
#         display_series, correct_answer, options = generate_question()
#         image = draw_grid(display_series)
#         image_url = upload_image(image)
#         if image_url:
#             success = post_question(image_url, correct_answer, options)
#             if success:
#                 success_count += 1

#     if success_count == num_questions:
#         return True
#     else:
#         print(f"Only {success_count}/{num_questions} questions were successfully posted.")
#         return False


# done
def num_100_crt(num_questions, difficulty, num):
    import random, requests, io
    from PIL import Image, ImageDraw, ImageFont

    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost:81/api/question/change"
    FONT_PATH = "arial.ttf"

    # get_sec = sec_data.find_one({"category": "Counting_100", "Tough": difficulty}) or {}
    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0

    final_sec = 0

    if difficulty not in ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]:
        print("❌ Invalid difficulty")
        return False

    def get_difficulty_params(diff):
        if diff == "Too Easy":
            return random.randint(2, 3), 10
        elif diff == "Easy":
            return random.randint(3, 4), 7
        elif diff == "Medium":
            return random.randint(5, 7), 5
        elif diff == "Tough":
            return random.randint(6, 10), 3
        elif diff == "Too Tough":
            return random.randint(10, 15), 1

    def generate_question():
        correct_series = list(range(1, 101))
        display_series = correct_series[:]
        wrong_count, _ = get_difficulty_params(difficulty)
        wrong_indexes = set()

        while len(wrong_indexes) < wrong_count:
            idx = random.randint(0, 99)
            wrong_indexes.add(idx)

        for idx in wrong_indexes:
            display_series[idx] = ""  # remove the number (empty box)

        correct_answer = wrong_count
        options = {correct_answer}
        while len(options) < 4:
            offset = random.randint(-4, 4)
            opt = correct_answer + offset
            if 1 <= opt <= 100 and opt != correct_answer:
                options.add(opt)

        options_list = list(options)
        random.shuffle(options_list)
        return display_series, correct_answer, options_list

    def draw_grid(display_series):
        img_width, img_height = 400, 250
        image = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype(FONT_PATH, 14)
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
            if str(num).strip():
                draw.text((x + 8, y + 8), str(num), fill="black", font=font)

        return image

    def upload_image(image):
        buffer = io.BytesIO()
        image.save(buffer, format="WEBP")
        buffer.seek(0)
        files = {'screenshot': ('screenshot.webp', buffer, 'image/webp')}
        try:
            res = requests.post(UPLOAD_ENDPOINT, files=files, timeout=10)
            data = res.json()
            if data.get("status") and data.get("path"):
                return f"https://backend.stawro.com/stawro/{data['path']}"
            else:
                print("❌ Upload failed.")
                return None
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return None

    def post_question(image_path, correct_answer, options, q_number):
        sec = ""

        if final_sec:
            if difficulty in ['Tough', "Too Tough"]:
                sec = str(final_sec)
            elif difficulty in ['Medium', "Easy"]:
                sec = str(final_sec)
            else:
                sec = "15"
        else:
            if difficulty in ['Tough', 'Too Tough']:
                sec = "15"
            else:
                sec = "12"

        payload = {
            "img": image_path,
            "Questio": "How many numbers are missing from the Table?",
            "qno": q_number,
            "a": str(options[0]),
            "b": str(options[1]),
            "c": str(options[2]),
            "d": str(options[3]),
            "Ans": str(correct_answer),  # ✅ now sends the actual value, not the letter
            "lang": "English",
            "tough": difficulty,
            "sub_lang": "Counting_100",
            "seconds": sec
        }

        try:
            res = requests.post(POST_ENDPOINT, json=payload, timeout=10)
            if res.status_code == 200:
                print(f"✅ Q{q_number} posted.")
                return True
            else:
                print(f"❌ Q{q_number} failed. Status: {res.status_code}")
                return False
        except Exception as e:
            print(f"❌ Q{q_number} error: {e}")
            return False

    # MAIN LOOP
    success_count = 0
    for i in range(num_questions):
        print(f"\n📌 Generating Question {num + i}")
        display_series, correct_answer, options = generate_question()
        image = draw_grid(display_series)
        image_url = upload_image(image)
        if image_url:
            success = post_question(image_url, correct_answer, options, num + i)
            if success:
                success_count += 1

    if success_count == num_questions:
        print("🎯 All questions posted successfully.")
        return True
    else:
        print(f"❌ Only {success_count}/{num_questions} questions posted.")
        return False

# done
def numers_crt(num_questions, difficulty, num):
    # === CONFIG ===
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost:81/api/question/change"
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 250
    FONT_SIZE = 22
    FONT_PATH = None  # Use default font
    IMAGE_PADDING = 15  # Added padding around edges

    # get_sec = sec_data.find_one({"category": "Counting", "Tough": difficulty}) or {}
    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0

    final_sec = 0

    DIFFICULTY_CONFIG = {
        "Too Easy": {"option_range": (0, 5), "seconds": 20, "total_numbers": 14},
        "Easy": {"option_range": (0, 6), "seconds": 25, "total_numbers": 14},
        "Medium": {"option_range": (0, 8), "seconds": 20, "total_numbers": 15},
        "Tough": {"option_range": (0, 10), "seconds": 20, "total_numbers": 16},
        "Too Tough": {"option_range": (0, 12), "seconds": 25, "total_numbers": 17},
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
                while True:
                    rand_num = random.randint(10, 99)
                    if rand_num != target_number:
                        numbers.append(rand_num)
                        break

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

        placed_boxes = []
        max_attempts = 1000

        def is_overlapping(x, y, w, h):
            for px, py, pw, ph in placed_boxes:
                if (x < px + pw and x + w > px and y < py + ph and y + h > py):
                    return True
            return False

        for num in data["numbers"]:
            attempts = 0
            while attempts < max_attempts:
                text = str(num)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                x = random.randint(IMAGE_PADDING, IMAGE_WIDTH - IMAGE_PADDING - text_w)
                y = random.randint(IMAGE_PADDING, IMAGE_HEIGHT - IMAGE_PADDING - text_h)

                if not is_overlapping(x, y, text_w, text_h):
                    draw.text((x, y), text, fill=(
                        random.randint(100, 255),
                        random.randint(100, 255),
                        random.randint(100, 255)
                    ), font=font)
                    placed_boxes.append((x, y, text_w, text_h))
                    break
                attempts += 1

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

            if final_sec:
                if q["difficulty"] in ['Tough', "Too Tough"]:
                    sec = str(final_sec)
                elif q["difficulty"] in ['Medium', "Easy"]:
                    sec = str(final_sec)
                else:
                    sec = "30"
            else:
                if q["difficulty"] in ['Tough', 'Too Tough']:
                    sec = "30"
                else:
                    sec = "25"

            post_data = {
                "img": f'https://backend.stawro.com/stawro/{image_path}',
                "Questio": q["question"],
                "qno": num,
                "a": q["options"][0],
                "b": q["options"][1],
                "c": q["options"][2],
                "d": q["options"][3],
                "Ans": q["answer"],  # ✅ direct correct answer, no a/b/c/d mapping
                "lang": "English",
                "tough": q["difficulty"],
                "seconds": sec,
                "sub_lang": "Counting",
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

# done
def OMR_crt(num_questions, difficulty, num):
    UPLOAD_URL = "https://backend.stawro.com/stawro/upload.php"
    POST_URL = "http://localhost:81/api/question/change"
    ALLOWED_DIFFICULTIES = ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]

    # get_sec = sec_data.find_one({"category": "OMR Challenge", "Tough": difficulty}) or {}
    # seconds_list = get_sec.get('ex_seconds', []) or []
    # final_sec = sum(seconds_list) / len(seconds_list) if seconds_list else 0
    final_sec = 0

    if difficulty not in ALLOWED_DIFFICULTIES:
        print(f"❌ Invalid difficulty level. Allowed: {ALLOWED_DIFFICULTIES}")
        return False

    def generate_number_by_difficulty(diff):
        if diff == "Too Easy":
            return str(random.randint(1000, 9999)).zfill(4)
        elif diff == "Easy":
            return str(random.randint(100000, 999999)).zfill(6)
        elif diff == "Medium":
            return str(random.randint(1000000000, 9999999999))
        elif diff == "Tough":
            return str(random.randint(1000000000, 9999999999))
        elif diff == "Too Tough":
            return str(random.randint(100000000000, 999999999999))
        else:
            return str(random.randint(1000000000, 9999999999))

    def generate_options_based_on_difficulty(correct, diff):
        options = [correct]
        used = {correct}
        arr_len = len(correct)

        while len(options) < 4:
            arr = list(correct)

            if diff == "Too Easy":
                arr[arr_len // 2] = str(random.randint(0, 9))
            elif diff == "Easy":
                i = random.choice([arr_len // 2 - 1, arr_len // 2])
                arr[i] = str(random.randint(0, 9))
            elif diff == "Medium":
                i = random.choice([4, 5]) if arr_len > 5 else arr_len // 2
                arr[i] = str(random.randint(0, 9))
            elif diff == "Tough":
                i = random.randint(0, arr_len - 1)
                arr[i] = str(random.randint(0, 9))
            elif diff == "Too Tough":
                indices = random.sample(range(arr_len), random.randint(2, 3))
                for i in indices:
                    arr[i] = str(random.randint(0, 9))

            new_str = ''.join(arr)
            if new_str not in used:
                used.add(new_str)
                options.append(new_str)

        random.shuffle(options)
        return options

    def render_omr_image(number):
        width, height = 400, 250
        col_width = width // len(number)
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()

        for idx, digit in enumerate(number):
            x = idx * col_width + col_width // 2
            for i in range(10):
                y = 20 + i * 20
                r = 8
                fill_color = "#000000" if str(i) == digit else "#ffffff"
                outline_color = "#000000"
                draw.ellipse((x - r, y - r, x + r, y + r), fill=fill_color, outline=outline_color)
                try:
                    w, h = font.getsize(str(i))
                except AttributeError:
                    bbox = font.getbbox(str(i))
                    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text((x - w // 2, y - h // 2), str(i), fill="black", font=font)

        return img

    def upload_image(img):
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        files = {'screenshot': ('omr.png', buffer, 'image/png')}
        try:
            response = requests.post(UPLOAD_URL, files=files)
            data = response.json()
            if data.get("status") == "success":
                print(f"✅ Uploaded: {data.get('path')}")
                return data.get("path")
            else:
                print("❌ Upload failed.")
        except Exception as e:
            print("❌ Upload error:", e)
        return None

    def post_question(correct, options, image_path, diff):
        difficulty_seconds_map = {
            "Too Easy": "20",
            "Easy": "20",
            "Medium": "35",
            "Tough": "38",
            "Too Tough": "40"
        }

        # ✅ Send the actual correct answer instead of a/b/c/d
        ans = correct

        if final_sec:
            if diff in ['Tough', "Too Tough"]:
                sec = str(final_sec)
            elif diff in ['Medium', "Easy"]:
                sec = str(final_sec)
            else:
                sec = difficulty_seconds_map.get(diff, "20")
        else:
            sec = difficulty_seconds_map.get(diff, "20")

        payload = {
            'qno': num,
            "Questio": "What is the number shown in the OMR sheet?",
            "Ans": ans,  # ✅ Actual answer text here
            'a': options[0],
            'b': options[1],
            'c': options[2],
            'd': options[3],
            "lang": "English",
            "sub_lang": "OMR Challenge",
            "tough": diff,
            "img": f"https://backend.stawro.com/stawro/{image_path}",
            "seconds": sec
        }

        try:
            res = requests.post(POST_URL, json=payload)
            if res.ok:
                print("✅ Question posted successfully!")
                return True
            else:
                print("❌ Failed to post question.")
                return False
        except Exception as e:
            print("❌ Error posting question:", e)
            return False

    # Main Loop
    success_count = 0

    for _ in range(num_questions):
        correct = generate_number_by_difficulty(difficulty)
        options = generate_options_based_on_difficulty(correct, difficulty)

        print(f"\n🎯 Correct Number: {correct}")
        print("🧠 Options:")
        for opt in options:
            print(" -", opt)

        image = render_omr_image(correct)
        path = upload_image(image)

        if path:
            if post_question(correct, options, path, difficulty):
                success_count += 1

    if success_count == num_questions:
        print(f"\n✅ All {num_questions} questions posted successfully.")
        return True
    else:
        print(f"\n⚠️ Only {success_count}/{num_questions} questions posted.")
        return False



def change_qn(qno, new_toughness, cat):
    if cat == 'Counting':
        numers_crt(1, new_toughness, qno)
    elif cat == 'Counting_100':
        num_100_crt(1, new_toughness, qno)
    elif cat == 'Maze Logic':
        maze_crt(1, new_toughness, qno)
    elif cat == 'leter_find':
        leter_count_crt(1, new_toughness, qno)
    elif cat == 'Character Count':
        int_char_mix_crt(1, new_toughness, qno)
    elif cat == 'similar_images':
        img_similar_crt(1, new_toughness, qno)
    elif cat == 'Code Guessing':
        corect_code_crt(1, new_toughness, qno)
    elif cat == 'clock':
        clock_crt(1, new_toughness, qno)
    elif cat == 'Pattern_Lock':
        generate_pattern_mcq_post(1, new_toughness, qno)
    elif cat == "OMR Challenge":
        OMR_crt(1,new_toughness, qno)
    else:
        stop_start("off")
        print(f"\033[91m⚠️ Unknown category: {cat}\033[0m")
        return False

    



# === Main loop ===
while True:
    os.system("cls" if os.name == "nt" else "clear")

    docs = list(collection.find().sort("qno", 1))
    existing_qnos = set()
    unexpected_qnos = []

    print(f"\nTotal documents: {len(docs)}\n")

    # ✅ Detect and show duplicate qnos
    qno_docs_map = defaultdict(list)
    for doc in docs:
        qno_str = str(doc.get("qno", "0")).strip()
        qno_docs_map[qno_str].append(doc)

    duplicates = {qno: entries for qno, entries in qno_docs_map.items() if len(entries) > 1}

    if duplicates:
        print("\n\033[91m⚠️ Duplicate QNOs Detected and Will Be Cleaned:\033[0m")
        for qno, entries in duplicates.items():
            print(f"\033[91m - Q{qno} appears {len(entries)} times\033[0m")

            # Keep only one (the first), delete others
            to_delete = entries[1:]  # skip the first entry
            for doc in to_delete:
                collection.delete_one({"_id": ObjectId(doc["_id"])})
            print(f"\033[92m   ✔️ Deleted {len(to_delete)} duplicates of Q{qno}\033[0m")
    else:
        print("\n\033[92m✅ No duplicate QNOs found.\033[0m")

    # Step 1: Analyze in-range questions
    for expected_qno in range(1, expected_range + 1):
        found = False
        for data in docs:
            qno = int(data.get("qno", 0))
            if qno == expected_qno:
                found = True
                existing_qnos.add(qno)
                
                yes_list = data.get("yes", [])
                count = len(yes_list)
                tough = data.get("tough", "Unknown")
                cat = data.get("sub_lang", "Unknown")

                if count > 1:
                    if tough in ['Too Tough', 'Tough']:
                        print(f'\033[31mQ{qno}: Change to TOUGH (Already tough) — Count: {count}\033[0m')
                        change_qn(qno, tough, cat)
                    elif tough == 'Medium':
                        print(f'\033[93mQ{qno}: Change to MEDIUM — Count: {count}\033[0m')
                        change_qn(qno, tough, cat)
                    elif count > 1:
                        print(f'\033[94mQ{qno}: Change to EASY — Count: {count}\033[0m')
                        change_qn(qno, tough, cat)
                    else:
                        print(f'\033[93mQ{qno}: Answered > 2 times — Count: {count}\033[0m')
                else:
                    print(f'\033[92mQ{qno}: ✅ Good — Count: {count}\033[0m')
                break

        if not found:
            # stop_start("off")
            print(f'\033[95m⚠️ Missing Question Q{expected_qno} — Not Found in DB\033[0m')
            data = change_qn(expected_qno, "Medium", "clock")
            print(data)
            print(f"\033[92m✅ Question Q{expected_qno} created successfully.\033[0m")



    # Step 2: Find and delete out-of-range questions
    for data in docs:
        qno = int(data.get("qno", 0))
        if qno < 1 or qno > expected_range:
            unexpected_qnos.append(qno)

    if unexpected_qnos:
        stop_start("off")  # Stop system
        print("\n\033[91m⚠️ Deleting Out-of-Range Question Numbers (Not 1–100):\033[0m")
        for uq in sorted(set(unexpected_qnos)):
            print(f"\033[91m - Deleting Q{uq}...\033[0m")
            result = collection.delete_many({"qno": uq})
        print("\033[92m✅ All unexpected questions deleted successfully.\033[0m")
        stop_start("on")

    else:
        print("\n\033[92m✅ All question numbers are within the range 1–100.\033[0m")

    # Wait before next scan
    speak("I am Reporting, Everything is Ok sir.")
    print("\033[92mEverything Ok Sir\033[0m")
    time.sleep(5)
    


import io
import random
import requests
from PIL import Image, ImageDraw, ImageFont

def generate_digit_count_mcq_post(num, difficulty, qno_start):
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost:81/api/question/change"

    ALLOWED_DIFFICULTIES = ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]

    # Difficulty ranges for start-end numbers
    DIFFICULTY_RANGES = {
        "Too Easy": (10, 20),
        "Easy": (20, 40),
        "Medium": (40, 80),
        "Tough": (80, 150),
        "Too Tough": (150, 300)
    }

    # Seconds logic for each difficulty
    DIFFICULTY_SECONDS = {
        "Too Easy": "25",
        "Easy": "25",
        "Medium": "15",
        "Tough": "19",
        "Too Tough": "19"
    }

    def generate_options(correct, difficulty):
        spread = {
            "Too Easy": 2,
            "Easy": 2,
            "Medium": 4,
            "Tough": 6,
            "Too Tough": 6
        }[difficulty]
        options = {correct}
        while len(options) < 4:
            val = max(0, correct + random.randint(-spread, spread))
            options.add(val)
        return random.sample(list(options), 4)

    if difficulty not in ALLOWED_DIFFICULTIES:
        raise ValueError(f"Invalid difficulty. Choose from: {ALLOWED_DIFFICULTIES}")

    min_gap, max_gap = DIFFICULTY_RANGES[difficulty]
    seconds = DIFFICULTY_SECONDS[difficulty]

    for i in range(num):
        qno = str(int(qno_start) + i)
        try:
            # Choose random digit 0-9
            target_digit = random.randint(0, 9)

            # Choose start and end numbers based on difficulty
            start = random.randint(1, 100)
            end = start + random.randint(min_gap, max_gap)

            # Count numbers containing the target digit
            correct_answer = sum(1 for n in range(start, end + 1) if str(target_digit) in str(n))

            # Generate options
            options = generate_options(correct_answer, difficulty)

            # Create image
            img = Image.new("RGB", (400, 250), "white")
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 120)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0,0), str(target_digit), font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            x = (400 - text_w) / 2
            y = (250 - text_h) / 2
            draw.text((x, y), str(target_digit), fill=(0,0,0), font=font)

            # Save to buffer
            buffer = io.BytesIO()
            img.save(buffer, format="WEBP")
            buffer.seek(0)

            # Upload image
            files = {'screenshot': ('digit_count.webp', buffer, 'image/webp')}
            res = requests.post(UPLOAD_ENDPOINT, files=files)
            data = res.json()
            if not (data.get("status") and data.get("path")):
                print(f"❌ Upload failed for Q{qno}")
                continue
            img_url = f"https://backend.stawro.com/stawro/{data['path']}"

            # Prepare payload
            payload = {
                "qno": qno,
                "Questio": f"How many numbers between {start} and {end} contain the digit '{target_digit}'?",
                "Ans": str(correct_answer),
                "a": str(options[0]),
                "b": str(options[1]),
                "c": str(options[2]),
                "d": str(options[3]),
                "lang": "English",
                "sub_lang": "Digit_Count",
                "tough": difficulty,
                "img": img_url,
                "seconds": seconds
            }

            # Post to backend
            post_res = requests.post(POST_ENDPOINT, json=payload)
            if post_res.status_code == 200:
                print(f"✅ Q{qno} posted ({difficulty}) → Ans: {correct_answer}")
            else:
                print(f"❌ Q{qno} failed: {post_res.status_code}")

        except Exception as e:
            print(f"❌ Exception in Q{qno}: {e}")

# Example usage
if __name__ == "__main__":
    generate_digit_count_mcq_post(num=1, difficulty="Medium", qno_start=1931)





















# import io
# import random
# import requests
# from PIL import Image, ImageDraw, ImageFont

# def generate_stroop_mcq_post(num, difficulty, qno):
#     UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
#     POST_ENDPOINT = "http://localhost:81/api/question/change"

#     ALLOWED_DIFFICULTIES = ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]

#     COLOR_NAMES = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange"]
#     COLOR_RGB = {
#         "Red": (255, 0, 0),
#         "Green": (0, 200, 0),
#         "Blue": (0, 0, 255),
#         "Yellow": (255, 215, 0),
#         "Purple": (128, 0, 128),
#         "Orange": (255, 140, 0)
#     }

#     DIFFICULTY_SETTINGS = {
#         "Too Easy": (3, 4, 0.8),
#         "Easy": (4, 5, 0.5),
#         "Medium": (5, 6, 0.3),
#         "Tough": (6, 7, 0.2),
#         "Too Tough": (7, 8, 0.15)
#     }

#     def generate_options(correct, difficulty):
#         spread = {
#             "Too Easy": 2,
#             "Easy": 2,
#             "Medium": 4,
#             "Tough": 6,
#             "Too Tough": 6
#         }[difficulty]
#         options = {correct}
#         while len(options) < 4:
#             val = max(0, correct + random.randint(-spread, spread))
#             options.add(val)
#         return random.sample(list(options), 4)

#     if difficulty not in ALLOWED_DIFFICULTIES:
#         raise ValueError(f"Invalid difficulty. Choose from: {ALLOWED_DIFFICULTIES}")

#     rows, cols, match_ratio = DIFFICULTY_SETTINGS[difficulty]

#     for q in range(1, num + 1):
#         try:
#             img = Image.new("RGB", (400, 250), "white")
#             draw = ImageDraw.Draw(img)

#             try:
#                 font = ImageFont.truetype("arial.ttf", 20)
#             except:
#                 font = ImageFont.load_default()

#             matches = 0
#             cell_w = 400 // cols
#             cell_h = (250 - 40) // rows  # leave space at top

#             for r in range(rows):
#                 for c in range(cols):
#                     word = random.choice(COLOR_NAMES)
#                     if random.random() < match_ratio:
#                         ink_color = COLOR_RGB[word]
#                         matches += 1
#                     else:
#                         ink_color = COLOR_RGB[random.choice([clr for clr in COLOR_NAMES if clr != word])]

#                     bbox = draw.textbbox((0, 0), word, font=font)
#                     text_w = bbox[2] - bbox[0]
#                     text_h = bbox[3] - bbox[1]

#                     x = c * cell_w + (cell_w - text_w) / 2
#                     y = r * cell_h + (cell_h - text_h) / 2 + 40
#                     draw.text((x, y), word, fill=ink_color, font=font)

#             # Save to buffer
#             buffer = io.BytesIO()
#             img.save(buffer, format="WEBP")
#             buffer.seek(0)

#             # Upload image
#             files = {'screenshot': ('stroop.webp', buffer, 'image/webp')}
#             res = requests.post(UPLOAD_ENDPOINT, files=files)
#             data = res.json()
#             if not (data.get("status") and data.get("path")):
#                 print(f"❌ Upload failed for Q{q}")
#                 continue
#             img_url = f"https://backend.stawro.com/stawro/{data['path']}"

#             # Generate options
#             correct_answer = matches
#             options = generate_options(correct_answer, difficulty)

#             # Seconds logic (basic)
#             if difficulty in ['Tough', "Too Tough"]:
#                 sec = "19"
#             elif difficulty in ['Medium', "Easy"]:
#                 sec = "15"
#             else:
#                 sec = "25"

#             # Prepare payload
#             payload = {
#                 "qno": qno,
#                 "Questio": "Count the entries where the WORD matches the INK COLOR.",
#                 "Ans": str(correct_answer),
#                 "a": str(options[0]),
#                 "b": str(options[1]),
#                 "c": str(options[2]),
#                 "d": str(options[3]),
#                 "lang": "English",
#                 "sub_lang": "Stroop_Challenge",
#                 "tough": difficulty,
#                 "img": img_url,
#                 "seconds": sec
#             }

#             # Post to backend
#             post_res = requests.post(POST_ENDPOINT, json=payload)
#             if post_res.status_code == 200:
#                 print(f"✅ Q{q} posted ({difficulty}) → Ans: {correct_answer}")
#             else:
#                 print(f"❌ Q{q} failed: {post_res.status_code}")

#         except Exception as e:
#             print(f"❌ Exception in Q{q}: {e}")

# # Example run
# if __name__ == "__main__":
#     generate_stroop_mcq_post(num=1, difficulty="Too Easy", qno="19311")














import io
import random
import requests
from PIL import Image, ImageDraw, ImageFont

def generate_stroop_mcq_post(num, difficulty, start_qno):
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://localhost:81/api/question/change"

    ALLOWED_DIFFICULTIES = ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]

    COLOR_NAMES = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange"]
    COLOR_RGB = {
        "Red": (255, 0, 0),
        "Green": (0, 200, 0),
        "Blue": (0, 0, 255),
        "Yellow": (255, 215, 0),
        "Purple": (128, 0, 128),
        "Orange": (255, 140, 0)
    }

    DIFFICULTY_SETTINGS = {
        "Too Easy": (3, 4, 0.8),
        "Easy": (4, 5, 0.5),
        "Medium": (5, 6, 0.3),
        "Tough": (6, 7, 0.2),
        "Too Tough": (7, 8, 0.15)
    }

    def generate_options(correct, difficulty):
        spread = {
            "Too Easy": 2,
            "Easy": 2,
            "Medium": 4,
            "Tough": 6,
            "Too Tough": 6
        }[difficulty]
        options = {correct}
        while len(options) < 4:
            val = max(0, correct + random.randint(-spread, spread))
            options.add(val)
        return random.sample(list(options), 4)

    if difficulty not in ALLOWED_DIFFICULTIES:
        raise ValueError(f"Invalid difficulty. Choose from: {ALLOWED_DIFFICULTIES}")

    rows, cols, match_ratio = DIFFICULTY_SETTINGS[difficulty]

    for i in range(num):
        qno = str(int(start_qno) + i)
        try:
            img = Image.new("RGB", (400, 250), "white")
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()

            matches = 0
            top_margin = 35
            cell_w = 400 // cols
            cell_h = (250 - top_margin) // rows  # leave space at top

            for r in range(rows):
                for c in range(cols):
                    word = random.choice(COLOR_NAMES)
                    if random.random() < match_ratio:
                        ink_color = COLOR_RGB[word]
                        matches += 1
                    else:
                        ink_color = COLOR_RGB[random.choice([clr for clr in COLOR_NAMES if clr != word])]

                    bbox = draw.textbbox((0, 0), word, font=font)
                    text_w = bbox[2] - bbox[0]
                    text_h = bbox[3] - bbox[1]

                    x = c * cell_w + (cell_w - text_w) / 2
                    y = r * cell_h + (cell_h - text_h) / 2 + top_margin
                    draw.text((x, y), word, fill=ink_color, font=font)

            # Save to buffer
            buffer = io.BytesIO()
            img.save(buffer, format="WEBP")
            buffer.seek(0)

            # Upload image
            files = {'screenshot': ('stroop.webp', buffer, 'image/webp')}
            res = requests.post(UPLOAD_ENDPOINT, files=files)
            data = res.json()
            if not (data.get("status") and data.get("path")):
                print(f"❌ Upload failed for Q{qno}")
                continue
            img_url = f"https://backend.stawro.com/stawro/{data['path']}"

            # Generate options
            correct_answer = matches
            options = generate_options(correct_answer, difficulty)

            # Seconds logic
            if difficulty in ['Tough', "Too Tough"]:
                sec = "19"
            elif difficulty in ['Medium', "Easy"]:
                sec = "15"
            else:
                sec = "25"

            # Prepare payload
            payload = {
                "qno": qno,
                "Questio": "Count the entries where the WORD matches the INK COLOR.",
                "Ans": str(correct_answer),
                "a": str(options[0]),
                "b": str(options[1]),
                "c": str(options[2]),
                "d": str(options[3]),
                "lang": "English",
                "sub_lang": "Stroop_Challenge",
                "tough": difficulty,
                "img": img_url,
                "seconds": sec
            }

            # Post to backend
            post_res = requests.post(POST_ENDPOINT, json=payload)
            if post_res.status_code == 200:
                print(f"✅ Q{qno} posted ({difficulty}) → Ans: {correct_answer}")
            else:
                print(f"❌ Q{qno} failed: {post_res.status_code}")

        except Exception as e:
            print(f"❌ Exception in Q{qno}: {e}")

# Example run
if __name__ == "__main__":
    generate_stroop_mcq_post(num=1, difficulty="Too Easy", start_qno="19311")














import io
import random
import requests
from PIL import Image, ImageDraw, ImageFont

# Configuration
UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
POST_ENDPOINT = "http://localhost:81/api/question/change"

alphabet = [chr(i) for i in range(97, 123)]  # a-z
colors = ["red","blue","green","orange","purple","brown","pink","teal"]

difficultySettings = {
    "Too Easy":  {"mistakes":[1,2], "rotation":5,  "colorCount":2, "letterFraction":0.3},
    "Easy":      {"mistakes":[2,3], "rotation":10, "colorCount":3, "letterFraction":0.5},
    "Medium":    {"mistakes":[3,4], "rotation":15, "colorCount":5, "letterFraction":0.7},
    "Tough":     {"mistakes":[4,5], "rotation":20, "colorCount":6, "letterFraction":0.9},
    "Too Tough": {"mistakes":[5,6], "rotation":30, "colorCount":8, "letterFraction":1.0}
}

def generate_alphabet_question( num=1, difficulty="Medium", qno_start=1):
    for i in range(num):
        qno = str(int(qno_start) + i)
        settings = difficultySettings[difficulty]
        
        # Container settings
        width, height = 400, 250
        letter_size = 24
        letters_per_row = width // letter_size
        rows = height // letter_size
        total_letters = int(letters_per_row * rows * settings["letterFraction"])
        
        # Generate sequence
        sequence = []
        while len(sequence) < total_letters:
            sequence += alphabet
        sequence = sequence[:total_letters]
        
        # Decide type: wrong or missing
        q_type = random.choice(["wrong", "missing"])
        
        # Generate mistakes indexes
        mistake_count = random.randint(settings["mistakes"][0], settings["mistakes"][1])
        mistake_indexes = random.sample(range(total_letters), mistake_count)
        
        # Create image
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        top_margin = 5
        cell_w = width // letters_per_row
        cell_h = (height - top_margin) // rows
        
        for idx, letter in enumerate(sequence):
            if idx in mistake_indexes:
                if q_type == "wrong":
                    letter = letter.upper()
                else:
                    letter = ""
            x = (idx % letters_per_row) * cell_w + cell_w//4
            y = (idx // letters_per_row) * cell_h + top_margin
            color_idx = random.randint(0, min(settings["colorCount"]-1, len(colors)-1))
            rot = random.uniform(-settings["rotation"], settings["rotation"])
            
            # Draw rotated text
            temp_img = Image.new("RGBA", (cell_w, cell_h), (255,255,255,0))
            temp_draw = ImageDraw.Draw(temp_img)
            temp_draw.text((0,0), letter, font=font, fill=colors[color_idx])
            rotated = temp_img.rotate(rot, expand=1)
            img.paste(rotated, (x, y), rotated)
        
        # Save image to buffer
        buffer = io.BytesIO()
        img.save(buffer, format="WEBP")
        buffer.seek(0)
        
        # Upload image
        files = {'screenshot': ('alphabet.webp', buffer, 'image/webp')}
        res = requests.post(UPLOAD_ENDPOINT, files=files)
        data = res.json()
        if not (data.get("status") and data.get("path")):
            print(f"❌ Upload failed for Q{qno}")
            continue
        img_url = f"https://backend.stawro.com/stawro/{data['path']}"
        
        # Generate options
        options = [mistake_count]
        while len(options) < 4:
            opt = random.randint(0, settings["mistakes"][1]+2)
            if opt not in options:
                options.append(opt)
        random.shuffle(options)
        
        # Seconds based on difficulty
        sec_map = {"Too Easy":25,"Easy":20,"Medium":15,"Tough":12,"Too Tough":10}
        seconds = sec_map.get(difficulty, 15)
        
        # Prepare payload
        payload = {
            "qno": qno,
            "Questio": f"Count the {'WRONG letters (uppercase)' if q_type=='wrong' else 'MISSING letters'} in the sequence.",
            "Ans": str(mistake_count),
            "a": str(options[0]),
            "b": str(options[1]),
            "c": str(options[2]),
            "d": str(options[3]),
            "lang": "English",
            "sub_lang": "Alphabet_Challenge",
            "tough": difficulty,
            "img": img_url,
            "seconds": str(seconds)
        }
        
        # Post to backend
        post_res = requests.post(POST_ENDPOINT, json=payload)
        if post_res.status_code == 200:
            print(f"✅ Q{qno} posted ({difficulty}) → Ans: {mistake_count}")
        else:
            print(f"❌ Q{qno} failed: {post_res.status_code}")

# Example usage
if __name__ == "__main__":
    generate_alphabet_question( num=1, difficulty="Too Tough", qno_start=1931)
