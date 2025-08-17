import time
import pyttsx3
from pymongo import MongoClient
from datetime import datetime
import urllib3
import os
import sys


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------
# Text-to-Speech Setup
# -------------------------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
female_voice = next((v.id for v in voices if "female" in v.name.lower() or "female" in v.id.lower()), None)
if female_voice:
    engine.setProperty('voice', female_voice)
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -------------------------
# MongoDB Setup
# -------------------------


MONGODB_URI = "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
  # Replace with your MongoDB URI
client = MongoClient(MONGODB_URI)
db = client["test"]

collection_passes = db['passes']
collection_live = db['start_valids']
collection_total_users = db['total_users']
collection_wons = db['wons']
collection_coupons = db['cupon_s']


# exclude_users = ["8926ehddyysjkldasd892hs", "8926ehddyysjkldassdfsagh"]

# Find all documents where 'user' is NOT in exclude_users
total_users_played_count = collection_total_users.count_documents({})
winners_count = collection_wons.count_documents({})


winning_percentage = (winners_count / total_users_played_count) *100

print(winning_percentage)


if winning_percentage < 10:
    print("ok")
else 








