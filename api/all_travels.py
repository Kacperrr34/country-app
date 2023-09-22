from pymongo import MongoClient
from flask import jsonify

def get_all_travels():
    client = MongoClient("mongodb://localhost:27017")
    db = client["country_db"]
    collection = db["travels"]

    try:

        response = collection.find()
        data = list(response)

        for travel in data:
            travel['_id'] = str(travel['_id'])
      
        return jsonify({
            "message":"Successfully data fetching",
            "data":data,
            "ok":True
        })

    except Exception as e:
        return jsonify({
            "message":"An error occured during data fetching",
            "error":str(e), 
            "ok":False
        })