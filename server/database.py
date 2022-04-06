from asyncio.proactor_events import _ProactorBaseWritePipeTransport
import os
from pymongo import *
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv(os.path.abspath(".env"))

uri = os.environ["MONGODB_URI"]
client = MongoClient(uri)

scrutiny_db = client.get_database("ScrutinyDB")
users = scrutiny_db["Users"]

def register_user(name):
    users.insert_one({ "name": name })

    res = users.find_one({ "name": name })
    id = str(res["_id"])

    return { "status": "OK", "uid": id }

def verify_user(uid):
    id = None

    try:
        id = ObjectId(uid)
    except:
        return { "status": "OK", "exists": False }

    res = users.find_one({ "_id":  id })

    if res != None:
        return { "status": "OK", "exists": True }
    
    return { "status": "OK", "exists": False }