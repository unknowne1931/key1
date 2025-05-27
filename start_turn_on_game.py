import time
import os
from pymongo import MongoClient

print("connecting to DB...")

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)

# Select the database and collection
db = client["test"]
start_stop = db["start_stops"]

# Greeting
print("Welcome to StaWro AI!")
print("Can I turn on the Game?")
i = input("yes/no: ").strip().lower()  # Clean input

if i == "yes" or i == "y":
    # Define the filter to find the document to update
    filter_query = {"user": "kick"}  # Customize as needed

    # Define the update operation
    new_values = {"$set": {"Status": "on"}}

    # Perform the update
    result = start_stop.update_one(filter_query, new_values)

    # Confirm result
    if result.modified_count > 0:
        print("Game status set to 'on'. ✅")
    elif result.matched_count > 0:
        print("Status already set to 'on'.")
    else:
        print("No matching document found.")
else:
    print("Okay, exiting...")
    exit()
