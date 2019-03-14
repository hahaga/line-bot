<<<<<<< HEAD
import boto3
import json
import decimal
import uuid
from flask import Flask
=======
from flask import Flask, jsonify, request
from flask_cors import CORS

DEBUG = True
>>>>>>> master

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

# Helper class to convert DynamoDB item to JSON
# cuz like fuck dealing with it when it's not JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
            return super(DecimalEncoder, self).default(o)

def createItem():
    # Connect to database
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    # Connect to databse table
    table = dynamodb.Table('FortuneCookie')

    # Make JSON file of fortunes you want to add
    # rawrawrawr stuff
    id = str(uuid.uuid4())
    fortune = "If you eat food, it will give you calories."
    author = "Master Hong"

    response = table.put_item(
        Item={
            #   NEVERMIND I DON'T NEED YOU
            'id' : id,
            'fortune' : fortune,
            'author' : author
        }
    )

@app.route("/")
def home():
    return "Hello, World!"


@app.route("/test")
def test_endpoint():
    createItem()
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
<<<<<<< HEAD
    #app.run(debug=True, host='0.0.0.0', port='8081')
    createItem()
=======
    app.run(debug=True, port="8081")
>>>>>>> master
