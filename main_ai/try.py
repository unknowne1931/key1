import os
import time
from pymongo import MongoClient
from collections import defaultdict


MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)

client = MongoClient(MONGODB_URI)
db = client["test"]
main_qns = db["qno_counts"]
start_stop_db = db["start_stops"]
qns_stored = db["question datas"]




