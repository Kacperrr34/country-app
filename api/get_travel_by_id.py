from pymongo import MongoClient
from flask import jsonify
from bson import ObjectId

def get_travel_by_id(travel_id):
    client = MongoClient("mongodb://localhost:27017")
    db = client["country_db"]
    collection = db["travels"]

    try:

        response = collection.find_one({"_id":ObjectId(travel_id)})

        response['_id'] = str(travel_id)
      
        return jsonify({
            "message":"Successfully data fetching",
            "data":response,
            "ok":True
        })

    except Exception as e:
        return jsonify({
            "message":"An error occured during data fetching",
            "error":str(e), 
            "ok":False
        })