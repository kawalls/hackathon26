from flask import request, jsonify, Blueprint
import requests
import os
from dotenv import load_dotenv
from airports import airport_lookup

load_dotenv()

api_key = os.getenv('search_api_key')

flight_bluePrint = Blueprint('flight', __name__)

@flight_bluePrint.route('/flight', methods=['POST'])
def search_flights():

    print("\n===== NEW FLIGHT REQUEST =====")

    data = request.json
    print("Incoming request data:", data)

    departure = data["departure"].lower()
    arrival = data["arrival"].lower()

    outbound_date = data["outbound_date"]
    return_date = data["return_date"]

    # Convert ISO timestamps → YYYY-MM-DD
    outbound_date = outbound_date[:10]
    return_date = return_date[:10]

    print("User entered departure:", departure)
    print("User entered arrival:", arrival)

    # Convert city → airport code
    if departure in airport_lookup:
        departure_code = ",".join(airport_lookup[departure][:2])
    else:
        departure_code = departure.upper()

    if arrival in airport_lookup:
        arrival_code = ",".join(airport_lookup[arrival][:2])
    else:
        arrival_code = arrival.upper()

    print("Converted departure code:", departure_code)
    print("Converted arrival code:", arrival_code)

    url = "https://www.searchapi.io/api/v1/search"

    params = {
        "engine": "google_flights",
        "flight_type": "round_trip",
        "departure_id": departure_code,
        "arrival_id": arrival_code,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "api_key": api_key
    }

    print("API Request Params:", params)

    response = requests.get(url, params=params)
    results = response.json()

    print("API Response Keys:", results.keys())

    # Combine both flight groups
    best = results.get("best_flights", [])
    other = results.get("other_flights", [])

    all_flights = best + other

    print("Total flights found:", len(all_flights))

    flightList = []

    for flight in all_flights:

        flights = flight.get("flights", [])
        if not flights:
            continue

        flightp1 = flights[0]
        flightp2 = flights[-1]

        flightList.append({
            "price": flight.get("price"),
            "total_duration": flight.get("total_duration"),
            "airline": flightp1.get("airline"),
            "airline_logo": flight.get("airline_logo"),
            "departure_airport": flightp1["departure_airport"].get("name"),
            "departure_time": flightp1["departure_airport"].get("time"),
            "arrival_airport": flightp2["arrival_airport"].get("name"),
            "arrival_time": flightp2["arrival_airport"].get("time"),
            "stops": len(flights) - 1,
            "travel_class": flightp1.get("travel_class"),
            "type": flight.get("type")
        })

    return jsonify(flightList)