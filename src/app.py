from flask import Flask, jsonify, request
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

@app.route("/")
def home():
    return "Hello, World!"


@app.route("/test")
def test_endpoint():
    return "This is only a test"


FORTUNES = [
    {
        "id": 0,
        "fortune": "A friend asks only for your time not your money.",
        "author": "Random",
        "approved": True,
    },
    {
        "id": 1,
        "fortune": "Your high-minded principles spell success.",
        "author": "Random Fool",
        "approved": False,
    },
]


@app.route("/fortune", methods=["GET"])
def get_fortune():
    response_obj = {"status": "success"}
    response_obj['fortunes'] = FORTUNES
    return jsonify(response_obj)


if __name__ == "__main__":
    app.run(debug=True, port="8081")
