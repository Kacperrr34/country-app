from flask import Flask,render_template,request,jsonify,redirect
import requests 
app = Flask(__name__)
from pymongo import MongoClient
app.debug = True
from api.add_travel import add_travel
from api.all_travels import get_all_travels
from api.delete_travel import delete_travel
from api.get_travel_by_id import get_travel_by_id
from api.edit_travel import edit_travel


# API
# Dodaj nową podróz------------------------------------------------
@app.route("/api/add-travel",methods=["POST"])
def api_add_travel():
    response = add_travel()
    return redirect("/travels")

# endpoint dla uzyskania wszysktich podrozy z naszej apikacji lub innej dowolnej

@app.route("/api/get-all-travels")
def api_get_all_travels():
    data = get_all_travels()
    return data
    
# Endpoint usuwanie wybranej podróży
@app.route("/api/delete-travel", methods=["DELETE","POST"])
def api_delete_travel():
    id = request.form.get("id_to_delete")
    response = delete_travel(id)
    return redirect("/travels")

# Endpoint: edytowanie wybranego posta
@app.route("/api/edit-travel", methods=["POST"])
def api_edit_travel(): 

    id= request.form.get("id_to_edit")
    response = edit_travel(id)


    return redirect("/travels")

# endpoint jedna podróż zgodna z id

@app.route("/api/get-travel-by-id/<id>")
def api_get_travel_by_id(id):
    data = get_travel_by_id(id)
    return data








# ROUTY:------------------------

@app.route("/travels")
def travvels_page():
        response = requests.get("http://127.0.0.1:5000/api/get-all-travels")
        travels = response.json()

        return render_template("travels.html",travels=travels['data'])






@app.route("/edit-travel/<id>")
def edit_travel_page(id):
    try:
        response = requests.get(f"http://127.0.0.1:5000/api/get-travel-by-id/{id}")
        travel = response.json()
        
        countries_response = requests.get("https://restcountries.com/v3.1/all")
        countries = countries_response.json()
        
        names = list(map(lambda country: country['name']['common'], countries))
        
        return render_template("edit-travel.html", travel=travel['data'], names=names)
        
        


    except Exception as e:
        print(e,"Test")
        return render_template("edit-travel.html", travel={})


@app.route("/add-travel")
def page_add_travel():

    try:
        response = requests.get("https://restcountries.com/v3.1/all")
        countries = response.json()

        names = list(map(lambda country: country['name']['common'], countries))

        return render_template("add-travel.html", names=sorted(names))
    
    except Exception as e:
        print("Error",e)
        return render_template("add-travel.html", names=[])










@app.route("/", methods=["GET", "POST"])
def home_page():
    
   search_query = request.form.get("query")
   continent_filter = request.form.get("continent_filter")


   print(continent_filter)
   print(search_query)

   url = ""
   if search_query:
       url = f"https://restcountries.com/v3.1/name/{search_query}"
   else:
       url = "https://restcountries.com/v3.1/all"


   try:
     response = requests.get(url)
     countries = response.json()

     if continent_filter:
         countries = filter(lambda country: country['region'] == continent_filter,countries)

     return render_template("index.html", countries = countries)
   except Exception as e:
       print(f"Wystąpił błąd", str(e))
       return "Nie działa"


@app.route("/country/<name>")
def country_page(name):


   response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
   data = response.json()
   
   currency_key = list(data[0]['currencies'].keys())[0] if data[0].get("currencies") is not None else []
   native_name_key = list(data[0]['name']['nativeName'].keys())[0] if data[0]['name'].get("nativeName") is not None else []
   languages = list(data[0]['languages'].values()) if data[0].get("languages") is not None else []
   


   neighbours = []

   for field in data:
          if "borders" not in field:
              print("nie ma borders!")
            #   borders_placeholder.append("PL")
          else:
              border_countries = ','.join(data[0]['borders'])
              border_countries = ",".join(data[0]['borders'] if data[0]['borders'] else borders_placeholder)
              response_neighbours= requests.get(f"https://restcountries.com/v3.1/alpha?codes={border_countries}")
              neighbours_data = list(response_neighbours.json())
              neighbours = list(map(lambda neighbour: neighbour['name']['common'], neighbours_data))
            #   borders_placeholder = []


            #   return

 


   country = {
          "common_name":data[0]['name']['common'],
          "native_name":data[0]['name']['nativeName'][native_name_key]['common'] if data[0]['name'].get('nativeName') else "?",
          "currency_name": data[0]['currencies'][currency_key]['name'] if data[0].get("currencies") else "?",
          "languages":", ".join(languages),
          "population":data[0]['population'],
          "region":data[0]['region'],
          "capital":data[0]['capital'][0] if data[0].get('capital') else '?',
          "sub_region":data[0]['subregion'] if data[0].get("subregion") else '?',
          'tld':data[0]['tld'],
          "coat_of_arms":data[0]["coatOfArms"]['svg'] if data[0]['coatOfArms'] else data[0]['flags']['svg']
      }
   return render_template("country.html", country = country, neighbours=neighbours)
