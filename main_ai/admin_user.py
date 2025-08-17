import time
import pyttsx3
from pymongo import MongoClient
from datetime import datetime
import urllib3

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

user_id = "8926ehddyysjkldassdfsagh"

while True:
    # -------------------------
    # Ensure user pass exists
    # -------------------------
    pass_doc = collection_passes.find_one({"pass": user_id})
    if not pass_doc:
        collection_passes.insert_one({
            "Time": datetime.now(),
            "pass": user_id,
            "email": "lokesh2006k@gmail.com",
            "username": "vishu",
            "valid": "Yes"
        })

    # -------------------------
    # Insert live and total user data
    # -------------------------
    collection_live.insert_one({"Time": datetime.now(), "user": user_id, "valid": "yes"})
    collection_total_users.insert_one({"Time": datetime.now(), "user": user_id})

    # -------------------------
    # Simulate user activity
    # -------------------------
    print("⏳ Waiting 10 seconds...")
    time.sleep(2)
    collection_live.delete_one({"user": user_id})

    # -------------------------
    # Handle wins and coupons
    # -------------------------
    total_won = collection_wons.count_documents({})
    next_no = total_won + 1
    # coupon_doc = collection_coupons.find_one({"no": str(next_no)})
    coupon_doc = collection_coupons.find_one({"no": str(next_no)}, {"_id": 1})

    if not coupon_doc:
        collection_wons.insert_one({
            "Time": datetime.now(),
            "user": user_id,
            "no": str(next_no),
            "ID": "stars"
        })
    else:
        collection_wons.insert_one({
            "Time": datetime.now(),
            "user": user_id,
            "no": str(next_no),
            "ID": coupon_doc['_id']
        })

    print("✅ Process Completed")
    speak(f"Hello! User {user_id}, your data has been updated successfully.")

    # -------------------------
    # Ask user if they want to continue
    # -------------------------
    answer = input("Can I go now? (yes/no): ").strip().lower()
    if answer in ['No', 'n', "N", "no"]:
        print("Exiting loop. Bye!")
        break
    else:
        print("Starting next iteration...\n")
