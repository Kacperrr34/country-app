from pymongo import MongoClient
from flask import request,jsonify
from bson import ObjectId

def delete_travel(travel_id):
    client = MongoClient("mongodb://localhost:27017")
    db = client["country_db"]
    collection = db["travels"]

    try:
        result = collection.delete_one({"_id":ObjectId(travel_id)})
 
        print(result.deleted_count)

        if result.deleted_count > 0:
            return jsonify({
                "message":"Travel was deleted succesfully", 
                "data":travel_id, 
                "ok":True
            })
        else:
            return jsonify({
                "message":"Travel not exists", 
                "data":travel_id, 
                "ok":False
            })

    except Exception as e:
        return jsonify({
            "message":"An error occured",
            "error":str(e),
            "ok":False
        })