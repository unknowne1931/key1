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




































# from pymongo import MongoClient
# import os
# import ctypes

# # Clear the console
# os.system('cls' if os.name == 'nt' else 'clear')

# # MongoDB connection
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# db = client["test"]
# qno_counts_collection = db["qno_counts"]
# qno_list_collection = db["question datas"]

# # Get unique categories with English language
# categories = []
# for doc in qno_list_collection.find({"language": "English"}):
#     if doc['category'] not in categories:
#         categories.append(doc['category'])

# # Count number of questions per category
# category_lengths = []
# for category in categories:
#     count = qno_list_collection.count_documents({"category": category, "language": "English"})
#     category_lengths.append({"category": category, "length": count})

# er_01 = []

# # Compare lengths
# if category_lengths:
#     base_length = category_lengths[1]['length'] or category_lengths[0]['length']
#     for cat in category_lengths:
#         if cat['length'] != base_length:
#             print(f"\033[93mCategory '{cat['category']}' has length {cat['length']} (not equal to {base_length})\033[0m")
#             print(f"\033[91mSome questions are missing {cat['category']} length Questions not Enough \033[0m")
#             er_01.append(cat['category'])
            
#             # ctypes.windll.user32.MessageBoxW(0, f"Some questions are missing IN : {cat['category']}", "Missing Questions Alert", 1)
            
#         elif int(cat['length'])  > int(base_length):
#             print(f"\033[93mThe length of {cat['category']} is High in Length {cat['length']}\033[0m")
            
#         else:
#             print(f"\033[92mCategory '{cat['category']}' has length {cat['length']} (equal to {base_length})\033[0m")


# if len(er_01) > 0:
#     for er in er_01:
#         print(f"\033[91m make fix this {er} length Increase or Decrease to continue \033[0m")
#         # exit()

# else:
#     print("\033[92mSelected Category Questions have same length\033[0m")
#     print("add function and make contine frome here")

# if len(category_lengths) == 10:
#     print("\033[92mAll category is ok\033[0m")
# else:
#     print("\033[91msome category questions are missing\033[0m")
#     print(f"\033[91mI Found {len(category_lengths)} Questions Types Only\033[0m")























# from pymongo import MongoClient
# import os
# import time

# # Optional: Only use ctypes if you're on Windows and want to show a popup
# # import ctypes


# # Clear the console
# os.system('cls' if os.name == 'nt' else 'clear')

# # MongoDB connection
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# db = client["test"]
# qno_list_collection = db["question datas"]



# final_arry = []

# # make chage it to 10 after to add 10 questions
# expected_category_count = 10
# tought_need_len = 0
# specific_num = []
# type_difi = [ 'Too Easy', 'Easy', 'Medium', 'Tough', 'Too Tough']





# def get_all_qno_to_bal():
#     print(f"expected Ways {len(specific_num)}")
#     print(f"Need {tought_need_len}")
#     # for dat in data:
#     #     print(dat['difficulty'], dat['category'])

        

    
    




# # Get unique categories with English language
# categories = set()
# for doc in qno_list_collection.find({"language": "English"}):
#     categories.add(doc['category'])

# # Count number of questions per category
# category_lengths = []
# for category in categories:
#     count = qno_list_collection.count_documents({"category": category, "language": "English"})
#     category_lengths.append({"category": category, "length": count})

# # Error tracking
# er_01 = []
# category_lengths_list = 0

# # Compare lengths
# if category_lengths:
#     # Choose the least length as base for comparison
#     base_length = min([c['length'] for c in category_lengths])
#     lengths = [c['length'] for c in category_lengths]
#     category_lengths_list = base_length
#     base_length = max(set(lengths), key=lengths.count)  # Most common length

#     print(f"\nBase length chosen for comparison: {base_length}\n")

#     for cat in category_lengths:
#         cat_name = cat['category']
#         cat_len = cat['length']
#         if cat_len < base_length:
#             print(f"\033[93mCategory '{cat_name}' has only {cat_len} questions. Expected: {base_length}\033[0m")
#             print(f"\033[91mSome questions are missing in category '{cat_name}'. Please add more.\033[0m")
#             er_01.append(cat_name)

#             # Optional popup alert (Windows only)
#             # ctypes.windll.user32.MessageBoxW(0, f"Missing questions in: {cat_name}", "Alert", 1)

#         elif cat_len > base_length:
#             print(f"\033[93mCategory '{cat_name}' has extra questions: {cat_len} > {base_length}\033[0m")
#         else:
#             print(f"\033[92mCategory '{cat_name}' has correct number of questions: {cat_len}\033[0m")

# # Summary
# print("\n" + "-"*50)

# if er_01:
#     for cat in er_01:
#         print(f"\033[91m❌ Fix required: Adjust number of questions in '{cat}' to match others.\033[0m")
#     # Optional: exit after error
#     # exit(1)
# else:
#     print("\033[92m✅ All selected category questions have the same length.\033[0m")
#     print("🔁 You can proceed with the next step here...")



# total_qno_len = qno_list_collection.count_documents({})

