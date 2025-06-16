import random
import time
import os

DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_directions(sequence):
    print("🧭 Memorize this direction sequence:")
    for direction in sequence:
        print("👉", direction)
        time.sleep(1)
        clear_screen()

def play_game():
    print("🎮 Welcome to the Direction Memory Game!")
    level = 1

    while True:
        print(f"\n🌟 Level {level}")
        sequence = [random.choice(DIRECTIONS) for _ in range(level)]
        show_directions(sequence)

        print("✏️ Enter the directions one by one:")
        correct = True
        for i, expected in enumerate(sequence):
            user_input = input(f"Step {i+1}: ").strip().upper()
            if user_input != expected:
                correct = False
                break

        if correct:
            print("✅ Correct! Next level coming...")
            level += 1
            time.sleep(1)
            clear_screen()
        else:
            print(f"❌ Wrong! The correct direction was '{expected}'.")
            print(f"🎯 Your final score: Level {level - 1}")
            break

if __name__ == "__main__":
    play_game()
