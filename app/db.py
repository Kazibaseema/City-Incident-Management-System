from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["cityops"]
incidents_col = db["incidents"]

# Ensure geospatial index
incidents_col.create_index([("location", "2dsphere")])


# app/db.py (add below incidents_col)
alerts_col = db["alerts"]
# Optional: index alerts by timestamp
alerts_col.create_index([("created_at", 1)])
