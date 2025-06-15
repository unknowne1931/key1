import tkinter as tk
import random
from PIL import ImageGrab
import requests
import io
import time

# === CONFIG ===
UPLOAD_ENDPOINT = "https://backend.stawro.com/stawro/upload.php"
POST_ENDPOINT = "http://localhost/api/question"

# === HELPERS ===
def get_random_string(length=25):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def count_letters(s):
    return sum(c.isalpha() for c in s)

def count_numbers(s):
    return sum(c.isdigit() for c in s)

def get_seconds_for_difficulty(difficulty):
    return {
        "Too Easy": 15,
        "Easy": 12,
        "Medium": 10,
        "Tough": 8,
        "Too Tough": 6
    }.get(difficulty, 10)

class CharCountAutoUploader:
    def __init__(self, num_questions, difficulty):
        self.num_questions = num_questions
        self.difficulty = difficulty

        # Start hidden root window
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.0)  # Make window invisible
        self.root.geometry('+3000+3000')     # Move it off-screen

        self.label = tk.Label(self.root, bg="#e44507", fg="white",
                              font=("Courier", 16), width=40, height=4, wraplength=400)
        self.label.pack()
        self.root.update_idletasks()

        self.start_loop()

    def start_loop(self):
        for i in range(self.num_questions):
            random_string = get_random_string()
            self.label.config(text=random_string)
            self.root.update_idletasks()
            time.sleep(0.1)  # Ensure it's rendered before capture

            mode = random.choice(["letters", "numbers"])
            correct_answer = count_letters(random_string) if mode == "letters" else count_numbers(random_string)
            question = f"How many {mode} are in the string above?"

            # Create unique options
            options = {correct_answer}
            while len(options) < 4:
                delta = random.randint(-3, 3)
                wrong = correct_answer + delta
                if wrong >= 0:
                    options.add(wrong)
            options = list(options)
            random.shuffle(options)

            try:
                image_url = self.capture_and_upload()
                if image_url:
                    self.upload_question(question, correct_answer, options, image_url)
                    print(f"✅ Uploaded Question {i + 1}")
                else:
                    print(f"❌ Skipped Question {i + 1} (image upload failed)")
            except Exception as e:
                print(f"❌ Error on Question {i + 1}: {e}")

        print(f"\n🎉 All {self.num_questions} questions uploaded.")
        self.root.quit()

    def capture_and_upload(self):
        x = self.label.winfo_rootx()
        y = self.label.winfo_rooty()
        w = x + self.label.winfo_width()
        h = y + self.label.winfo_height()

        img = ImageGrab.grab(bbox=(x, y, w, h)).resize((400, 250))
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        files = {"screenshot": ("screenshot.png", buffer, "image/png")}
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        response.raise_for_status()

        json_data = response.json()
        if json_data.get("status"):
            return f"https://backend.stawro.com/stawro/{json_data['path']}"
        return None

    def upload_question(self, question, answer, options, image_url):
        payload = {
            "question": question,
            "answer": str(answer),
            "a": str(options[0]),
            "b": str(options[1]),
            "c": str(options[2]),
            "d": str(options[3]),
            "language": "English",
            "category": "Character Count",
            "difficulty": self.difficulty,
            "type": "Mental Ability",
            "image": image_url,
            "seconds": get_seconds_for_difficulty(self.difficulty)
        }
        response = requests.post(POST_ENDPOINT, json=payload)
        response.raise_for_status()

# === MAIN ===
if __name__ == "__main__":
    try:
        num = int(input("How many questions to generate? ").strip())
        diff = input("Enter difficulty (Too Easy, Easy, Medium, Tough, Too Tough): ").strip().title()
        if diff not in ["Too Easy", "Easy", "Medium", "Tough", "Too Tough"]:
            print("❗ Invalid difficulty. Defaulting to Medium.")
            diff = "Medium"
        CharCountAutoUploader(num, diff)
    except Exception as e:
        print(f"❌ Failed: {e}")
