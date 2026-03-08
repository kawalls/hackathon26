from flask import Flask, request, jsonify, Blueprint
import requests
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv('serp_api_key')

hotel_bluePrint = Blueprint('hotel', __name__)#changed to blueprint method

@hotel_bluePrint.route('/hotel', methods=['POST'])#changed to blueprint method 

def search_hotels():
     data = request.json
     
     destination = data["destination"]
     check_in_date = data["check_in_date"]
     check_out_date = data["check_out_date"]
     adults = data["adults"]
     children = data["children"]

     url = "https://serpapi.com/search" 
#url = "https://www.searchapi.io/api/v1/search" og
     params = {
         "engine": "google_hotels",
         "q": destination,
         "check_in_date": check_in_date,
         "check_out_date": check_out_date,
         "adults": adults,
         "children": children,
         "api_key": api_key # changed to match variable 
     }

     response = requests.get(url, params=params)
     results = response.json()
     #print(results.keys()) used for trouble shootingggg
     #print(results)
     #print(results["properties"][0])

     #return jsonify(results) commented out for newly added filtering code

     hotelList = []
     for hotel in results.get("properties",[]):
       hotelList.append({
            "name": hotel.get("name"),     
            "type": hotel.get("type"),
            "reviews": hotel.get("reviews"),
            "thumbnail": hotel.get("images", [{}])[0].get("thumbnail"), #different than {} since contains a list of dicts
            "check_in_date": hotel.get("check_in_date"),# could omit since we just needed the requested info
            "check_out_date": hotel.get("check_out_date"),# could omit since we just needed the requested info
            "overall_rating": hotel.get("overall_rating"),
            "rate_per_night": hotel.get("rate_per_night", {}).get("extracted_lowest"),# pulls lowest rape per night since extracted within the rate_per night
            "amenities": hotel.get("amenities"),
            "total_price": hotel.get("total_rate", {}). get("extracted_lowest"),
                })

     return jsonify(hotelList)

