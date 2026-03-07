from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv('search_api_key')

app = Flask(__name__)

@app.route('/flight', methods=['POST'])

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
         "api_key": search_api_key
     }

     response = requests.get(url, params=params)
     results = response.json()

     return jsonify(results)
