from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # allow Godot Web Export to call this API

def scrape_kahoot(quiz_id: str):
    # Kahoot's public REST endpoint
    url = f"https://kahoot.it/rest/kahoots/{quiz_id}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch quiz: {response.status_code}")

    return response.json()

@app.route("/scrape", methods=["GET"])
def scrape():
    quiz_id = request.args.get("quiz_id")

    if not quiz_id:
        return jsonify({"error": "Missing quiz_id"}), 400

    try:
        data = scrape_kahoot(quiz_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Kahoot Scraper API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
