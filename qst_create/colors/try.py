from PIL import Image, ImageDraw
import random
import requests
import io

# CONFIGURABLE VALUES
num_questions = 3
difficulty = "medium"
seconds = 15

def get_random_rgb():
    return [random.randint(0, 255) for _ in range(3)]

def rgb_string(rgb):
    return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"

def slightly_different(rgb, difficulty):
    diff_range = {
        "easy": 80,
        "medium": 40,
        "tough": 15
    }.get(difficulty.lower(), 40)
    
    return [max(0, min(255, c + random.randint(-diff_range, diff_range))) for c in rgb]

def generate_color_quiz(difficulty):
    total_boxes = 25
    clue_rgb = get_random_rgb()
    clue_color = rgb_string(clue_rgb)

    match_rate = {
        "easy": 0.4,
        "medium": 0.3,
        "tough": 0.2
    }.get(difficulty.lower(), 0.3)

    colors = []
    clue_color_count = 0

    for _ in range(total_boxes - 1):
        is_exact = random.random() < match_rate
        rgb = clue_rgb if is_exact else slightly_different(clue_rgb, difficulty)
        color_str = rgb_string(rgb)
        colors.append(color_str)
        if color_str == clue_color:
            clue_color_count += 1

    colors.insert(0, clue_color)
    clue_color_count += 1

    return colors, clue_color, clue_color_count

def generate_options(correct_answer):
    option_set = {correct_answer}
    include_none = random.random() < 0.4
    total_options = 3 if include_none else 4

    while len(option_set) < total_options:
        wrong = max(0, min(25, correct_answer + random.randint(-2, 2)))
        option_set.add(wrong)

    options = sorted(list(option_set))
    if include_none:
        options.append("None of the above")
    return options

def draw_color_boxes(colors, clue_color):
    width, height = 500, 300
    box_width = 90
    box_height = 60
    padding = 5

    img = Image.new("RGB", (width, height), "#f0f0f0")
    draw = ImageDraw.Draw(img)

    rows = 5
    cols = 5
    for idx, color in enumerate(colors[:25]):
        x = (idx % cols) * (box_width + padding) + 10
        y = (idx // cols) * (box_height + padding) + 10
        rgb = tuple(map(int, color.replace("rgb(", "").replace(")", "").split(",")))
        draw.rectangle([x, y, x + box_width, y + box_height], fill=rgb, outline="black", width=1)

    return img

def upload_image(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    files = {'screenshot': ('color_quiz.png', buffer, 'image/png')}
    response = requests.post("https://backend.stawro.com/stawro/upload.php", files=files)

    if response.ok:
        data = response.json()
        print("✅ Image uploaded:", data["path"])
        return data["filename"]
    else:
        print("❌ Upload failed:", response.status_code)
        return None

def post_question(ans, options, filename, difficulty="Medium", seconds=15):
    url = "http://localhost/api/question"
    body = {
        "question": "How many boxes match the clue color exactly?",
        "answer": str(ans),
        "a": str(options[0]),
        "b": str(options[1]),
        "c": str(options[2]),
        "d": str(options[3]) if len(options) > 3 else "None of the above",
        "language": "English",
        "category": "colors",
        "difficulty": difficulty,
        "type": "Mental Ability",
        "image": f"https://backend.stawro.com/stawro/uploads/{filename}",
        "seconds": seconds
    }

    response = requests.post(url, json=body)
    if response.ok:
        print("✅ Question posted successfully!")
    else:
        print("❌ Failed to post question:", response.status_code, response.text)


# Run for given number of questions
for i in range(num_questions):
    print(f"\n🎨 Creating Question {i+1}/{num_questions}...")

    colors, clue_color, correct_ans = generate_color_quiz(difficulty)
    options = generate_options(correct_ans)

    print(f"Answer: {correct_ans}")
    print("Options:", options)

    image = draw_color_boxes(colors, clue_color)
    filename = upload_image(image)

    if filename:
        post_question(correct_ans, options, filename, difficulty=difficulty.title(), seconds=seconds)
