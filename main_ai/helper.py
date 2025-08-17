##Everything ok

import os
from pymongo import MongoClient
import subprocess

from PIL import Image, ImageDraw, ImageFont
import calendar
import random
import requests
from io import BytesIO
import sys
import time
import urllib3
import traceback
import math
import io
from bson.objectid import ObjectId
import pyttsx3




# Setup pyttsx3 with female voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
female_voice = None
for voice in voices:
    if "female" in voice.name.lower() or "female" in voice.id.lower():
        female_voice = voice.id
        break
if female_voice:
    engine.setProperty('voice', female_voice)
else:
    # fallback to first voice if female not found
    engine.setProperty('voice', voices[1].id)

# Set slower speech rate (default is usually 200)
engine.setProperty('rate', 170)


def speak(text):
    engine.say(text)
    engine.runAndWait()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


os.system('cls')

# MongoDB connection
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
    # "mongodb+srv://instasecur24:kick@stawroprototypecluster.0xbx0u5.mongodb.net/?retryWrites=true&w=majority&appName=staWroprototypecluster"
        
)




client = MongoClient(MONGODB_URI)
db = client["test"]
collection1 = db["qno_counts"]
collection = db["question datas"]
sec_data = db['seconds_cals']
balance_db = db['balances']
passes_db = db['passes']
wons_db = db['wons']



def balance():
    os.system('cls')
    user = input("User ID : ")
    if user != "":
        print(f"ID : {user}")
    print(f"user : {user}")
    fet_bal = balance_db.find_one({"user" : user})
    if fet_bal:
        speak(f"User has {fet_bal['balance']}, Rupees Only")
        print(f"\033[92m{user} : {fet_bal['balance']}\033[0m")

    else:
        speak("User Not Found")



def balance_add():
    os.system('cls')
    user = input("User ID : ")
    if user != "":
        print(f"ID : {user}")
    print(f"user : {user}")
    fet_bal = balance_db.find_one({"user" : user})
    if fet_bal:
        speak(f"User has {fet_bal['balance']}, Rupees Only")
        print(f"\033[92m{user} : {fet_bal['balance']}\033[0m")
        ad_bal = input("Add Balance [1, 5 ,100] : ")
        # Add 5 to the user's balance
        current_balance = fet_bal.get('balance', 0)
        new_balance = int(current_balance) + int(ad_bal)
        balance_db.update_one({"user": user}, {"$set": {"balance": f"{new_balance}"}})
        speak(f"Added. New balance is {new_balance} Rupees Only")
        print(f"\033[92m{user} : {new_balance}\033[0m")

    else:
        speak("User Not Found")


def user_data():
    os.system('cls')
    user = input("User ID : ")
    if user != "":
        print(f"ID : {user}")
        print(f"user : {user}")
        fet_data = passes_db.find_one({"_id" : ObjectId(user)})
        if fet_data:
            print(f"\033[92mEmail : {fet_data['email']}\033[0m")
            print(f"\033[92mUsername : {fet_data['username']}\033[0m")
            speak(f"Email : {fet_data['email']}")
            speak(f"username : {fet_data['username']}")
    else:
        print("User not found")
        speak("User not Found")


while True:
    user_input = input("Type 'exit' to quit or press Enter to run again : ").strip().lower()
    if user_input == "exit":
        print("Exiting program...")
        break


    try:

        if user_input in ['balance']:
            speak("Fetching user Balance")
            balance()

        elif user_input in ['add', 'add balance', 'refund']:
            balance_add()
        
        elif user_input in ['email', 'user id', 'name']:
            user_data()

        else:
            print("Only these command" \
            "[ 'email', 'user id', 'name' ]" \
            "[ 'balance' ]" \
            "[ 'add', 'add balance', 'refund' ]")



            


    except Exception as e:
        print("Error occurred:", e)
