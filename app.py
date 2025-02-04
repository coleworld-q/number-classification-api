from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Helper functions
def is_prime(n):
    """Check if a number is prime. Only valid for integers."""
    if n < 2 or n % 1 != 0:  # Exclude non-integers
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is a perfect number. Only valid for integers."""
    if n < 2 or n % 1 != 0:  # Exclude non-integers
        return False
    return sum(i for i in range(1, int(n)) if n % i == 0) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number. Only valid for integers."""
    if n % 1 != 0:  # Exclude non-integers
        return False
    digits = [int(d) for d in str(int(n))]
    length = len(digits)
    return sum(d ** length for d in digits) == int(n)

def digit_sum(n):
    """Calculate the sum of digits of a number (only for integers)."""
    if n % 1 != 0:  # Exclude non-integers
        return None
    return sum(int(d) for d in str(int(n)))

def get_fun_fact(n):
    """Get a fun fact about a number. If it's an Armstrong number, generate a custom fact."""
    if n % 1 != 0:  # Only request fun facts for integers
        return "Fun facts are only available for integers."

    if is_armstrong(n):
        digits = [int(d) for d in str(int(n))]
        length = len(digits)
        armstrong_expression = " + ".join(f"{d}^{length}" for d in digits)
        return f"{int(n)} is an Armstrong number because {armstrong_expression} = {int(n)}"
    
    # Fetch from Numbers API for other numbers
    try:
        response = requests.get(f"http://numbersapi.com/{int(n)}/math?json", timeout=5)
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available.")
    except requests.RequestException:
        return "No fun fact available due to API error."

    return "No fun fact available."

# Root Endpoint - Now returns JSON instead of 404
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Number Classification API!",
        "usage": "Use /api/classify-number?number=<number> to classify a number."
    }), 200

# API Endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """Classify a number and return its mathematical properties."""
    number_str = request.args.get('number')
    
    # Validate input
    try:
        number = float(number_str)  # Support integers & floating points
    except (TypeError, ValueError):
        return jsonify({
            "error": True,
            "message": "Invalid input. Please provide a valid number.",
            "number": number_str
        }), 400

    properties = ["even" if number % 2 == 0 else "odd"] if number % 1 == 0 else ["floating-point"]

    if is_armstrong(number):
        properties.append("armstrong")

    response = {
        "error": False,
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),  # None for floats
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response), 200

# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Render provides a dynamic port
    app.run(host='0.0.0.0', port=port, debug=True)
