from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys

app = Flask(__name__)

# MongoDB Connection
mongo_uri = "mongodb+srv://instasecur24:kick@flutterdata.cgalmbt.mongodb.net/?retryWrites=true&w=majority&appName=flutterdata"
client = MongoClient(mongo_uri)

def connect_db():
    try:
        client.admin.command('ping')  # Test the connection
        print("MongoDB connected")
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        sys.exit(1)

connect_db()

db = client.get_database()

# Define Schema Equivalent in Python (MongoDB does not enforce schemas)
question_collection = db["Qno_Count"]

@app.route("/", methods=["GET"])
def home():
    return jsonify("Hello World"), 200

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=80)
        print("Server started on port 80")
    except Exception as e:
        print(f"Server error: {e}")

# Exception Handling
import logging

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught Exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
