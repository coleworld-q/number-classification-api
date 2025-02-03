# Number Classification API

This API classifies a given number based on its mathematical properties and provides a fun fact using the Numbers API.

## Project Overview

The **Number Classification API** allows users to input a number and get the following details:

- Whether the number is prime or perfect
- Properties such as whether it's an Armstrong number, even, or odd
- The sum of the digits of the number
- A fun fact related to the number

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   ```

2. **Navigate to the project directory**:
   ```bash
   cd number-classification-api
   ```

3. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

4. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Once you have the project set up, you can start the API server using Flask:

```bash
python app.py
```

By default, the API will run on `http://127.0.0.1:5000/`.

## Usage

To classify a number, send a GET request to the following URL:

```
http://127.0.0.1:5000/api/classify-number?number=371
```

### Example Response:

For the input `371`, the response will be:

```json
{
  "number": 371,
  "is_prime": false,
  "is_perfect": false,
  "properties": ["armstrong", "odd"],
  "digit_sum": 11,
  "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

### Error Handling

If an invalid input is provided (e.g., a string instead of a number), the response will be:

```json
{
  "number": "abc",
  "error": true
}
```

## Functions Implemented

The API performs the following checks:

1. **Prime Check**: Determines if the number is prime.
2. **Perfect Check**: Determines if the number is a perfect number.
3. **Armstrong Check**: Checks if the number is an Armstrong number.
4. **Digit Sum**: Calculates the sum of the digits of the number.
5. **Fun Fact**: Fetches a fun fact related to the number from the Numbers API.

## Future Improvements

- Add support for additional mathematical properties (e.g., Fibonacci, triangular numbers).
- Implement more advanced error handling and input validation.
- Add caching to reduce the load on the Numbers API.
- Provide options for users to request a fun fact from specific categories (e.g., history, trivia).

## License

This project is open-source and licensed under the MIT License.

## Contributing

Feel free to fork the repository, submit issues, or send pull requests for improvements or bug fixes.

---



