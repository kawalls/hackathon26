from flask import Flask, request, jsonify, Blueprint
import requests
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv('search_api_key')

flight_bluePrint = Blueprint('flight', __name__)#changed to blueprint method

@flight_bluePrint.route('/flight', methods=['POST'])#changed to blueprint method 

def search_flights():
     data = request.json
     
     departure = data["departure"]
     arrival = data["arrival"]
     outbound_date = data["outbound_date"]
     return_date = data["return_date"]

     url = "https://www.searchapi.io/api/v1/search"

     params = {
         "engine": "google_flights",
         "flight_type": "round_trip",
         "departure_id": departure,
         "arrival_id": arrival,
         "outbound_date": outbound_date,
         "return_date": return_date,
         "api_key": api_key # changed to match variable 
     }

     response = requests.get(url, params=params)
     results = response.json()

     #return jsonify(results) commented out for newly added filtering code

     flightList = []
     for flight in results.get("best_flights",[]):
        flightp1 = flight["flights"][0] # gets all first section of flight list starting flight
        flightp2 = flight["flights"][-1] # gets all second section of flight list continuingflight
        flightList.append({
            "price": flight.get("price"),
            "total_duration": flight.get("total_duration"),
            "airline": flightp1.get("airline"),
            "airline_logo": flight.get("airline_logo"),
            "departure_airport": flightp1["departure_airport"].get("name"),
            "departure_time": flightp1["departure_airport"].get("time"),
            "arrival_airport": flightp2["arrival_airport"].get("name"),
            "arrival_time": flightp2["arrival_airport"].get("time"),
            "stops": len(flight["flights"]) - 1,
            "travel_class": flightp1.get("travel_class"),
            "type": flight.get("type")
                })

     return jsonify(flightList)

