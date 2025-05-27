# # from pymongo import MongoClient
# # import os

# # # Clear the terminal screen
# # os.system('cls' if os.name == 'nt' else 'clear')

# # # MongoDB connection
# # client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# # db = client["test"]
# # qno_counts_collection = db["qno_counts"]
# # qno_list_collection = db["questions_users"]

# # # Get all English questions
# # english_questions = list(qno_counts_collection.find({"lang": "English"}))
# # qno_len = len(english_questions)

# # # Group qnos by difficulty
# # difficulty_groups = {
# #     "Too Easy": [],
# #     "Easy": [],
# #     "Medium": [],
# #     "Tough": [],
# #     "Too Tough": []
# # }

# # for doc in english_questions:
# #     difficulty = doc.get("tough")
# #     qno = doc.get("qno")
# #     if difficulty in difficulty_groups:
# #         difficulty_groups[difficulty].append(qno)

# # # Create groups of 10
# # group_qnos = []
# # for i in range(qno_len - 9, 0, -10):
# #     group = list(range(i, i + 10))
# #     group_qnos.append(group)

# # # Helper to get a replacement question
# # def get_replacement(target_difficulties, used_qnos):
# #     query = {
# #         "tough": {"$in": target_difficulties},
# #         "lang": "English"
# #     }

# #     for doc in qno_list_collection.find(query):
# #         if qno_counts_collection.find_one({"Questio": doc['Questio'], "lang": "English"}):
# #             continue  # Already exists
# #         return doc  # Valid replacement

# #     return None

# # # Process each group
# # for group in group_qnos:
# #     questions = []
# #     for qno in group:
# #         qno_str = str(qno)
# #         doc = qno_counts_collection.find_one({"qno": qno_str, "lang": "English"})
# #         if doc:
# #             questions.append({"qno": qno_str, "tough": doc['tough']})

# #     # Count current tough or too tough
# #     tough_qs = [q for q in questions if q["tough"] in ["Tough", "Too Tough"]]
# #     easy_qs = [q for q in questions if q["tough"] in ["Too Easy", "Easy", "Medium"]]

# #     if len(tough_qs) == 2:
# #         print(f"✅ Group OK with 2 tough: {[q['qno'] for q in tough_qs]}")
# #     else:
# #         # Need to fix the group
# #         print(f"🔧 Fixing group: {group}")
# #         # Remove excess tough
# #         if len(tough_qs) > 2:
# #             for extra in tough_qs[2:]:
# #                 replacement = get_replacement(["Too Easy", "Easy", "Medium"], group)
# #                 if replacement:
# #                     qno_counts_collection.update_one(
# #                         {"qno": extra["qno"], "lang": "English"},
# #                         {"$set": {
# #                             "tough": replacement['tough'],
# #                             "Questio": replacement['Questio'],
# #                             "user": replacement['user'],
# #                             "img": replacement['img'],
# #                             "a": replacement['a'],
# #                             "b": replacement['b'],
# #                             "c": replacement['c'],
# #                             "d": replacement['d'],
# #                             "Ans": replacement['Ans'],
# #                             "seconds": replacement['seconds'],
# #                             "yes": [""],
# #                             "no": [""]
# #                         }}
# #                     )
# #         # Add missing tough
# #         elif len(tough_qs) < 2:
# #             needed = 2 - len(tough_qs)
# #             for _ in range(needed):
# #                 replacement = get_replacement(["Tough", "Too Tough"], group)
# #                 if replacement and easy_qs:
# #                     to_replace = easy_qs.pop(0)
# #                     qno_counts_collection.update_one(
# #                         {"qno": to_replace["qno"], "lang": "English"},
# #                         {"$set": {
# #                             "tough": replacement['tough'],
# #                             "Questio": replacement['Questio'],
# #                             "user": replacement['user'],
# #                             "img": replacement['img'],
# #                             "a": replacement['a'],
# #                             "b": replacement['b'],
# #                             "c": replacement['c'],
# #                             "d": replacement['d'],
# #                             "Ans": replacement['Ans'],
# #                             "seconds": replacement['seconds'],
# #                             "yes": [""],
# #                             "no": [""]
# #                         }}
# #                     )

# #         print("✅ Group fixed to have exactly 2 Tough/Too Tough questions.")
# #     print("----------------------------------------------------------")















# from pymongo import MongoClient
# import os
# import time

# # MongoDB connection
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# db = client["test"]
# qno_counts_collection = db["qno_counts"]
# qno_list_collection = db["questions_users"]

# # Helper to get a replacement question
# def get_replacement(target_difficulties, used_qnos):
#     query = {
#         "tough": {"$in": target_difficulties},
#         "lang": "English"
#     }

#     for doc in qno_list_collection.find(query):
#         if qno_counts_collection.find_one({"Questio": doc['Questio'], "lang": "English"}):
#             continue  # Already exists
#         return doc  # Valid replacement

#     return None

# while True:
#     try:
#         os.system('cls' if os.name == 'nt' else 'clear')
#         print("\033[96m[INFO] Running Tough Question Balancing...\033[0m")

#         # Get all English questions
#         english_questions = list(qno_counts_collection.find({"lang": "English"}))
#         qno_len = len(english_questions)

#         # Group qnos by difficulty
#         difficulty_groups = {
#             "Too Easy": [],
#             "Easy": [],
#             "Medium": [],
#             "Tough": [],
#             "Too Tough": []
#         }

#         for doc in english_questions:
#             difficulty = doc.get("tough")
#             qno = doc.get("qno")
#             if difficulty in difficulty_groups:
#                 difficulty_groups[difficulty].append(qno)