# sum = total_qno_len - expected_category_count


# i = sum

# while i > 0:
#     specific_num.append(i)
#     i-=expected_category_count

# print(f"I Found {len(specific_num)} Groups")



# for dat in type_difi:
#     print(f"Need {len(specific_num)*2} {dat} Questions")
#     tought_need_len = len(specific_num)*2

# get_all_qno_to_bal()

# print(f"Totaly need {len(specific_num)*expected_category_count} Questions")






# # for i in range(category_lengths_list):
# #     final_arry.append([])






# # # Final check for number of categories

# # if len(category_lengths) == expected_category_count:
# #     print(f"\033[92m✅ All {expected_category_count} categories are present.\033[0m")
# #     for cat_gr_len in category_lengths:
# #         get_all_qno_to_bal(expected_category_count, cat_gr_len, category_lengths_list)

# # else:
# #     print(f"\033[91m⚠️ Expected {expected_category_count} categories but found {len(category_lengths)}.\033[0m")
























# from pymongo import MongoClient
# from collections import defaultdict

# # MongoDB connection
# client = MongoClient("mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata")
# db = client["test"]
# qno_list_collection = db["question datas"]

# # Config
# difficulties = ['Too Easy', 'Easy', 'Medium', 'Tough', 'Too Tough']
# expected_category_count = 10
# all_qnlist = []
# specific_num = []

# total_qno_len = qno_list_collection.count_documents({})

# sum = total_qno_len - expected_category_count


# i = sum

# while i > 0:
#     specific_num.append(i)
#     i-=expected_category_count

# for dif in difficulties:
#     data = qno_list_collection.find({"difficulty" : dif})
#     for data_new in data:
#         dat = {
#             "difficulty" : data_new['difficulty'],
#             "category" : data_new['category'],
#             "id" : data_new['_id']
#         }
#         all_qnlist.append(dat)

# # for item in all_qnlist:
# #     print(f"Difficulty: {item['difficulty']} ; Category: {item['category']} ; ID: {item['id']}")


# print(f"\033[92mGroups from {specific_num} , Expected Group : {len(specific_num)}\033[0m")

import os

os.system('cls')

ary1 = []
ary2 = []
ary3 = []


