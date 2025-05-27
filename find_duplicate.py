import os
import time
from pymongo import MongoClient
from collections import defaultdict
import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"> {text}")
    engine.say(text)
    engine.runAndWait()


# Connect to MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
client = MongoClient(MONGODB_URI)

# Select your database and collection
db = client["test"]
collection = db["qno_counts"]

# Optional delay
time.sleep(1)

# Step 1: Group documents by the "qno" field
all_docs = collection.find({"lang": "English"})
qno_map = defaultdict(list)

for doc in all_docs:
    qno = doc.get("qno")
    if qno is not None:
        qno_map[qno].append(doc)

# Step 2: Show qno values that have duplicates
print("🔍 Duplicate qno values:")
duplicate_found = False

for qno_value, docs in qno_map.items():
    if len(docs) > 1:
        speak(f"Duplicate found for qno {qno_value}.")
        print(f"qno = {qno_value} → {len(docs)} duplicates")
        duplicate_found = True
        time.sleep(5)

if not duplicate_found:
    speak("No duplicates found.")
    print("✅ No duplicates found.")
    

# Close the connection
client.close()
