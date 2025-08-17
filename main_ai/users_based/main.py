# import os
# import time
# from pymongo import MongoClient
# from collections import defaultdict


# os.system('cls')


# MONGODB_URI = os.getenv(
#     "MONGODB_URI",
#     "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
# )

# client = MongoClient(MONGODB_URI)
# db = client["test"]
# main_qns = db["qno_counts"]
# start_stop_db = db["start_stops"]
# qns_stored = db["question datas"]
# total_users_pl = db['total_users']




# # new collection
# users_bal = db['balances']
# live_users = db['start_valids']
# entry_fees = db['rupees']
# won_data = db['wons']

# data = live_users.find({})

# get_usr_id = []
# # print(f"total number of users : {len(data)}")
# for i, dat in enumerate(data, 1):
#     # print(f"{i} : {dat}")
#     if dat['user'] not in get_usr_id:
#         get_usr_id.append(dat['user'])
#         get_user_bal = users_bal.find_one({"user" : dat['user']})
#         get_entry_bal = entry_fees.find_one({"username" : "admin"})
#         attepts_left = int(get_user_bal['balance']) / int(get_entry_bal['rupee'])
#         print(int(attepts_left))
#         print(get_user_bal['balance'])
#         if attepts_left <= 1 :
#             total_played_data = list(total_users_pl.find({"user" : dat['user']}))
#             won_user_data = list(won_data.find({"user" : dat['user']}))
#             total_won_data = (len(won_user_data) / len(total_played_data)) * 100 if len(total_played_data) > 0 else 0
#             if total_won_data <= 0:
#                 print(f"Make this user win : {dat['user']}")
#             elif total_won_data <= 10:
#                 print(f"Make chck his Luck {dat['user']}")
#             elif total_won_data <= 20:
#                 print(f"Make himm loose the game {dat['user']} ")
#             elif total_won_data >= 90:
#                 print(f"Make his Loose the game {dat['user']} ")
#             else:
#                 print(f"Default {dat['user']} ")

            
#         else:
#             print(f"Let them check there luck : {dat['user']} ")
        
#         get_usr_id.append(dat['user'])

    
#     else:
#         print(f"Checked, OK : {dat["_id"]}")







import os
import time
from pymongo import MongoClient
from collections import defaultdict

# Set this only once
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)

client = MongoClient(MONGODB_URI)
db = client["test"]

main_qns = db["qno_counts"]
start_stop_db = db["start_stops"]
qns_stored = db["question datas"]
total_users_pl = db['total_users']

# new collections
users_bal = db['balances']
live_users = db['start_valids']
entry_fees = db['rupees']
won_data = db['wons']

get_usr_id = []

while True:
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal screen

    data = live_users.find({})
    

    for i, dat in enumerate(data, 1):
        if dat['_id'] not in get_usr_id:
            get_usr_id.append(dat['_id'])

            get_user_bal = users_bal.find_one({"user": dat['user']})
            get_entry_bal = entry_fees.find_one({"username": "admin"})
            if not get_user_bal or not get_entry_bal:
                print(f"Missing balance or entry fee data for user: {dat['user']}")
                continue

            try:
                attepts_left = int(get_user_bal['balance']) / int(get_entry_bal['rupee'])
                print(f"User: {dat['user']}, Attempts left: {int(attepts_left)}, Balance: {get_user_bal['balance']}")

                if attepts_left <= 1:
                    total_played_data = list(total_users_pl.find({"user": dat['user']}))
                    won_user_data = list(won_data.find({"user": dat['user']}))
                    total_won_data = (len(won_user_data) / len(total_played_data)) * 100 if total_played_data else 0

                    ##make continue here

                    if total_won_data <= 0:
                        print(f"\033[92mMake this user win : {dat['user']}\033[0m")
                    elif total_won_data >= 80:
                        print(f"Make him lose the game {dat['user']}")
                    else:
                        print(f"\033[93mMake let him play good {dat['user']}\033[0m")
                else:
                    ##make continue here
                    print(f"Let them check their luck : {dat['user']}")
            except Exception as e:
                print(f"Error processing user {dat['user']}: {str(e)}")
        else:
            print(f"\033[93mChecked already, OK : {dat['_id']}\033[0m")

    print("\nWaiting for 5 seconds...\n")
    time.sleep(2)
