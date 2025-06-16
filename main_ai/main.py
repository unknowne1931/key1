import os
import time
from pymongo import MongoClient
import subprocess

os.system('cls')

# MongoDB connection
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)


def start_add():
    subprocess.run(["python", "./main_ai/cat/calend.py"] + ["20", "Too Tough"])



client = MongoClient(MONGODB_URI)
db = client["test"]
collection1 = db["qno_counts"]
collection = db["question datas"]


expected_group = 3

tough = ['Too Easy', 'Easy', 'Medium', 'Tough', 'Too Tough']
cat_list = []

data = collection.find({})


for index, dat in enumerate(data):
    print('\033[92m' + '>'*index + " " + '\033[0m')
    if dat['category'] not in cat_list:
        cat_list.append(dat['category'])
    os.system('cls')

    


if len(cat_list) < 10:
    print('Wee need more Questions')
elif len(cat_list) == 10:
    print("Everything ok with Question")
else:
    print("I Found more Questions")
    start_add()

print(len(cat_list))


