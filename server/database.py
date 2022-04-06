import os
from pymongo import *
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv(os.path.abspath(".env"))

uri = os.environ["MONGODB_URI"]
client = MongoClient(uri)

scrutiny_db = client.get_database("ScrutinyDB")
users = scrutiny_db["Users"]

def make_id(uid):
    id = None

    try:
        id = ObjectId(uid)
    except:
        return { "status": "ERROR" }

    return { "status": "OK", "id": id }

def register_user(obj):
    users.insert_one({ "name": obj["name"], "disturbances":  obj["disturbances"]})

    res = users.find_one({ "name": obj["name"] })
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

def add_data_to_db(uid, data):
    res_id = make_id(uid)

    if res_id["status"] != "OK":
        return res_id

    users.update_one({ "_id": res_id["id"] }, { "$push": { "disturbances": data } })

    return { "status": "OK" }

def get_data_from_db(uid):
    res_id = make_id(uid)

    if res_id["status"] != "OK":
        return res_id

    res = users.find_one({ "_id": res_id["id"] })

    return { "status": "OK", "data": res["disturbances"] }