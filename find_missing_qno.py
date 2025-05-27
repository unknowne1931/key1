# import os
# from pymongo import MongoClient
# import pyttsx3
# import subprocess


# # Initialize the text-to-speech engine
# engine = pyttsx3.init()
# engine.setProperty('rate', 150)
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()


# # MongoDB connection
# MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# client = MongoClient(MONGODB_URI)

# # Select DB and collection
# db = client["test"]
# collection1 = db["qno_counts"]

# # Get total document count
# total_docs = collection1.count_documents({})
# print(f"📊 Total documents in collection1: {total_docs}")

# Missing = []
# exist = []

# for num in range (1,total_docs):
#     data = collection1.find_one({"qno" : f"{num}"})
#     if data['qno'] == f"{num}":
#         exist.append(num)

#     else:
#         print(f"{num} Missing Question Number {num}")
#         Missing.append(num)

# if total_docs-1 == len(exist):
#     speak("Sir, I found all Question List.")
#     speak("Everything OK sir")
# else:
#     speak("Sir, Some Question are Missed or, The length of Total Question Numbers from Data Base, won't Mactched")
#     speak("May be You can find them in Missing List, Let them Check Before Start Game")
#     speak("I gonna stop Game sir, to Setup all Again")
#     subprocess.run(["python", "stop_turn_off.py"], shell=True)

# for data in Missing:
#     speak(f"Question Number {data}")

# if len(data) < 0:
#     speak("No Missing Question Numbers Found Sir")

# # Close connection
# client.close()




# import os
# from pymongo import MongoClient
# import pyttsx3
# import subprocess

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()
# engine.setProperty('rate', 150)
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)

# def speak(text):
#     print(f"🔊 {text}")
#     engine.say(text)
#     engine.runAndWait()

# # MongoDB connection
# MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# client = MongoClient(MONGODB_URI)

# # Select DB and collection
# db = client["test"]
# collection1 = db["qno_counts"]

# # Get total document count
# total_docs = collection1.count_documents({})
# print(f"📊 Total documents in collection1: {total_docs}")

# Missing = []
# exist = []

# for num in range(1, total_docs + 1):
#     data = collection1.find_one({"qno": str(num)})
#     if data and data.get("qno") == str(num):
#         exist.append(num)
#     else:
#         print(f"❌ Missing Question Number: {num}")
#         Missing.append(num)

# if total_docs == len(exist):
#     speak("Sir, I found all question list.")
#     speak("Everything is OK, sir.")
# else:
#     speak("Sir, some questions are missing or the total count does not match.")
#     speak("Please check the missing list before starting the game.")
#     speak("I will now stop the game for setup.")
#     subprocess.run(["python", "stop_turn_off.py"], shell=True)

#     for missing_qno in Missing:
#         speak(f"Missing Question Number: {missing_qno}")

# if len(Missing) == 0:
#     speak("No missing question numbers found, sir.")

# # Close MongoDB connection
# client.close()


















import os
import time
from pymongo import MongoClient
import pyttsx3
import subprocess

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
client = MongoClient(MONGODB_URI)

# Select DB and collection
db = client["test"]
collection1 = db["qno_counts"]

while True:
    print("\n🔁 Checking for missing questions...")

    total_docs = collection1.count_documents({})
    print(f"📊 Total documents in collection1: {total_docs}")

    Missing = []
    exist = []

    for num in range(1, total_docs + 1):
        data = collection1.find_one({"qno": str(num)})
        if data and data.get("qno") == str(num):
            exist.append(num)
        else:
            print(f"❌ Missing Question Number: {num}")
            Missing.append(num)

    if total_docs == len(exist):
        speak("Sir, I found all question list.")
        speak("Everything is OK, sir.")
    else:
        speak("Sir, some questions are missing or the total count does not match.")
        speak("Please check the missing list before starting the game.")
        speak("I will now stop the game for setup.")
        subprocess.run(["python", "stop_turn_off.py"], shell=True)

        for missing_qno in Missing:
            speak(f"Missing Question Number: {missing_qno}")

    if len(Missing) == 0:
        speak("No missing question numbers found, sir.")

    # Wait 5 seconds before running again
    time.sleep(5)

# Close connection (will not be reached unless interrupted)
client.close()
