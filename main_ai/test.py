from pymongo import MongoClient
import os

# MongoDB connection
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
)
client = MongoClient(MONGODB_URI)
db = client["test"]
histories_db = db['histories']

# Fetch credited transactions
credited_data = histories_db.find({"type": "Credited"})

# Aggregate total credited amounts by user
user_totals = {}
for record in credited_data:
    user_id = str(record.get("user", "Unknown"))
    rupee_amount = record.get("rupee", 0)

    # Convert to float if string, default 0 if not valid
    try:
        rupee_amount = float(rupee_amount)
    except (ValueError, TypeError):
        rupee_amount = 0

    user_totals[user_id] = user_totals.get(user_id, 0) + rupee_amount

# Sort by credited amount (highest first)
top_users = sorted(user_totals.items(), key=lambda x: x[1], reverse=True)[:3]

# Display results
print("Top 3 Credited Users:")
for rank, (user_id, total_amount) in enumerate(top_users, start=1):
    print(f"{rank}. User: {user_id} | Total Credited: ₹{total_amount}")
