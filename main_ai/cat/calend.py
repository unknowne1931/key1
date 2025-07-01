# everything ok

import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



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
    num = int(input("Enter number of questions to generate: "))
    difficulty = input("Enter difficulty (Too Easy, Easy, Medium, Tough, Too Tough): ").strip()

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
