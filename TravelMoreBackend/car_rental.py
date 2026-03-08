from flask import Flask, request, jsonify, Blueprint
import requests
import os
from dotenv import load_dotenv

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
     print(results.keys()) #used for trouble shootingggg
     print(results)
     #print(results["properties"][0])

     return jsonify(results) #commented out for newly added filtering code

