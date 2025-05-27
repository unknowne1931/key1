import pyttsx3
from pymongo import MongoClient
import subprocess
import os
import time
import psutil


# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)



def speak(text):
    print(f"> {text}")
    engine.say(text)
    engine.runAndWait()

def start_new_task(path):
    subprocess.Popen(['start', '/MIN', 'cmd', '/k', f'python {path}'], shell=True)


import psutil

def is_file_running(filename):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and filename in " ".join(cmdline):  # Join list to string before checking
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False




speak("hello sir, I am Anu, I am your project Assistant, the Project , staWro")
speak("i am your assistent, and co-pilot to lead your project")
speak(" i can controle all Automatic")



db = client["test"]
wons_table = db["wons"]
total_plyed = db["total_users"]
start_stop = db["start_stops"]

# First-time status check
start_status = start_stop.find_one({"user": "kick"})
if start_status["Status"] != "on":
    speak("Game is turned off")
    speak("Can I turn on the game to continue?")
    subprocess.run(["python", "start_turn_on_game.py"], shell=True)

# Command memory list
cmd = []

# Loop until Ctrl+C is pressed
try:
    while True:
        os.system("cls")  # Clears terminal (only works on Windows)



        # Fetch data
        wons_length = wons_table.count_documents({})
        total_plyed_length = total_plyed.count_documents({})

        if total_plyed_length == 0:
            speak("No data found to calculate win percentage.")
            time.sleep(3)
            continue

        wons_length_per = (wons_length / total_plyed_length) * 100
        print(f"Win %: {wons_length_per:.2f}")

        check_status_status = is_file_running('sub_main.py')

        

        if check_status_status == True:
            print("The main game Engine is running. OK")
        else:
            speak("The main game engine is not running. I will start it.")
            start_new_task('sub_main.py')
        
        



        # Decision logic
        if wons_length_per <= 0:
            if "ck_qn" not in cmd:
                speak("Winning is zero, I will check all existing questions.")
                subprocess.run(["python", "find_duplicate.py"], shell=True)
                cmd.append("ck_qn")
            elif "ck_missing_qno" not in cmd:
                speak("I gonna check for missing question numbers.")
                subprocess.run(["python", "find_missing_qno.py"], shell=True)
                cmd.append("ck_missing_qno")
            elif "start_tough_balencer" not in cmd:
                speak("Checking the, Tough Question Changer AI Status")
                t_status = is_file_running("auto_chng.py")
                if t_status == True :
                    speak("The Tough Question Changer AI is Active")
                    cmd.append("start_tough_balencer")
                else:
                    speak("I Gonna Start Tough Question Changer AI")
                    start_new_task('auto_chng.py')
            else:
                print("Everything Checks Fine")

        elif wons_length_per <= 25:
            speak("Winning percentage is lesser than or equal to 25%")
            speak("Game is balanced.")
        elif wons_length_per <= 50:
            speak("Winning percentage is greater than 25%")
            speak("Game going out of balancing mode. Turning off the game.")
            subprocess.run(["python", "stop_turn_off.py"], shell=True)
            cmd.clear()
        elif wons_length_per <= 75:
            speak("Winning percentage is greater than 50%")
            speak("Game going out of control. Turning off the game.")
            subprocess.run(["python", "stop_turn_off.py"], shell=True)
            cmd.clear()
        elif wons_length_per <= 90:
            speak("Winning percentage is greater than 75%")
            speak("Game getting dangerous. Turning off the game.")
            subprocess.run(["python", "stop_turn_off.py"], shell=True)
            cmd.clear()
        elif wons_length_per <= 100:
            speak("Winning percentage is greater than 90%")
            speak("Game too dangerous. Turning off the game.")
            subprocess.run(["python", "stop_turn_off.py"], shell=True)
            cmd.clear()
        else:
            speak("Winning percentage is greater than 100%")
            speak("Game out of control. Shutting down.")
            subprocess.run(["python", "stop_turn_off.py"], shell=True)
            cmd.clear()

        # Wait a bit before next loop
        time.sleep(5)

except KeyboardInterrupt:
    speak("Game monitor stopped manually.")
