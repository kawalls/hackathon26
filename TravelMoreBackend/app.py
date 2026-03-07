from flask import Flask, jsonify
from dotenv import load_dotenv
from flights2 import flight_bluePrint

load_dotenv()

app = Flask(__name__)
app.register_blueprint(flight_bluePrint)

@app.route("/")
def home():
    return "Flask + Selenium backend running"




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

