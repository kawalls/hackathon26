from flask import Flask, jsonify
from scraper import get_page_title

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask + Selenium backend running"

@app.route("/scrape")
def scrape():
    title = get_page_title("https://example.com")
    return jsonify({"title": title})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
