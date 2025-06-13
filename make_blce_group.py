# from pymongo import MongoClient
# import os
# import time


# os.system('cls')

# # MongoDB connection
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# db = client["test"]
# qno_counts_collection = db["qno_counts"]
# qno_list_collection = db["question datas"]

# # Convert cursor to list
# data = list(qno_list_collection.find())

# # Compute group count logic
# expected_category_count = 10
# data_len = len(data) - expected_category_count

# total_questions = len(data)  # or any integer value

# sum_value = total_questions - 9
# grp_ary = []
# tough_lst = []
# cate_lst = []

# for dat in data:
#     if dat['difficulty'] in tough_lst:
#         continue
#     else:
#         tough_lst.append(dat['difficulty'])


# for dat in data:
#     if dat['category'] in cate_lst:
#         continue
#     else:
#         cate_lst.append(dat['category'])



# specific_numbers = []
# for i in range(sum_value, 0, -10):
#     specific_numbers.append(i)
#     grp_ary.append([])


# print(specific_numbers)
# print(grp_ary)
# print(tough_lst)
# print(cate_lst)


# for dat in grp_ary:
#     while len(dat) < expected_category_count:
#         for tg in tough_lst:
#             data = qno_list_collection.find({"difficulty" : tg})
#             for get_data in data:
#                 if get_data['difficulty'] and get_data['category'] in dat:
#                     continue
#                 else:
#                     dat.append(data)
#                 # print(get_data['difficulty'] + get_data['category'])
#             # count_easy = sum(1 for item in data if item['difficulty'] == tg)
#             # if count_easy <= 2 and data['_id'] not in dat["difficulty"]:
#             #     dat.append(i)
                
                
 
#             # if tg not in dat['difficulty'] and 


# print(len(grp_ary))

# for data in grp_ary:
#     for dat in data:
#         print(dat)










# from pymongo import MongoClient
# import os

# # Clear screen
# os.system('cls' if os.name == 'nt' else 'clear')

# # MongoDB connection
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# db = client["test"]
# qno_list_collection = db["question datas"]

# # Fetch all questions
# all_questions = list(qno_list_collection.find())

# expected_category_count = 10
# total_questions = len(all_questions)
# sum_value = total_questions - 9  # Controls number of groups

# specific_numbers = []
# for i in range(sum_value, 0, -10):
#     specific_numbers.append(i)



# # Extract unique difficulties and categories
# difficulties = list({q['difficulty'] for q in all_questions})
# categories = list({q['category'] for q in all_questions})

# # Create group slots and group counters
# group_count = sum_value // expected_category_count
# grp_ary = [[] for _ in range(group_count)]

# print(f"Total Questions: {total_questions}")
# print(f"Group Count: {group_count}")
# print(f"Difficulties: {difficulties}")
# print(f"Categories: {categories}")
# print(f'Groups Starts : {specific_numbers}')

# # Helper to track used questions
# used_ids = set()

# # Begin grouping
# for group in grp_ary:
#     group_categories = set()
#     group_difficulties = set()

#     for question in all_questions:
#         qid = str(question['_id'])

#         if qid in used_ids:
#             continue

#         # Ensure uniqueness in category and difficulty
#         if question['category'] in group_categories:
#             continue
#         if question['difficulty'] in group_difficulties:
#             continue

#         # Add to group
#         group.append(question)
#         group_categories.add(question['category'])
#         group_difficulties.add(question['difficulty'])
#         used_ids.add(qid)

#         if len(group) >= expected_category_count:
#             break

# # Print results
# print(f"\nTotal Groups Formed: {len(grp_ary)}\n")

# for idx, group in enumerate(grp_ary, 1):
#     print(f"\nGroup {idx} ({len(group)} questions):")
#     for q in group:
#         print(f"  - ID: {q['_id']} | Difficulty: {q['difficulty']} | Category: {q['category']}")












# from pymongo import MongoClient
# import os
# import random

# # Clear screen
# os.system('cls' if os.name == 'nt' else 'clear')

# # MongoDB connection
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# db = client["test"]
# qno_list_collection = db["question datas"]

# # Fetch all questions
# all_questions = list(qno_list_collection.find())
# random.shuffle(all_questions)  # Optional: Shuffle to randomize selection

# expected_category_count = 10
# total_questions = len(all_questions)
# group_count = (total_questions // expected_category_count)
# sum_value = total_questions - (expected_category_count-1) 

# specific_numbers = []
# for i in range(sum_value, 0, -expected_category_count):
#     specific_numbers.append(i)

# print(f"Total Questions: {total_questions}")
# print(f"Target Groups: {group_count}")
# print(f"Specific numbers: {specific_numbers}")

# # Difficulty group requirement
# difficulty_structure = ["Too Easy", "Too Easy", "Easy", "Easy"]

# # Prepare storage
# used_ids = set()
# grp_ary = []

