from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEY = "5fdfc007cf785aee873ef79b812365c5"
BASE_URL = "http://api.exchangeratesapi.io/v1/"

@app.route('/')
def home():
    return "Currency Converter API is running!"

# Endpoint to fetch live exchange rates
@app.route('/api/convert', methods=['GET'])
def convert_currency():
    target = request.args.get('target', 'INR')
    amount = float(request.args.get('amount', 1))

    try:
        response = requests.get(f"{BASE_URL}/latest", params={"access_key": API_KEY, "symbols": target})
        data = response.json()

        if "rates" not in data:
            return jsonify({"error": "Failed to fetch live rates"}), 400

        target_rate = data["rates"].get(target)
        converted_amount = amount * target_rate

        return jsonify({
            "status": "success",
            "base": "EUR",
            "target": target,
            "amount": amount,
            "converted_amount": round(converted_amount, 2),
            "rate": target_rate
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch historical rates for the graph
@app.route('/api/historical', methods=['GET'])
def historical_data():
    target = request.args.get('target', 'INR')
    days = int(request.args.get('days', 30))  # Default to 30 days

    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)

        historical_rates = {}

        for day in range(days + 1):
            date = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
            response = requests.get(f"{BASE_URL}/{date}", params={"access_key": API_KEY, "symbols": target})
            data = response.json()

            if "rates" in data:
                historical_rates[date] = data["rates"].get(target)
            else:
                historical_rates[date] = None  # Handle missing data

        return jsonify(historical_rates)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8080)
