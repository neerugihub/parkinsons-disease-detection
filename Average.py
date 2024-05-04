from flask import Flask, jsonify, request
import requests
from collections import deque

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
TEST_SERVER_URL = "http://localhost:9876/numbers"
QUALIFIED_IDS = {'p': 'prime', 'f': 'fibonacci', 'e': 'even', 'r': 'random'}

# Circular buffer to store numbers
window_buffer = deque(maxlen=WINDOW_SIZE)

def fetch_numbers(qualified_id):
    url = f"{TEST_SERVER_URL}/{qualified_id}"
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        print(f"Error fetching numbers: {e}")
    return []

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

@app.route('/numbers')
def get_numbers():
    qualified_id = request.args.get('qualified_id')
    if qualified_id not in QUALIFIED_IDS:
        return jsonify({"error": "Invalid qualified ID"}), 400
    
    numbers = fetch_numbers(qualified_id)
    if not numbers:
        return jsonify({"error": "Failed to fetch numbers"}), 500

    # Add unique numbers to the window buffer
    for num in numbers:
        if num not in window_buffer:
            window_buffer.append(num)

    # Calculate average
    avg = calculate_average(window_buffer)

    response = {
        "numbers": numbers,
        "windowPrevState": list(window_buffer),
        "windowCurrState": list(window_buffer),
        "avg": round(avg, 2)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='localhost', port=9877)
