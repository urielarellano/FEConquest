import certifi
from pymongo import MongoClient
import json
from dotenv import load_dotenv
load_dotenv()
uri = os.getenv("MONGODB_URI")

client = MongoClient(uri,
                     tlsCAFile=certifi.where()
                     )

db = client["FEConquest"]
collection = db["classes"]

with open("hoshidan-classes.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

print("✅ Data inserted into MongoDB!")

