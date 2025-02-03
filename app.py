from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Helper functions
def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is a perfect number."""
    if n < 2:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d ** length for d in digits) == n

def digit_sum(n):
    """Calculate the sum of digits of a number."""
    return sum(int(d) for d in str(n))

def get_fun_fact(n):
    """Get a fun fact about a number. If it's an Armstrong number, generate a custom fact."""
    if is_armstrong(n):
        digits = [int(d) for d in str(n)]
        length = len(digits)
        armstrong_expression = " + ".join(f"{d}^{length}" for d in digits)
        return f"{n} is an Armstrong number because {armstrong_expression} = {n}"
    
    # Fetch from Numbers API for other numbers
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json", timeout=5)
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available.")
    except requests.RequestException:
        return "No fun fact available due to API error."

    return "No fun fact available."

# API Endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """Classify a number and return its mathematical properties."""
    number_str = request.args.get('number')
    
    # Validate input
    if not number_str or not number_str.lstrip('-').isdigit():
        return jsonify({"error": "Invalid input. Please provide a valid integer."}), 400

    number = int(number_str)
    properties = ["even" if number % 2 == 0 else "odd"]
    
    if is_armstrong(number):
        properties.append("armstrong")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response), 200

# Welcome Page for root route
@app.route('/')
def welcome():
    return "Welcome to the Number Classification API! Use /api/classify-number?number=7 to test."

# Main entry point
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Render provides a dynamic port
    app.run(host='0.0.0.0', port=port, debug=True)
