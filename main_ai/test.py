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




def img_similar_crt(num, difficulty):
    # ---- Configuration ----
    ALL_IMAGES = ["./main_ai/1.png", "./main_ai/2.png", "./main_ai/3.png", "./main_ai/4.png"]
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


img_similar_crt(10, "Tough")