# # Helper to filter questions
# def get_question(difficulty, excluded_categories):
#     for q in all_questions:
#         qid = str(q['_id'])
#         if (
#             qid not in used_ids and
#             q['difficulty'] == difficulty and
#             q['category'] not in excluded_categories
#         ):
#             return q
#     return None

# # Start grouping
# for _ in range(group_count):
#     group = []
#     used_categories = set()

#     # Add specific difficulty pattern first
#     for diff in difficulty_structure:
#         q = get_question(diff, used_categories)
#         if q:
#             group.append(q)
#             used_ids.add(str(q['_id']))
#             used_categories.add(q['category'])

#     # Fill the rest (6 more questions) without repeating category
#     for q in all_questions:
#         if len(group) >= expected_category_count:
#             break
#         qid = str(q['_id'])
#         if qid in used_ids or q['category'] in used_categories:
#             continue
#         group.append(q)
#         used_ids.add(qid)
#         used_categories.add(q['category'])

#     if len(group) == expected_category_count:
#         grp_ary.append(group)

# # Print results
# print(f"\nTotal Groups Formed: {len(grp_ary)}")

# for idx, group in enumerate(grp_ary, 0):

#     print(f"\nGroup {idx + 1} ({len(group)} questions):")
#     for q_idx, q in enumerate(group, 0):
#         print(specific_numbers[q_idx])
#         sum_tott = specific_numbers[q_idx] + (expected_category_count-1)
#         while specific_numbers[q_idx] <= sum_tott:
#             specific_numbers[q_idx] = specific_numbers[q_idx] + 1
#             print(f" no {q_idx} : QNO {specific_numbers}. ID: {q['_id']} | Difficulty: {q['difficulty']} | Category: {q['category']}")






















































# 99% correct




# from pymongo import MongoClient
# import os
# import random
# import sys
# import time

# # Clear screen
# os.system('cls' if os.name == 'nt' else 'clear')

# # MongoDB connection
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# db = client["test"]
# qno_list_collection = db["question datas"]
# live_data_base = db['qno_counts']

# # Delete all documents from "qno_counts" collection
# delete_result = live_data_base.delete_many({})
# print(f"\nDeleted {delete_result.deleted_count} documents from 'qno_counts' collection.")


# # Fetch all questions
# all_questions = list(qno_list_collection.find())
# random.shuffle(all_questions)  # Optional: Shuffle to randomize selection

# expected_category_count = 10
# total_questions = len(all_questions)
# group_count = (total_questions // expected_category_count)
# sum_value = total_questions - (expected_category_count-1) 

# specific_numbers = []
# for i in range(sum_value, 0, -expected_category_count):
#     specific_numbers.append(i)

# print(f"Total Questions: {total_questions}")
# print(f"Target Groups: {group_count}")
# print(f"Specific numbers: {specific_numbers}")

# # Difficulty group requirement
# difficulty_structure = ["Too Easy", "Too Easy", "Easy", "Easy"]

# # Prepare storage
# used_ids = set()
# grp_ary = []

# # Helper to filter questions
# def get_question(difficulty, excluded_categories):
#     for q in all_questions:
#         qid = str(q['_id'])
#         if (
#             qid not in used_ids and
#             q['difficulty'] == difficulty and
#             q['category'] not in excluded_categories
#         ):
#             return q
#     return None

# # Start grouping
# for _ in range(group_count):
#     group = []
#     used_categories = set()

#     # Add specific difficulty pattern first
#     for diff in difficulty_structure:
#         q = get_question(diff, used_categories)
#         if q:
#             group.append(q)
#             used_ids.add(str(q['_id']))
#             used_categories.add(q['category'])

#     # Fill the rest (6 more questions) without repeating category
#     for q in all_questions:
#         if len(group) >= expected_category_count:
#             break
#         qid = str(q['_id'])
#         if qid in used_ids or q['category'] in used_categories:
#             continue
#         group.append(q)
#         used_ids.add(qid)
#         used_categories.add(q['category'])

#     if len(group) == expected_category_count:
#         grp_ary.append(group)

# # Print results
# print(f"\nTotal Groups Formed: {len(grp_ary)}")


# for idx, group in enumerate(grp_ary):
#     start_qno = specific_numbers[idx]  # e.g., 91, 81, ...
#     print(f"\nGroup {idx + 1} ({len(group)} questions):")
    
#     for i, q in enumerate(group):
#         qno = start_qno + i  # sequential question number
#         print(f" QNO {qno} - ID: {q['_id']} | Difficulty: {q['difficulty']} | Category: {q['category']}")
#         ans = ''
#         if q['answer'] == q['a']:
#             ans == "a"
#         elif q['answer'] == q['b']:
#             ans == "b"
#         elif q['answer'] == q['c']:
#             ans == "c"
#         elif q['answer'] == q['d']:
#             ans == "d"
#         else:
#             print(f"\033[91mSome answers are Missing. Check it id: {q['_id']}\033[0m")
#             sys.exit("Stopping execution as requested.")

