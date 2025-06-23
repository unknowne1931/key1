import os
import time
from pymongo import MongoClient
from collections import defaultdict
from bson.objectid import ObjectId

# --- Connect to MongoDB ---
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)

client = MongoClient(MONGODB_URI)
db = client["test"]
collection = db["qno_counts"]
start_stop_db = db["start_stops"]

expected_range = 100

# ✅ System control function
def stop_start(new_status):
    start_stop = start_stop_db.find_one({})
    if not start_stop:
        start_stop_db.insert_one({"Status": new_status})
        print(f"\033[93m⚠️ Created Status Document with value: {new_status}\033[0m")
        return

    current_status = start_stop.get("Status", "on")

    if current_status.lower() != new_status.lower():
        start_stop_db.update_one({"_id": start_stop["_id"]}, {"$set": {"Status": new_status}})
        if new_status != "on":
            print(f"\033[91m⛔ Game stopped. Status changed to: {new_status}\033[0m")
        else:
            print("\033[92m✅ Game is running...\033[0m")
    else:
        print("\033[91m⛔ System is stopped. Please start it to continue.\033[0m")

# === Main loop ===
while True:
    os.system("cls" if os.name == "nt" else "clear")

    docs = list(collection.find().sort("qno", 1))
    existing_qnos = set()
    unexpected_qnos = []

    print(f"\nTotal documents: {len(docs)}\n")

    # ✅ Detect and show duplicate qnos
    qno_docs_map = defaultdict(list)
    for doc in docs:
        qno_str = str(doc.get("qno", "0")).strip()
        qno_docs_map[qno_str].append(doc)

    duplicates = {qno: entries for qno, entries in qno_docs_map.items() if len(entries) > 1}

    if duplicates:
        print("\n\033[91m⚠️ Duplicate QNOs Detected and Will Be Cleaned:\033[0m")
        for qno, entries in duplicates.items():
            print(f"\033[91m - Q{qno} appears {len(entries)} times\033[0m")

            # Keep only one (the first), delete others
            to_delete = entries[1:]  # skip the first entry
            for doc in to_delete:
                collection.delete_one({"_id": ObjectId(doc["_id"])})
            print(f"\033[92m   ✔️ Deleted {len(to_delete)} duplicates of Q{qno}\033[0m")
    else:
        print("\n\033[92m✅ No duplicate QNOs found.\033[0m")




    # Step 1: Analyze in-range questions
    for expected_qno in range(1, expected_range + 1):
        found = False
        for data in docs:
            qno = int(data.get("qno", 0))
            if qno == expected_qno:
                found = True
                existing_qnos.add(qno)
                
                yes_list = data.get("yes", [])
                count = len(yes_list)
                tough = data.get("tough", "Unknown")
                cat = data.get("sub_lang", "Unknown")

                if count > 2:
                    if tough in ['Too Tough', 'Tough']:
                        print(f'\033[91mQ{qno}: Change to TOUGH (Already tough) — Count: {count}\033[0m')
                    elif tough == 'Medium':
                        print(f'\033[93mQ{qno}: Change to MEDIUM — Count: {count}\033[0m')
                    elif count > 5:
                        print(f'\033[94mQ{qno}: Change to EASY — Count: {count}\033[0m')
                    else:
                        print(f'\033[91mQ{qno}: Answered > 2 times — Count: {count}\033[0m')
                else:
                    print(f'\033[92mQ{qno}: ✅ Good — Count: {count}\033[0m')
                break

        if not found:
            stop_start("off")
            print(f'\033[95m⚠️ Missing Question Q{expected_qno} — Not Found in DB\033[0m')

    # Step 2: Find and delete out-of-range questions
    for data in docs:
        qno = int(data.get("qno", 0))
        if qno < 1 or qno > expected_range:
            unexpected_qnos.append(qno)

    if unexpected_qnos:
        stop_start("off")  # Stop system
        print("\n\033[91m⚠️ Deleting Out-of-Range Question Numbers (Not 1–100):\033[0m")
        for uq in sorted(set(unexpected_qnos)):
            print(f"\033[91m - Deleting Q{uq}...\033[0m")
            result = collection.delete_many({"qno": uq})
        print("\033[92m✅ All unexpected questions deleted successfully.\033[0m")
    else:
        print("\n\033[92m✅ All question numbers are within the range 1–100.\033[0m")

    # Wait before next scan
    time.sleep(5)
