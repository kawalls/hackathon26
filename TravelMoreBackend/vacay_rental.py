from flask import request, jsonify, Blueprint
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("serp_api_key")

vacay_rental_bluePrint = Blueprint("vacay_rental", __name__)

@vacay_rental_bluePrint.route("/vacay_rental", methods=["POST"])
def search_vacay_rentals():

    print("\n==============================")
    print("VACAY RENTAL API HIT")
    print("==============================")

    # Raw request body
    print("Raw request data:", request.data)

    # Parse JSON safely
    data = request.get_json(silent=True)
    print("Parsed JSON:", data)

    if not data:
        print("ERROR: No JSON received")
        return jsonify({"error": "No JSON received"}), 400

    destination = data.get("destination")
    adults = data.get("adults")
    children = data.get("children")

    check_in_date = data.get("check_in_date")
    check_out_date = data.get("check_out_date")

    print("Destination:", destination)
    print("Adults:", adults)
    print("Children:", children)
    print("Check-in:", check_in_date)
    print("Check-out:", check_out_date)

    url = "https://serpapi.com/search"

    params = {
        "engine": "google_hotels",
        "q": f"vacation rentals in {destination}",
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "children": children,
        "api_key": api_key
    }

    print("\nSerpAPI params:", params)

    response = requests.get(url, params=params)

    print("HTTP Status:", response.status_code)

    try:
        results = response.json()
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        return jsonify({"error": "SerpAPI response not JSON"}), 500

    print("SerpAPI keys:", results.keys())

    if "error" in results:
        print("SERPAPI ERROR:", results["error"])

    properties = results.get("properties", [])
    print("Properties found:", len(properties))

    vacay_rental_list = []

    for hotel in properties:

        images = hotel.get("images", [])
        thumbnail = None
        if images:
            thumbnail = images[0].get("thumbnail")

        vacay_rental_list.append({
            "name": hotel.get("name"),
            "type": hotel.get("type"),
            "reviews": hotel.get("reviews"),
            "thumbnail": thumbnail,
            "overall_rating": hotel.get("overall_rating"),
            "rate_per_night": hotel.get("rate_per_night", {}).get("extracted_lowest"),
            "amenities": hotel.get("amenities"),
            "total_price": hotel.get("total_rate", {}).get("extracted_lowest")
        })

    print("Returning rentals:", len(vacay_rental_list))

    return jsonify(vacay_rental_list)