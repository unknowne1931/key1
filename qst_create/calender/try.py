##Everything fine make add some styling

from PIL import Image, ImageDraw, ImageFont
import calendar
import random
import requests
from io import BytesIO

# Config
API_UPLOAD = "https://backend.stawro.com/stawro/upload.php"
API_POST = "http://192.168.31.44/api/question"
FONT_PATH = "arial.ttf"  # Ensure this font exists or change path
YEAR = 2024

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
        delta = random.choice([-2, -1, 1, 2])  # default fallback

    x_day = hint_day + delta
    x_day = max(1, min(max_day, x_day))
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

def upload_image(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    files = {'screenshot': ('calendar.png', buffer, 'image/png')}
    response = requests.post(API_UPLOAD, files=files)
    data = response.json()
    return f"https://backend.stawro.com/stawro/{data['path']}" if data.get("status") else None

def post_question(img_url, options, answer, level):
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
    response = requests.post(API_POST, json=payload)
    return response.ok

def main():
    try:
        total = int(input("How many questions do you want to generate? "))
        level = input("Enter difficulty level (Too Easy / Easy / Medium / Tough / Too Tough): ").strip()

        for i in range(total):
            print(f"📌 Creating question {i+1}/{total}...")
            month = random.randint(1, 12)
            max_day = calendar.monthrange(YEAR, month)[1]

            x_day, hint_day = choose_days(max_day, level)
            img = draw_calendar(month, YEAR, x_day, hint_day)
            options, answer = get_mcq_options(x_day, max_day)
            image_url = upload_image(img)

            if image_url:
                success = post_question(image_url, options, answer, level)
                print("✅ Posted" if success else "❌ Failed to post")
            else:
                print("❌ Failed to upload image")

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
