from pymongo import MongoClient
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "case_study_ai"
COLLECTION_NAME = "refined_results"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_rag_result(document_name: str, refined_text: str, metadata: dict = {}):
    data = {
        "document_name": document_name,
        "refined_text": refined_text,
        "metadata": metadata,
        "timestamp": datetime.utcnow()
    }
    return collection.insert_one(data)
