from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Helper functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d ** length for d in digits) == n

def digit_sum(n):
    return sum(int(d) for d in str(n))

def get_fun_fact(n):
    if is_armstrong(n):
        digits = [int(d) for d in str(n)]
        length = len(digits)
        armstrong_expression = " + ".join(f"{d}^{length}" for d in digits)
        return f"{n} is an Armstrong number because {armstrong_expression} = {n}"
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json", timeout=5)
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available.")
    except requests.RequestException:
        return "No fun fact available due to API error."
    return "No fun fact available."

# Root endpoint to prevent 404 error
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Number Classification API! Use /api/classify-number?number=<num> to classify a number."})

# API Endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')
    if not number_str or not number_str.lstrip('-').isdigit():
        return jsonify({
            "error": "Invalid input. Please provide a valid integer.",
            "number": number_str
        }), 400
    
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
