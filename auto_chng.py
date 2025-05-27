import os
import time
from pymongo import MongoClient

# MongoDB connection
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)

client = MongoClient(MONGODB_URI)
db = client["test"]
collection1 = db["qno_counts"]
collection = db["Question Data"]

# ANSI escape code for green
GREEN = "\033[92m"
RESET = "\033[0m"

try:
    while True:
        print("⏳ Starting cycle...")
        
        documents = list(collection.find({
            "tough": { "$in": ["Tough", "Too Tough"] }
        }))

        documents1 = collection1.find({
            "tough": { "$in": ["Tough", "Too Tough"] }
        })

        for entry in documents1:
            num = entry.get('qno')
            os.system("cls")
            
            if entry.get('yes') and len(entry['yes']) > 3:
                os.system("cls")
                for doc in documents:
                    questio_value = doc.get("_id")
                    sublang = doc.get("type")

                    if questio_value:

                        match = collection1.find_one({"ID": questio_value, "sub_lang" : sublang})

                        
                        if match:
                            print(f"✅ Exist: {questio_value}")
                        else:
                            print(f"❌ Not Exist: {questio_value} → Updating qno {num}")
                            
                            update_result = collection1.update_one(
                                {"qno": num},
                                {"$set": {
                                    "user": "Auto",
                                    "qno": num,
                                    "img": doc.get("image"),
                                    "Questio": doc.get("question"),
                                    "a": doc.get("a"),
                                    "b": doc.get("b"),
                                    "c": doc.get("c"),
                                    "d": doc.get("d"),
                                    "Ans": doc.get("answer"),
                                    "seconds": doc.get("seconds"),
                                    "lang": doc.get("language"),
                                    "tough": doc.get("difficulty"),
                                    "yes": [""],
                                    "no": [""],
                                    "sub_lang": doc.get("type"),
                                    "ID" : doc.get("_id")
                                }}
                            )
                            print("🛠️ Update Result:", update_result.raw_result)
                            break
            else:
                print(f"{GREEN}200 OK{RESET}")

        time.sleep(2)

except KeyboardInterrupt:
    print("🛑 Script stopped manually.")

finally:
    client.close()
    print("🔌 MongoDB connection closed.")
