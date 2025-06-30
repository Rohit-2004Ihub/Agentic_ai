from pymongo import MongoClient
from datetime import datetime
import pytz
import hashlib

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["case_study_ai"]
collection = db["refined_result"] 

def generate_text_hash(text: str) -> str:
    """
    Generate a unique SHA256 hash for the given text.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def save_rag_result(user_id, document_name, refined_text, metadata=None):
    """
    Save the RAG result to MongoDB if it's not a duplicate (based on text hash).
    Timestamp is saved in IST.
    """
    ist_now = datetime.now(pytz.timezone("Asia/Kolkata"))
    text_hash = generate_text_hash(refined_text)

    # Prevent duplicate based on hash
    existing = collection.find_one({
        "user_id": user_id,
        "document_name": document_name,
        "hash": text_hash
    })

    if existing:
        print("⚠️ Duplicate detected: Same user, document, and text already saved.")
        return

    data = {
        "user_id": user_id,
        "document_name": document_name,
        "refined_text": refined_text,
        "hash": text_hash,
        "metadata": metadata or {},
        "timestamp": ist_now
    }

    collection.insert_one(data)
    print("✅ RAG result saved successfully.")
