from flask import Flask, request, jsonify, send_file
import os
from fetch_delhi_case import fetch_delhi_case_details
from database import init_db

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize DB on startup
init_db()

@app.route('/')
def index():
    return send_file(os.path.join(BASE_DIR, '..', 'frontend', 'index.html'))

@app.route('/fetch-delhi-case', methods=['POST'])
def fetch_case():
    data = request.get_json()
    if not all(k in data for k in ("caseType", "caseNumber", "caseYear")):
        return jsonify({"error": "Missing required fields"}), 400

    result = fetch_delhi_case_details(
        case_type=data["caseType"],
        case_number=data["caseNumber"],
        case_year=data["caseYear"]
    )
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
