import random
import requests
from PIL import Image, ImageDraw
import io

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

# === FUNCTIONS ===

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

    # Word wrap logic
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
    else:
        print("❌ Failed to post question:", response.text)

def run_letter_quiz():
    num_questions = int(input("How many questions do you want to post? "))
    user_input = input("Enter difficulty (Too Easy, Easy, Medium, Tough, Too Tough): ").strip().title()

    # Normalize and default fallback
    difficulty = "Medium"
    for key in difficulty_map:
        if key.lower() in user_input.lower():
            difficulty = key
            break

    diff_data = difficulty_map[difficulty]
    min_len, max_len = diff_data["length_range"]
    seconds = str(diff_data["seconds"])

    for i in range(num_questions):
        print(f"\n🔢 Generating question {i + 1}/{num_questions}...")

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

        post_question(question_data)

# === MAIN ===
if __name__ == "__main__":
    run_letter_quiz()
