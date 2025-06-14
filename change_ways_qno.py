# import pandas as pd
# from pymongo import MongoClient
# import random

# # Connect to MongoDB
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")

# db1 = client["test"]
# collection1 = db1["question_lists"]
# qno_list_collection = db1["qno_counts"]

# db2 = client["users_mind"]
# collection2 = db2["hist"]




# # Function to fetch questions based on tough
# def fetch_questions():

#     tough_data = ["Too Easy", "Easy", "Medium", "Tough", "Too Tough" , "Too Easy", "Easy", "Medium", "Tough", "Too Tough"]
#     qst_types = ["calender", "clock" , "colors", "img_similar", "int_char", "GK", "GK", "sentence", "number", "sudoku"]

#     random.shuffle(tough_data)
#     random.shuffle(qst_types)

#     questions = []
#     for tough, qtype in zip(tough_data, qst_types):
#         q = qno_list_collection.find_one({"tough": tough, "type": qtype})
#         if q:
#             questions.append(q)


 

#     # Combine all fetched questions
#     all_questions = questions
#     # If not enough questions were found, fill the remaining slots with any available questions
#     total_needed = 10  # 3 tough + 3 easy + 3 medium + 1 tough
#     if len(all_questions) < total_needed:
#         remaining_needed = total_needed - len(all_questions)
#         remaining_qns = list(qno_list_collection.find().limit(remaining_needed))  # Fetch extra questions
#         all_questions.extend(remaining_qns)

#     # Shuffle questions for randomness
#     random.shuffle(all_questions)

#     return all_questions






# get_user = []  # List to store user data

# while True:
#     command = input("Type 'exit' to close the connection, 'get user' to fetch users, or 'remove user' to delete a user: ").strip().lower()
    
#     if command == "exit":
#         print("Closing the connection...")
#         break

#     elif command == "get user":
#         fetched_data = list(collection1.find())  # Convert cursor to a list
#         temp_users = []  # Temporary list to store fetched users

#         for data in fetched_data:
#             user = data.get("user")
#             user_list = data.get("list")

#             if user and not any(entry["user"] == user for entry in get_user):
#                 temp_users.append({"user": user, "list": user_list})

#         get_user.extend(temp_users)  # Add only new users to get_user

#         # Fetch user history from collection2
#         for user_data in get_user:
#             user_history = collection2.find_one({"user": user_data["user"]})

#             if user_history:
#                 print(f"User Data from 'hist': {user_history}")
#             else:
#                 print(f"No data found for user: {user_data['user']}")
#                 print("New user detected.")

#                 # Fetch and print questions
#                 selected_questions = fetch_questions()
#                 print(f"Total Questions Selected: {len(selected_questions)}")
#                 for q in selected_questions:
#                     print(f"{q['qno']} {q['tough']}")  # Prints the fetched question data


                

#     elif command == "remove user":
#         user_to_remove = input("Enter the user to remove: ").strip()

#         # Filter out the user from the list
#         updated_users = [entry for entry in get_user if entry["user"] != user_to_remove]
        
#         if len(updated_users) < len(get_user):
#             print(f"Removed {user_to_remove}")
#         else:
#             print(f"{user_to_remove} not found in the list.")

#         get_user = updated_users  # Update the list

#         print("Updated User List:", get_user)

































import pandas as pd
from pymongo import MongoClient
import random
import os

# Connect to MongoDB
client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")

db1 = client["test"]
collection1 = db1["question datas"]
qno_list_collection = db1["qno_counts"]

os.system('cls')

excepted_qn_in_grp = 10
qn_len = qno_list_collection.count_documents({})
sum_value = qn_len - (excepted_qn_in_grp - 1)

specific_numbers = []
for i in range(sum_value, 0, -excepted_qn_in_grp):
    specific_numbers.append(i)

print(specific_numbers)

for spec_1 in specific_numbers:
    print(f"From : {spec_1}")
    prnt_to = spec_1 + (excepted_qn_in_grp-1)
    qn_for_analysis_grp = []
    while spec_1 <= prnt_to:
        qno_get_data = qno_list_collection.find_one({"qno" : str(spec_1)})
        if qno_get_data['tough'] in ["Tough", "Too Tough"]:
            dat = {
                "qno" : qno_get_data['qno'],
                "tough" : qno_get_data['tough'],
                "ID" : qno_get_data['ID'],
                "cate" : qno_get_data['sub_lang']
            }
            qn_for_analysis_grp.append(dat)
        spec_1 = spec_1 +1
        
    print(f"Tough Len :{len(qn_for_analysis_grp)}")
    if len(qn_for_analysis_grp) > 4:
        print(f"\033[93mRemove {len(qn_for_analysis_grp) - 4} remaining Questions\033[0m")
        
    elif len(qn_for_analysis_grp) < 4:
        print(f"\033[91mAdd {4 - len(qn_for_analysis_grp)}\033[0m")
    else:
        print("\033[92mEverything Ok with this Group\033[0m")
    print("-----------------------------")

# for data in qno_list_collection.find({}):
#     print(data['tough'] + f" : {data['sub_lang']}")