#         # Create groups of 10
#         group_qnos = []
#         for i in range(qno_len - 9, 0, -10):
#             group = list(range(i, i + 10))
#             group_qnos.append(group)

#         # Process each group
#         for group in group_qnos:
#             questions = []
#             for qno in group:
#                 qno_str = str(qno)
#                 doc = qno_counts_collection.find_one({"qno": qno_str, "lang": "English"})
#                 if doc:
#                     questions.append({"qno": qno_str, "tough": doc['tough']})

#             tough_qs = [q for q in questions if q["tough"] in ["Tough", "Too Tough"]]
#             easy_qs = [q for q in questions if q["tough"] in ["Too Easy", "Easy", "Medium"]]

#             if len(tough_qs) == 2:
#                 print(f"\033[92m✅ Group OK with 2 tough: {[q['qno'] for q in tough_qs]}\033[0m")
#             else:
#                 print(f"\033[93m🔧 Fixing group: {group}\033[0m")
#                 if len(tough_qs) > 2:
#                     for extra in tough_qs[2:]:
#                         replacement = get_replacement(["Too Easy", "Easy", "Medium"], group)
#                         if replacement:
#                             qno_counts_collection.update_one(
#                                 {"qno": extra["qno"], "lang": "English"},
#                                 {"$set": replacement | {"yes": [""], "no": [""]}}
#                             )
#                 elif len(tough_qs) < 2:
#                     needed = 2 - len(tough_qs)
#                     for _ in range(needed):
#                         replacement = get_replacement(["Tough", "Too Tough"], group)
#                         if replacement and easy_qs:
#                             to_replace = easy_qs.pop(0)
#                             qno_counts_collection.update_one(
#                                 {"qno": to_replace["qno"], "lang": "English"},
#                                 {"$set": replacement | {"yes": [""], "no": [""]}}
#                             )
#                 print("\033[92m✅ Group fixed to have exactly 2 Tough/Too Tough questions.\033[0m")
#             print("----------------------------------------------------------")

#         print("\033[94m[INFO] Waiting 10 seconds before next run...\033[0m")
#         time.sleep(20)

#     except KeyboardInterrupt:
#         print("\n\033[91m[STOPPED] Program manually stopped.\033[0m")
#         break




























from pymongo import MongoClient
import os
import time

# MongoDB connection
client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
db = client["test"]
qno_counts_collection = db["qno_counts"]
qno_list_collection = db["questions_users"]

# Helper to get a replacement question
def get_replacement(target_difficulties, used_qnos):
    query = {
        "tough": {"$in": target_difficulties},
        "lang": "English"
    }

    for doc in qno_list_collection.find(query):
        if qno_counts_collection.find_one({"Questio": doc['Questio'], "lang": "English"}):
            continue  # Already exists
        return doc  # Valid replacement

    return None

while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[96m[INFO] Running Tough Question Balancing...\033[0m")

        # Get all English questions
        english_questions = list(qno_counts_collection.find({"lang": "English"}))
        qno_len = len(english_questions)

        # Group qnos by difficulty
        difficulty_groups = {
            "Too Easy": [],
            "Easy": [],
            "Medium": [],
            "Tough": [],
            "Too Tough": []
        }

        for doc in english_questions:
            difficulty = doc.get("tough")
            qno = doc.get("qno")
            if difficulty in difficulty_groups:
                difficulty_groups[difficulty].append(qno)

        # Create groups of 10
        group_qnos = []
        for i in range(qno_len - 9, 0, -10):
            group = list(range(i, i + 10))
            group_qnos.append(group)

        # Process each group
        for group in group_qnos:
            questions = []
            for qno in group:
                qno_str = str(qno)
                doc = qno_counts_collection.find_one({"qno": qno_str, "lang": "English"})
                if doc:
                    questions.append({"qno": qno_str, "tough": doc['tough']})

            tough_qs = [q for q in questions if q["tough"] in ["Tough", "Too Tough"]]
            easy_qs = [q for q in questions if q["tough"] in ["Too Easy", "Easy", "Medium"]]

            if len(tough_qs) == 2:
                print(f"\033[92m✅ Group OK with 2 tough: {[q['qno'] for q in tough_qs]}\033[0m")
            else:
                print(f"\033[93m🔧 Fixing group: {group}\033[0m")
                if len(tough_qs) > 2:
                    for extra in tough_qs[2:]:
                        replacement = get_replacement(["Too Easy", "Easy", "Medium"], group)
                        if replacement:
                            replacement.pop('_id', None)  # ✅ Remove _id
                            qno_counts_collection.update_one(
                                {"qno": extra["qno"], "lang": "English"},
                                {"$set": replacement | {"yes": [""], "no": [""]}}
                            )
                elif len(tough_qs) < 2:
                    needed = 2 - len(tough_qs)
                    for _ in range(needed):
                        replacement = get_replacement(["Tough", "Too Tough"], group)
                        if replacement and easy_qs:
                            to_replace = easy_qs.pop(0)
                            replacement.pop('_id', None)  # ✅ Remove _id
                            qno_counts_collection.update_one(
                                {"qno": to_replace["qno"], "lang": "English"},
                                {"$set": replacement | {"yes": [""], "no": [""]}}
                            )
                print("\033[92m✅ Group fixed to have exactly 2 Tough/Too Tough questions.\033[0m")
            print("----------------------------------------------------------")

        time.sleep(10)

    except Exception as e:
        print(f"\033[91m[ERROR] {e}\033[0m")
        time.sleep(5)
