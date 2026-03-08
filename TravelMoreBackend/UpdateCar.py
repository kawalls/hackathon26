from flask import request, jsonify, Blueprint
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

api_key = os.getenv("serp_api_key")

car_rental_bluePrint = Blueprint("car_rental", __name__)

@car_rental_bluePrint.route("/car_rental", methods=["POST"])
def search_car_rentals():

    print("\n==============================")
    print("CAR RENTAL API HIT")
    print("==============================")

    data = request.get_json(silent=True)
    print("Incoming JSON:", data)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    destination = data.get("destination")
    check_in_date = data.get("check_in_date")
    check_out_date = data.get("check_out_date")
    passengers = data.get("passengers")

    if not destination or not check_in_date or not check_out_date or passengers is None:
        return jsonify({"error": "Missing required fields"}), 400

    # Convert ISO timestamps → YYYY-MM-DD
    check_in_date = check_in_date.split("T")[0]
    check_out_date = check_out_date.split("T")[0]

    print("Destination:", destination)
    print("Check-in:", check_in_date)
    print("Check-out:", check_out_date)
    print("Passengers:", passengers)

    # Determine vehicle category
    if passengers <= 2:
        category = "Economy or Compact Vehicle"
    elif passengers <= 4:
        category = "Standard or Sedan Vehicle"
    elif passengers <= 5:
        category = "Full Size or SUV Vehicle"
    else:
        category = "Minivan or Large SUV Vehicle"

    # Convert dates
    check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
    check_out = datetime.strptime(check_out_date, "%Y-%m-%d")

    day_count = (check_out - check_in).days
    if day_count <= 0:
        return jsonify({"error": "Invalid date range"}), 400

    # Car pricing model
    category_type_info = {
        "Economy or Compact Vehicle": {
            "daily_rate": 45,
            "example_cars": ["Toyota Corolla", "Honda Civic", "Hyundai Elantra"]
        },
        "Standard or Sedan Vehicle": {
            "daily_rate": 65,
            "example_cars": ["Toyota Camry", "Honda Accord", "Nissan Altima"]
        },
        "Full Size or SUV Vehicle": {
            "daily_rate": 85,
            "example_cars": ["Toyota RAV4", "Ford Explorer", "Jeep Grand Cherokee"]
        },
        "Minivan or Large SUV Vehicle": {
            "daily_rate": 110,
            "example_cars": ["Chrysler Pacifica", "Honda Odyssey", "Chevrolet Suburban"]
        }
    }

    price_info = category_type_info.get(category)
    daily_cost = price_info["daily_rate"]

    url = "https://serpapi.com/search"

    params = {
        "engine": "google_local",
        "q": f"{category} car rentals in {destination}",
        "hl": "en",
        "gl": "us",
        "api_key": api_key
    }

    print("SerpAPI params:", params)

    response = requests.get(url, params=params)
    results = response.json()

    print("SerpAPI keys:", results.keys())

    local_results = results.get("local_results", [])

    car_rental_list = []

    for car in local_results:
        car_rental_list.append({
            "title": car.get("title"),
            "category": category,
            "example_cars": price_info["example_cars"],
            "price_per_day": daily_cost,
            "total_price": round(daily_cost * day_count, 2),
            "company": car.get("title"),
            "rating": car.get("rating"),
            "address": car.get("address")
        })

    print("Returning car rentals:", len(car_rental_list))

    return jsonify(car_rental_list)