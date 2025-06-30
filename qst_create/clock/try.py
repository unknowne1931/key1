##everything ok
from PIL import Image, ImageDraw
import random
import math
import requests
import io

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
        num_questions = int(input("📌 How many clock questions do you want to generate? "))
        difficulty = input("📌 Enter difficulty level (Too Easy / Easy / Medium / Tough / Too Tough): ").strip()
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
