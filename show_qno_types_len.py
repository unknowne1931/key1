from pymongo import MongoClient
import time
from colorama import Fore, Style, init
import os
import subprocess

# Initialize colorama
init(autoreset=True)

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)

# Access the database and collection
db = client["test"]
qno_counts_collection = db["qno_counts"]

try:
    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        too_easy = []
        easy = []
        medium = []
        tough = []
        too_tough = []

        documents = list(qno_counts_collection.find())
        qno_len = len(documents)

        for document in documents:
            level = document.get('tough', '').strip()
            qno = document.get('qno')

            if level == "Too Easy":
                too_easy.append(qno)
            elif level == "Easy":
                easy.append(qno)
            elif level == "Medium":
                medium.append(qno)
            elif level == "Tough":
                tough.append(qno)
            elif level == "Too Tough":
                too_tough.append(qno)
            else:
                print(f"{Fore.MAGENTA}Unknown difficulty level for Qno {qno}: '{level}'{Style.RESET_ALL}")

        # Print colored difficulty breakdown
        print("\n--- Difficulty Distribution ---")
        print(f"{Fore.GREEN}Length of Too Easy  : {len(too_easy)}")
        print(f"{Fore.LIGHTGREEN_EX}Length of Easy      : {len(easy)}")
        print(f"{Fore.YELLOW}Length of Medium    : {len(medium)}")
        print(f"{Fore.LIGHTRED_EX}Length of Tough     : {len(tough)}")
        print(f"{Fore.RED}Length of Too Tough : {len(too_tough)}")
        print(f"{Fore.CYAN}Total Questions     : {qno_len}")

        time.sleep(20)

except KeyboardInterrupt:
    print(f"\n{Fore.LIGHTBLUE_EX}Stopped by user.{Style.RESET_ALL}")
