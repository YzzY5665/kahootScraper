from flask import Flask, request, jsonify
import threading
import time

# --- Kahoot scraper import (adjust to match the repo) ---
from kahoot_scrape import KahootClient


# --- Scraper function ---
def scrape_kahoot(quiz_id: str):
    client = KahootClient()
    data = client.scrape_quiz(quiz_id)  # adjust if needed
    return data


# --- Flask API ---
app = Flask(__name__)

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


@app.route("/", methods=["GET"])
def home():
    return "Kahoot Scraper API is running."


# --- Startup test scrape ---
def run_startup_test():
    # Delay to ensure server is fully started
    time.sleep(2)

    TEST_QUIZ_ID = "dd08e4c5-2800-47ed-8c1d-5d0f36a1ee76"

    print("\n--- Running startup test scrape ---")
    try:
        result = scrape_kahoot(TEST_QUIZ_ID)
        print("Startup scrape successful!")
        print(result)
    except Exception as e:
        print("Startup scrape FAILED:")
        print(str(e))
    print("--- End startup test ---\n")


# Run the test in a background thread so it doesn't block Flask
threading.Thread(target=run_startup_test, daemon=True).start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
