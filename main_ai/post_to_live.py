import os
import time
from pymongo import MongoClient
from collections import defaultdict


os.system('cls')


MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
    # "mongodb+srv://instasecur24:kick@stawroprototypecluster.0xbx0u5.mongodb.net/?retryWrites=true&w=majority&appName=staWroprototypecluster"
)

client = MongoClient(MONGODB_URI)
db = client["test"]
main_qns = db["qno_counts"]
start_stop_db = db["start_stops"]
qns_stored = db["question datas"]


expected_qno = 300

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

stop_start('off')

main_qns.delete_many({})

data_qns = qns_stored.find({})
for i, dat in enumerate(data_qns,1):
    print(f"Qno : {i} ----> {dat['difficulty']}")
    ans = ""
    if dat['answer'] == dat['a']:
        ans = 'a'
    elif dat['answer'] == dat['b']:
        ans = 'b'
    elif dat['answer'] == dat['c']:
        ans = 'c'
    else:
        ans = 'd'

    main_qns.insert_one({
        "Time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ID" : dat['_id'],
        "user" : "staWro",
        "img" : dat['image'],
        "Questio" : dat['question'],
        "qno" : str(i),
        "a" : dat['a'],
        "b" : dat['b'],
        "c" : dat['c'],
        "d" : dat['d'],
        "Ans" : dat['answer'],
        # "Ans" : ans,
        "lang" : dat['language'],
        "tough" : dat['difficulty'],
        "seconds" :dat['seconds'],
        "sub_lang" : dat['category'],
        "yes" : [''],
        "no" : ['']
    })

    print(f"\033[92mQno {i} Posted ok\033[0m")


stop_start('on')


