import os
import time
from pymongo import MongoClient
from collections import defaultdict
import pyttsx3

# Setup Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"> {text}")
    engine.say(text)
    engine.runAndWait()

# MongoDB URI
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)

# Repeat every 10 seconds
try:
    while True:
        client = MongoClient(MONGODB_URI)
        db = client["test"]
        collection = db["qno_counts"]

        # Group documents by 'qno'
        all_docs = collection.find()
        qno_map = defaultdict(list)

        for doc in all_docs:
            qno = doc.get("qno")
            if qno is not None:
                qno_map[qno].append(doc)

        print("\n🔍 Checking for duplicates...")
        duplicate_found = False

        for qno_value, docs in qno_map.items():
            if len(docs) > 1:
                speak(f"Duplicate found for qno {qno_value}.")
                print(f"qno = {qno_value} → {len(docs)} duplicates")
                duplicate_found = True
                time.sleep(1)

        if not duplicate_found:
            print("✅ No duplicates found.")

        client.close()
        print("🔁 Checking again in 10 seconds...\n")
        time.sleep(20)

except KeyboardInterrupt:
    print("\n⏹️ Stopped by user.")
    speak("Stopped monitoring.")
