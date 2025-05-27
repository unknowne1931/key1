import time
import psutil
import subprocess
import pyttsx3
import os
import sys
import requests
from pymongo import MongoClient


# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"> {text}")
    engine.say(text)
    engine.runAndWait()



def is_file_running(filename):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and filename in " ".join(cmdline):  # Join list to string before checking
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


try:
    while True:

        # Check if the script is running
        missing_qno_status = is_file_running("find_missing_qno.py")
        if missing_qno_status:
            print("Missing Qno Finder is running.")
        else:
            print("Missing Qno Finder is not running.")
            speak("Missing Qno Finder is not running.")
            # Start the script if it's not running
            subprocess.Popen(['start', '/MIN', 'cmd', '/k', 'python find_missing_qno.py'], shell=True)
            print("Missing Qno Finder started.")
            speak("Missing Qno Finder started.")
            os.system("cls")


        auto_chng_status = is_file_running("auto_chng.py")
        if auto_chng_status:
            print("Tough Qno Changer is running.")
        else:
            print("Tough Qno Changer is not running.")
            speak("Tough Qno Changer is not running.")
            # Start the script if it's not running
            subprocess.Popen(['start', '/MIN', 'cmd', '/k', 'python auto_chng.py'], shell=True)
            print("Tough Qno Changer started.")
            speak("Tough Qno Changer started.")
            os.system("cls")

        
        qno_types_len = is_file_running("qno_types_len.py")

        if qno_types_len:
            print("Qno Types Length is running.")
        else:
            print("Qno Types Length is not running.")
            speak("Qno Types Length is not running.")
            # Start the script if it's not running
            subprocess.Popen(['start', 'cmd', '/k', 'python show_qno_types_len.py'], shell=True)
            print("Qno Types Length started.")
            speak("Qno Types Length started.")
            os.system("cls")


        # Check if the script is running
        find_duplicate = is_file_running("find_duplicate.py")   
        if find_duplicate:
            print("Find Duplicate is running.")
        else:
            print("Find Duplicate is not running.")
            speak("Find Duplicate is not running.")
            # Start the script if it's not running
            subprocess.Popen(['start', '/MIN', 'cmd', '/k', 'python auto_find_duplicate.py'], shell=True)
            print("Find Duplicate started.")
            speak("Find Duplicate started.")
            os.system("cls")

        check_tough_balen_status = is_file_running('make_blce_group.py')

        if check_tough_balen_status == True:
            print("\033[92mTough Question Balencing working Fine\033[0m")
        else:
            print("Tough Question Balencing may be Turned Off")
            speak("Tough Question Balencing may be Turned Off")
            speak("I gonna Turn it On")
            subprocess.Popen(['start', '/MIN', 'cmd', '/k', 'python make_blce_group.py'], shell=True)
            print("Tough Question Balencing started.")
            speak("Tough Question Balencing started.")
            os.system("cls")


        speak("Everything OK, sir")


        # Check every 5 seconds
        time.sleep(5)
except KeyboardInterrupt:
    print("Program stopped by user.")

