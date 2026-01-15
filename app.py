from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from requests.exceptions import RequestException, Timeout

app = Flask(__name__)
CORS(app)  # allow browser / Godot Web Export access

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

KAHOOT_URL = "https://kahoot.it/rest/kahoots/{}"
REQUEST_TIMEOUT = 5  # seconds

# ---------------------------------------------------------------------------
# Kahoot scraping logic
# ---------------------------------------------------------------------------

def scrape_kahoot(quiz_id: str):
    try:
        response = requests.get(
            KAHOOT_URL.format(quiz_id),
            timeout=REQUEST_TIMEOUT
        )
    except Timeout:
        # Kahoot did not respond in time
        raise RuntimeError("Kahoot request timed out")
    except RequestException:
        # Network / DNS / TLS / etc
        raise RuntimeError("Failed to reach Kahoot")

    if response.status_code == 404:
        raise RuntimeError("Quiz not found")

    if response.status_code != 200:
        raise RuntimeError("Kahoot returned an error")

    return response.json()

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/scrape", methods=["GET"])
def scrape():
    quiz_id = request.args.get("quiz_id")

    # Validate input
    if not quiz_id:
        return jsonify({
            "error": "Missing quiz_id"
        }), 400

    if not quiz_id.isalnum():
        return jsonify({
            "error": "Invalid quiz_id"
        }), 400

    try:
        data = scrape_kahoot(quiz_id)
        return jsonify(data)

    except RuntimeError as e:
        # Controlled, user-safe errors
        return jsonify({
            "error": str(e)
        }), 502

    except Exception:
        # Catch-all safety net
        return jsonify({
            "error": "Internal server error"
        }), 500

@app.route("/")
def home():
    return "Kahoot Scraper API is running."

# ---------------------------------------------------------------------------
# Entry point (local dev only)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