data = [
  {
    "_id": {
      "$numberInt": "1"
    },
    "language": "English",
    "category": "calend",
    "difficulty": "Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:01Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:01Z"
    }
  },
  {
    "_id": {
      "$numberInt": "2"
    },
    "language": "English",
    "category": "colo",
    "difficulty": "Medium",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:02Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:02Z"
    }
  },
  {
    "_id": {
      "$numberInt": "3"
    },
    "language": "English",
    "category": "spel",
    "difficulty": "Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:03Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:03Z"
    }
  },
  {
    "_id": {
      "$numberInt": "4"
    },
    "language": "English",
    "category": "int_text",
    "difficulty": "Too Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:04Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:04Z"
    }
  },
  {
    "_id": {
      "$numberInt": "5"
    },
    "language": "English",
    "category": "sudoku",
    "difficulty": "Too Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:05Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:05Z"
    }
  },
  {
    "_id": {
      "$numberInt": "6"
    },
    "language": "English",
    "category": "gk",
    "difficulty": "Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:06Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:06Z"
    }
  },
  {
    "_id": {
      "$numberInt": "7"
    },
    "language": "English",
    "category": "img_smlr",
    "difficulty": "Medium",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:07Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:07Z"
    }
  },
  {
    "_id": {
      "$numberInt": "8"
    },
    "language": "English",
    "category": "sent",
    "difficulty": "Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:08Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:08Z"
    }
  },
  {
    "_id": {
      "$numberInt": "9"
    },
    "language": "English",
    "category": "msng_ltr",
    "difficulty": "Too Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:09Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:09Z"
    }
  },
  {
    "_id": {
      "$numberInt": "10"
    },
    "language": "English",
    "category": "shape",
    "difficulty": "Too Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:10Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:10Z"
    }
  },
  {
    "_id": {
      "$numberInt": "11"
    },
    "language": "English",
    "category": "calend",
    "difficulty": "Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:11Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:11Z"
    }
  },
  {
    "_id": {
      "$numberInt": "12"
    },
    "language": "English",
    "category": "colo",
    "difficulty": "Medium",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:12Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:12Z"
    }
  },
  {
    "_id": {
      "$numberInt": "13"
    },
    "language": "English",
    "category": "spel",
    "difficulty": "Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:13Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:13Z"
    }
  },
  {
    "_id": {
      "$numberInt": "14"
    },
    "language": "English",
    "category": "int_text",
    "difficulty": "Too Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:14Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:14Z"
    }
  },
  {
    "_id": {
      "$numberInt": "15"
    },
    "language": "English",
    "category": "sudoku",
    "difficulty": "Too Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:15Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:15Z"
    }
  },
  {
    "_id": {
      "$numberInt": "16"
    },
    "language": "English",
    "category": "gk",
    "difficulty": "Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:16Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:16Z"
    }
  },
  {
    "_id": {
      "$numberInt": "17"
    },
    "language": "English",
    "category": "img_smlr",
    "difficulty": "Medium",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:17Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:17Z"
    }
  },
  {
    "_id": {
      "$numberInt": "18"
    },
    "language": "English",
    "category": "sent",
    "difficulty": "Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:18Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:18Z"
    }
  },
  {
    "_id": {
      "$numberInt": "19"
    },
    "language": "English",
    "category": "msng_ltr",
    "difficulty": "Too Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:19Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:19Z"
    }
  },
  {
    "_id": {
      "$numberInt": "20"
    },
    "language": "English",
    "category": "shape",
    "difficulty": "Too Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:20Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:20Z"
    }
  },
  {
    "_id": {
      "$numberInt": "21"
    },
    "language": "English",
    "category": "calend",
    "difficulty": "Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:21Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:21Z"
    }
  },
  {
    "_id": {
      "$numberInt": "22"
    },
    "language": "English",
    "category": "colo",
    "difficulty": "Medium",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:22Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:22Z"
    }
  },
  {
    "_id": {
      "$numberInt": "23"
    },
    "language": "English",
    "category": "spel",
    "difficulty": "Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:23Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:23Z"
    }
  },
  {
    "_id": {
      "$numberInt": "24"
    },
    "language": "English",
    "category": "int_text",
    "difficulty": "Too Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:24Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:24Z"
    }
  },
  {
    "_id": {
      "$numberInt": "25"
    },
    "language": "English",
    "category": "sudoku",
    "difficulty": "Too Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:25Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:25Z"
    }
  },
  {
    "_id": {
      "$numberInt": "26"
    },
    "language": "English",
    "category": "gk",
    "difficulty": "Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:26Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:26Z"
    }
  },
  {
    "_id": {
      "$numberInt": "27"
    },
    "language": "English",
    "category": "img_smlr",
    "difficulty": "Medium",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:27Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:27Z"
    }
  },
  {
    "_id": {
      "$numberInt": "28"
    },
    "language": "English",
    "category": "sent",
    "difficulty": "Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:28Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:28Z"
    }
  },
  {
    "_id": {
      "$numberInt": "29"
    },
    "language": "English",
    "category": "msng_ltr",
    "difficulty": "Too Tough",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:29Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:29Z"
    }
  },
  {
    "_id": {
      "$numberInt": "30"
    },
    "language": "English",
    "category": "shape",
    "difficulty": "Too Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:30Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:30Z"
    }
  },
  {
    "_id": {
      "$numberInt": "31"
    },
    "language": "English",
    "category": "calend",
    "difficulty": "Too Easy",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:31Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:31Z"
    }
  },
  {
    "_id": {
      "$numberInt": "32"
    },
    "language": "English",
    "category": "colo",
    "difficulty": "Medium",
    "type": "Mental Ability",
    "createdAt": {
      "$date": "2025-06-02T06:45:32Z"
    },
    "updatedAt": {
      "$date": "2025-06-02T06:45:32Z"
    }
  }
]

# Create a dictionary to hold groups by (category, difficulty)


# Print all categories and all difficulties found in the data
categories = sorted(set(d['category'] for d in data))
difficulties = sorted(set(d['difficulty'] for d in data))
print("Categories:", categories)
print("Difficulties:", difficulties)
print()
grouped = {}



expected_category_count = 10
data_len = len(data) - expected_category_count


i = data_len
specific_num = []


while i > 0:
    specific_num.append(i)
    i-=expected_category_count


#tough calculus
need_qn_ln = len(specific_num)*2


print(f"\033[92m{len(specific_num)} Groups Possible\033[0m")



# Fill the dictionary
for dat in data:
    cat = dat['category']
    dif = dat['difficulty']
    key = (cat, dif)
    if key not in grouped:
        grouped[key] = []
    grouped[key].append(dat)

# Print required count for each (category, difficulty) and show if enough exist
print("\nRequired per (category, difficulty):", len(specific_num))
print("Summary of all categories and all difficulties:\n")
for cat in categories:
    for dif in difficulties:
        key = (cat, dif)
        count = len(grouped.get(key, []))
        enough = count >= len(specific_num)
        status = "✅ Enough" if enough else "❌ Not enough"
        color = "\033[92m" if enough else "\033[91m"
        print(f"{color}Category: {cat:10} | Difficulty: {dif:9} | Count: {count:2} | {status}\033[0m")
print()


# Create groups of 10 questions, as many as len(specific_num)
groups = []
for group_idx in range(len(specific_num)):
    group = []
    for cat in categories:
        for dif in difficulties:
            key = (cat, dif)
            # Only add if there are enough questions for this group
            if len(grouped.get(key, [])) > group_idx:
                group.append(grouped[key][group_idx])
            # Stop if group reaches 10 questions
            if len(group) == 10:
                break
        if len(group) == 10:
            break
    if len(group) == 10:
        groups.append(group)

# Print the groups
for idx, group in enumerate(groups, 1):
    print(f"\n\033[96mGroup {idx}:\033[0m")
    for q in group:
        print(f"  ID: {q['_id']['$numberInt']}, Category: {q['category']}, Difficulty: {q['difficulty']}")



