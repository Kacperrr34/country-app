from flask import request,jsonify
from pymongo import MongoClient

def add_travel():
    client = MongoClient("mongodb://localhost:27017")
    db = client["country_db"]
    collection = db["travels"]

    # tytul, opis, data rozpoczecia, data powrotu, cena, kraj
    title = request.form.get("travel_title")
    desc = request.form.get("travel_desc")
    start = request.form.get("travel_start")
    end = request.form.get("travel_end")
    cost = request.form.get("travel_cost")
    country = request.form.get("travel_country")

    try:


        data= {
            "title":title, 
           "desc":desc,
           "start":start,
           "end":end,
           "cost":cost,
           "country":country
        }
        collection.insert_one(data)

        data["_id"] = str(data["_id"])


        return jsonify({
            "message":"New travel added", 
            "ok":True,
            "data":data
        })

    
    except Exception as e:
        return jsonify({
            "message":"An error occured",
            "error": str(e), 
            "ok":False
        }) 
