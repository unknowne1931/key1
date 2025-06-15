# import random
# import io
# import requests
# from PIL import Image, ImageDraw, ImageFont

# # === CONFIG ===
# UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
# POST_ENDPOINT = "http://localhost/api/question"
# IMAGE_WIDTH = 400
# IMAGE_HEIGHT = 250
# FONT_SIZE = 22
# FONT_PATH = None  # Use default font

# # Difficulty settings
# DIFFICULTY_CONFIG = {
#     "Too Easy":    {"target_prob": 0.4, "total": 25, "option_range": (0, 5), "seconds": 20},
#     "Easy":        {"target_prob": 0.3, "total": 30, "option_range": (0, 7), "seconds": 18},
#     "Medium":      {"target_prob": 0.2, "total": 35, "option_range": (0, 9), "seconds": 15},
#     "Tough":       {"target_prob": 0.15, "total": 40, "option_range": (0, 10), "seconds": 12},
#     "Too Tough":   {"target_prob": 0.1, "total": 50, "option_range": (0, 12), "seconds": 10},
# }


# def generate_question(difficulty):
#     config = DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["Medium"])
#     target_number = random.randint(10, 99)
#     numbers = []
#     count = 0

#     for _ in range(config["total"]):
#         if random.random() < config["target_prob"]:
#             numbers.append(target_number)
#             count += 1
#         else:
#             rand_num = random.randint(10, 99)
#             numbers.append(rand_num)

#     # Generate options
#     option_low, option_high = config["option_range"]
#     options = list(set(random.sample(range(option_low, option_high + 1), 5)))

#     if count not in options:
#         options[random.randint(0, 4)] = count

#     random.shuffle(options)

#     # Ensure 4 options with possibility of 'None of the above'
#     include_none = random.choice([True, False])
#     if include_none:
#         if count in options:
#             options.remove(count)
#             correct_answer = "None of the above"
#         else:
#             correct_answer = str(count)
#         options = options[:3]  # Keep only 3 incorrect ones
#         options.append("None of the above")
#     else:
#         correct_answer = str(count)
#         if count not in options:
#             options[random.randint(0, 3)] = count
#         options = options[:4]

#     random.shuffle(options)

#     return {
#         "question": f"How many times does the number \"{target_number}\" appear?",
#         "answer": correct_answer,
#         "target": target_number,
#         "options": options[:4],
#         "numbers": numbers,
#         "correct_count": count,
#         "difficulty": difficulty,
#         "seconds": config["seconds"]  # ← Added
#     }



# def render_image(data):
#     img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color=(58, 54, 54))
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.load_default() if FONT_PATH is None else ImageFont.truetype(FONT_PATH, FONT_SIZE)

#     for _ in range(len(data["numbers"])):
#         x = random.randint(0, IMAGE_WIDTH - 30)
#         y = random.randint(0, IMAGE_HEIGHT - 30)
#         num = random.choice(data["numbers"])
#         draw.text((x, y), str(num), fill=(random.randint(100,255), random.randint(100,255), random.randint(100,255)), font=font)

#     buffer = io.BytesIO()
#     img.save(buffer, format="PNG")
#     buffer.seek(0)
#     return buffer

# def upload_image(image_bytes):
#     files = {'screenshot': ("screenshot.png", image_bytes, 'image/png')}
#     try:
#         response = requests.post(UPLOAD_ENDPOINT, files=files)
#         if response.status_code == 200:
#             return response.json().get("path")
#     except Exception as e:
#         print("Upload Error:", e)
#     return None

# def post_question(data):
#     try:
#         response = requests.post(POST_ENDPOINT, json=data)
#         return response.json()
#     except Exception as e:
#         print("Post Error:", e)
#         return {}

# def main():
#     print("Available difficulty levels: Too Easy, Easy, Medium, Tough, Too Tough")
#     difficulty = input("Enter difficulty: ").strip()

#     num_questions = int(input("How many questions to generate? ").strip())
#     for i in range(num_questions):
#         print(f"\nGenerating Question {i+1}/{num_questions}")
#         q = generate_question(difficulty)
#         image_stream = render_image(q)
#         image_path = upload_image(image_stream)
#         if not image_path:
#             print("❌ Failed to upload image.")
#             continue

#         post_data = {
#             "question": q["question"],
#             "answer": q["answer"],
#             "a": q["options"][0],
#             "b": q["options"][1],
#             "c": q["options"][2],
#             "d": q["options"][3],
#             "language": "English",
#             "category": "Counting",
#             "difficulty": q["difficulty"],
#             "type": "Mental Ability",
#             "image": f"https://backend.stawro.com/stawro/{image_path}",
#             "seconds": str(q["seconds"])  # ← Dynamic seconds based on difficulty
#         }


#         result = post_question(post_data)
#         print("📥 Response from API:", result)
#         if "Question added successfully" in result or result.get("message") == "Question added successfully":
#             print("\033[92m✅ Question posted successfully!\033[0m")
#         else:
#             print("⚠️ Failed to post question.")

# if __name__ == "__main__":
#     main()
























import random
import io
import requests
from PIL import Image, ImageDraw, ImageFont

# === CONFIG ===
UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
POST_ENDPOINT = "http://localhost/api/question"
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 250
FONT_SIZE = 22
FONT_PATH = None  # Use default font

# Difficulty settings
DIFFICULTY_CONFIG = {
    "Too Easy": {"option_range": (0, 5), "seconds": 15},
    "Easy": {"option_range": (0, 6), "seconds": 12},
    "Medium": {"option_range": (0, 8), "seconds": 10},
    "Tough": {"option_range": (0, 10), "seconds": 8},
    "Too Tough": {"option_range": (0, 12), "seconds": 7},
}

def generate_question(difficulty):
    config = DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["Medium"])
    target_number = random.randint(10, 99)
    total_numbers = 30
    numbers = []
    count = 0

    for _ in range(total_numbers):
        if random.random() < 0.2:
            numbers.append(target_number)
            count += 1
        else:
            rand_num = random.randint(10, 99)
            numbers.append(rand_num)

    include_none = random.random() < 0.4  # 40% chance
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

    for _ in range(30):
        x = random.randint(0, IMAGE_WIDTH - 30)
        y = random.randint(0, IMAGE_HEIGHT - 30)
        num = random.choice(data["numbers"])
        draw.text((x, y), str(num), fill=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), font=font)

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
    print("Available difficulty levels: Too Easy, Easy, Medium, Tough, Too Tough")
    difficulty = input("Enter difficulty: ").strip()

    num_questions = int(input("How many questions to generate? ").strip())
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
        if isinstance(result, dict) and ("Question added successfully" in result.get("message", "") or result.get("message") == "Question added successfully"):
            print("\033[92m✅ Question posted successfully!\033[0m")
        else:
            print("⚠️ Failed to post question.")

if __name__ == "__main__":
    main()
