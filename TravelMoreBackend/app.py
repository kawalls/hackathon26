from flask import Flask
from flask_cors import CORS  # Import CORS
from flights2 import flight_bluePrint
from hotel import hotel_bluePrint
from vacay_rental import vacay_rental_bluePrint
from UpdateCar import car_rental_bluePrint
from chatbot import claude_blueprint
app = Flask(__name__)
CORS(app) # Initialize CORS for the entire app

# register the flights blueprint
app.register_blueprint(flight_bluePrint)
app.register_blueprint(hotel_bluePrint)
app.register_blueprint(vacay_rental_bluePrint)
app.register_blueprint(car_rental_bluePrint)
app.register_blueprint(claude_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)