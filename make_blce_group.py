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
#                             replacement.pop('_id', None)  # ✅ Remove _id
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
#                             replacement.pop('_id', None)  # ✅ Remove _id
#                             qno_counts_collection.update_one(
#                                 {"qno": to_replace["qno"], "lang": "English"},
#                                 {"$set": replacement | {"yes": [""], "no": [""]}}
#                             )
#                 print("\033[92m✅ Group fixed to have exactly 2 Tough/Too Tough questions.\033[0m")
#             print("----------------------------------------------------------")

#         time.sleep(10)

#     except Exception as e:
#         print(f"\033[91m[ERROR] {e}\033[0m")
#         time.sleep(5)





































from pymongo import MongoClient
import os
import time

# MongoDB connection
client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
db = client["test"]
qno_counts_collection = db["qno_counts"]
qno_list_collection = db["question datas"]


os.system('cls' if os.name == 'nt' else 'clear')

cat =[]


for doc in qno_list_collection.find({"language": "English"}):
    if doc['category'] not in cat:
        cat.append(doc['category'])
print("Categories found:", cat)


cat_len = []

for category in cat:
    data_len = qno_list_collection.count_documents({"category": category, "language": "English"})
    cat_len.append({"len" : data_len, "cat" : category})
print("Category lengths:", cat_len)

for catlen in cat_len:
      if catlen["len"] != cat_len[0]["len"]:
        print(f"Category '{catlen['cat']}' has length {catlen['len']} (not equal to {cat_len[0]['len']})")

