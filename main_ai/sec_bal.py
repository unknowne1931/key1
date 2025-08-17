import os
import time
from pymongo import MongoClient
from collections import defaultdict


os.system('cls')


MONGODB_URI = os.getenv(
    "MONGODB_URI",
    # "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
    "mongodb+srv://instasecur24:kick@stawroprototypecluster.0xbx0u5.mongodb.net/?retryWrites=true&w=majority&appName=staWroprototypecluster"
)

client = MongoClient(MONGODB_URI)
db = client["test"]
main_qns = db["qno_counts"]
start_stop_db = db["start_stops"]
qns_stored = db["question datas"]
sec_data = db['seconds_cals']