#         live_data_base.insert_one(
#             {
#                 "Time": time.time(),
#                 "user": "Auto",
#                 "img": q['image'],
#                 "Questio": q['question'],
#                 "qno": f"{qno}",
#                 "a": q['a'],
#                 "b": q['b'],
#                 "c": q['c'],
#                 "d": q['d'],
#                 "Ans": ans,
#                 "lang": q['language'],
#                 "tough": q['difficulty'],
#                 "seconds": q['seconds'],
#                 "sub_lang": q['category'],
#                 "yes": [
#                     ""
#                 ],
#                 "no": [
#                     "",
#                     ],        
#                 }
#             )



# print("Everythin Ok")
# print('\033[1;32m' + '\033[1m' + '\033[38;2;0;255;0m' + "\n\n" + "Everything Ok".center(40) + '\033[0m')
# print('\033[1;32m' + '\033[1m' + '\033[38;2;0;255;0m' + "\n" + "NOTE: Font size 40px is only applicable in web/GUI, not in terminal." + '\033[0m')




























from pymongo import MongoClient
import os
import random
import sys
import time

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# MongoDB connection
client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
db = client["test"]
qno_list_collection = db["question datas"]
live_data_base = db['qno_counts']

# Delete all documents from "qno_counts" collection
delete_result = live_data_base.delete_many({})
print(f"\nDeleted {delete_result.deleted_count} documents from 'qno_counts' collection.")

# Fetch and shuffle all questions
all_questions = list(qno_list_collection.find())
random.shuffle(all_questions)

expected_category_count = 10
total_questions = len(all_questions)
group_count = total_questions // expected_category_count
sum_value = total_questions - (expected_category_count - 1)

# Create specific starting numbers for question groups
specific_numbers = []
for i in range(sum_value, 0, -expected_category_count):
    specific_numbers.append(i)

print(f"Total Questions: {total_questions}")
print(f"Target Groups: {group_count}")
print(f"Specific numbers: {specific_numbers}")

# Required difficulty structure per group
difficulty_structure = ["Too Easy", "Too Easy", "Easy", "Easy"]

# Track used question IDs and store groups
used_ids = set()
grp_ary = []

# Helper: Get question with specific difficulty & unused category
def get_question(difficulty, excluded_categories):
    for q in all_questions:
        qid = str(q['_id'])
        if (
            qid not in used_ids and
            q['difficulty'] == difficulty and
            q['category'] not in excluded_categories
        ):
            return q
    return None

# Start forming groups
for _ in range(group_count):
    group = []
    used_categories = set()

    # Add required difficulty pattern
    for diff in difficulty_structure:
        q = get_question(diff, used_categories)
        if q:
            group.append(q)
            used_ids.add(str(q['_id']))
            used_categories.add(q['category'])

    # Fill remaining slots (6 more) without repeating categories
    for q in all_questions:
        if len(group) >= expected_category_count:
            break
        qid = str(q['_id'])
        if qid in used_ids or q['category'] in used_categories:
            continue
        group.append(q)
        used_ids.add(qid)
        used_categories.add(q['category'])

    # Add group only if it has exact number of questions
    if len(group) == expected_category_count:
        grp_ary.append(group)

# Insert groups into DB and display
print(f"\nTotal Groups Formed: {len(grp_ary)}")

for idx, group in enumerate(grp_ary):
    start_qno = specific_numbers[idx]
    print(f"\n--- Group {idx + 1} ({len(group)} questions) ---")
    
    for i, q in enumerate(group):
        qno = start_qno + i
        print(f" QNO {qno} - ID: {q['_id']} | Difficulty: {q['difficulty']} | Category: {q['category']}")

        # Determine correct option letter
        answer_text = q.get('answer', '')
        ans = ''
        if answer_text == q.get('a'):
            ans = "a"
        elif answer_text == q.get('b'):
            ans = "b"
        elif answer_text == q.get('c'):
            ans = "c"
        elif answer_text == q.get('d'):
            ans = "d"
        else:
            print(f"\033[91m❌ Answer mismatch or missing in ID: {q['_id']}\033[0m")
            sys.exit("Stopping execution due to answer error.")

        # Insert into qno_counts collection
        live_data_base.insert_one({
            "Time": time.time(),
            "ID" : f"{q.get('_id')}",
            "user": "Auto",
            "img": q.get('image', ''),
            "Questio": q.get('question', ''),
            "qno": f"{qno}",
            "a": q.get('a', ''),
            "b": q.get('b', ''),
            "c": q.get('c', ''),
            "d": q.get('d', ''),
            "Ans": ans,
            "lang": q.get('language', ''),
            "tough": q.get('difficulty', ''),
            "seconds": f"{q.get('seconds', 30)}",
            "sub_lang": q.get('category', ''),
            "yes": [""],
            "no": [""]
        })

# Final success message
print('\033[1;32m' + "\n\n" + "✅ Everything Ok".center(40) + '\033[0m')
