from pymongo import MongoClient
from flask import request,jsonify
from bson import ObjectId

def edit_travel(travel_id):
    client = MongoClient("mongodb://localhost:27017")
    db = client["country_db"]
    collection = db["travels"]

    title = request.form.get("travel_title")
    desc = request.form.get("travel_desc")
    start = request.form.get("travel_start")
    end = request.form.get("travel_end")
    cost = request.form.get("travel_cost")
    country = request.form.get("travel_country")


    try:
        result = collection.update_one(
            {"_id":ObjectId(travel_id)},
            {"$set":{
             "title":title,
             "desc":desc,
             "start":start,
             "end":end,
             "cost":cost,
             "country":country
            }}                                   
        )
        
        return jsonify({
                "message":"Travel was updated succesfully", 
                "data":travel_id, 
                "ok":True
            })




    except Exception as e:
        return jsonify({
                "message":"An error occured", 
                "data":str(0),
                "ok":False
            })