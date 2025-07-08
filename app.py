from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["events"]

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    formatted_data = {
        "request_id": data.get("request_id"),
        "author": data.get("author"),
        "action": data.get("action"),
        "from_branch": data.get("from_branch"),
        "to_branch": data.get("to_branch"),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }
    collection.insert_one(formatted_data)
    return jsonify({"message": "Event stored successfully"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
