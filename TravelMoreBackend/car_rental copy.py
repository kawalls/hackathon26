from flask import Flask, request, jsonify, Blueprint
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


api_key = os.getenv('serp_api_key')

car_rental_bluePrint = Blueprint('car_rental', __name__)#changed to blueprint method

@car_rental_bluePrint.route('/car_rental', methods=['POST'])#changed to blueprint method 

def search_car_rentals():
     data = request.json
     
     destination = data["destination"]
     check_in_date = data["check_in_date"]
     check_out_date = data["check_out_date"]
     passengers = data["passengers"]

     url = "https://serpapi.com/search" 
     #url = "https://www.searchapi.io/api/v1/search" og
     params = {
     "engine": "google",
     "q": f"car rentals in {destination}, seating {passengers} passengers, from {check_in_date} to {check_out_date}",
     "api_key": api_key
     }

     response = requests.get(url, params=params)
     results = response.json()

     # convert dates to day numbers
     check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
     check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
     day_count = (check_out - check_in).days


     #print(results.keys()) #used for trouble shootingggg
     #rint(results)
     #print(results["properties"][0])

     #return jsonify(results) #commented out for newly added filtering code

     car_rental_List = []
     ads = results.get("ads", [])
     
     for ad in ads: #products are in ads when it comes to the query so you have to loop in 
          if "products" in ad:
               source = ad.get("source")
               for car in ad.get("products", []):
                    extensions = car.get("extensions", [])
                    price_string = extensions[0] if extensions else None
                    daily_cost = float(price_string.replace("$", "").replace(",", "")) if price_string else None
                    car_rental_List.append({
                        "title": car.get("title"),
                        "price_per_day": daily_cost,
                        "total_price": round(daily_cost * day_count, 2) if daily_cost else None,
                        "daily_cost": daily_cost,
                        "company": source,
                    })
     return jsonify(car_rental_List)

