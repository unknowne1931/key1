from pymongo import MongoClient
import os
import time


os.system('cls')

# MongoDB connection
client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
db = client["test"]
qno_counts_collection = db["qno_counts"]
qno_list_collection = db["question datas"]

# Convert cursor to list
data = list(qno_list_collection.find())

# Compute group count logic
expected_category_count = 10
data_len = len(data) - expected_category_count

total_questions = len(data)  # or any integer value

sum_value = total_questions - 9
grp_ary = []
tough_lst = []
cate_lst = []

for dat in data:
    if dat['difficulty'] in tough_lst:
        continue
    else:
        tough_lst.append(dat['difficulty'])


for dat in data:
    if dat['category'] in cate_lst:
        continue
    else:
        cate_lst.append(dat['category'])



specific_numbers = []
for i in range(sum_value, 0, -10):
    specific_numbers.append(i)
    grp_ary.append([])


print(specific_numbers)
print(grp_ary)
print(tough_lst)
print(cate_lst)


for dat in grp_ary:
    while len(dat) < expected_category_count:
        for tg in tough_lst:
            data = qno_list_collection.find({"difficulty" : tg})
            count_easy = sum(1 for item in data if item['difficulty'] == tg)
            if count_easy <= 2 and data['_id'] not in dat["difficulty"]:
                
                
 
            # if tg not in dat['difficulty'] and 


print(grp_ary)















# import os
# from pymongo import MongoClient
# import time

# # MongoDB connection
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# db = client["test"]
# qno_counts_collection = db["qno_counts"]
# qno_list_collection = db["question datas"]

# # Clear console (only works on Windows)
# os.system('cls' if os.name == 'nt' else 'clear')

# # Fetch data
# data = list(qno_list_collection.find({}))
# print(f"\033[93mTotal questions fetched: {len(data)}\033[0m\n")

# # Get unique categories and difficulties safely
# categories = sorted(set(d.get('category', 'Unknown') for d in data))
# difficulties = sorted(set(d.get('difficulty', 'Unknown') for d in data))

# print("Categories:", categories)
# print("Difficulties:", difficulties)
# print()

# # Group questions by (category, difficulty)
# grouped = {}
# for dat in data:
#     cat = dat.get('category', 'Unknown')
#     dif = dat.get('difficulty', 'Unknown')
#     key = (cat, dif)
#     grouped.setdefault(key, []).append(dat)

# # Compute how many groups we can form (based on 10 questions per group)
# expected_category_count = 10
# data_len = len(data) - expected_category_count
# i = data_len
# specific_num = []
# while i > 0:
#     specific_num.append(i)
#     i -= expected_category_count
# need_qn_ln = len(specific_num) * 2

# print(f"\033[92m{len(specific_num)} Groups Possible\033[0m")

# # Summary of available questions per category/difficulty
# print("\n\033[1mSummary of all categories and difficulties:\033[0m\n")
# for cat in categories:
#     for dif in difficulties:
#         key = (cat, dif)
#         count = len(grouped.get(key, []))
#         enough = count >= len(specific_num)
#         status = "✅ Enough" if enough else "❌ Not enough"
#         color = "\033[92m" if enough else "\033[91m"
#         print(f"{color}Category: {cat:10} | Difficulty: {dif:9} | Count: {count:2} | {status}\033[0m")
# print()

# # Build groups
# groups = []
# for group_idx in range(len(specific_num)):
#     group = []
#     for cat in categories:
#         for dif in difficulties:
#             key = (cat, dif)
#             if len(grouped.get(key, [])) > group_idx:
#                 group.append(grouped[key][group_idx])
#             if len(group) == 10:
#                 break
#         if len(group) == 10:
#             break
#     if len(group) == 10:
#         groups.append(group)

# # Display all groups
# for idx, group in enumerate(groups, 1):
#     print(f"\n\033[96mGroup {idx}:\033[0m")
#     for q in group:
#         _id = str(q.get('_id', ''))
#         cat = q.get('category', 'Unknown')
#         dif = q.get('difficulty', 'Unknown')
#         print(f"  ID: {_id}, Category: {cat}, Difficulty: {dif}")
