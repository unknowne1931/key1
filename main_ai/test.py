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


def numers_crt(num_questions, difficulty):
    # === CONFIG ===
    UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
    POST_ENDPOINT = "http://192.168.31.44/api/question"
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 250
    FONT_SIZE = 22
    FONT_PATH = None  # Use default font
    IMAGE_PADDING = 15  # Added padding around edges

    DIFFICULTY_CONFIG = {
        "Too Easy": {"option_range": (0, 5), "seconds": 15, "total_numbers": 15},
        "Easy": {"option_range": (0, 6), "seconds": 12, "total_numbers": 23},
        "Medium": {"option_range": (0, 8), "seconds": 10, "total_numbers": 26},
        "Tough": {"option_range": (0, 10), "seconds": 8, "total_numbers": 30},
        "Too Tough": {"option_range": (0, 12), "seconds": 7, "total_numbers": 40},
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
                # ensure we don't accidentally add the target number
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
        max_attempts = 1000  # Avoid infinite loops

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

numers_crt(5, "Too Easy")