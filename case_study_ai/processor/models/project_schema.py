from pymongo import MongoClient
import os
from datetime import datetime

client = MongoClient(os.getenv("MONGO_URI"))
db = client["case_study_ai"]

def save_case_study(student_name, structured, case_study, visuals, pitch_feedback):
    db.cases.insert_one({
        "student_name": student_name,
        "structured": structured,
        "case_study": case_study,
        "visuals": visuals,
        "pitch_feedback": pitch_feedback,
        "timestamp": datetime.now()
    })
