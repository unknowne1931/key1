import os
from pymongo import MongoClient



MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)





client = MongoClient(MONGODB_URI)
db = client["test"]
collection = db["qno_counts"]
collection1 = db["question datas"]


len = collection.count_documents({})
print(len)


