import boto3
import json
import decimal
import uuid
import random
import sys
from loguru import logger
from flask import Flask, jsonify
from flask_cors import CORS
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add("debug.log")


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

    # Access database table
    table = dynamodb.Table('FortuneCookie')

    # Make JSON file of fortunes you want to add
    # rawrawrawr stuff
    id = str(uuid.uuid4())
    # fortune = "If you eat food, it will give you calories."
    # author = "Master Hong"

    response = table.put_item(
        Item={
            'id' : id,
            "fortune": "Your high-minded principles spell success.",
            "author": "Random Fool",
            "approved": True
        }
    )

@app.route("/")
def home():
    return "Hello, World!"


@app.route("/test")
def test_endpoint():
    
    return "This is only a test"


# Test fortunes
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

# Helper function
def get_all_fortunes():
    # connect to the database
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    # Access database table
    table = dynamodb.Table('FortuneCookie')

    try:
        response_obj = table.scan()
    except ClientError as e:
        print("Failed...")
        print(e.response['Error']['Message'])
    else:
        items = response_obj['Items']
        return items
        # testing prints
        #print("GetItem succeeded: ")
        #print(json.dumps(item, indent=4, cls=DecimalEncoder))


@app.route("/fortune", methods=["GET"])
def get_fortune():
    fortunes = get_all_fortunes()

    # Choose a random fortune
    chosen = random.randint(0, len(fortunes)-1)
    print(fortunes[chosen])
    
    response_obj = {
        "fortune" : fortunes[chosen],
        "status": "success" 
    }

    logger.debug(json.dumps(response_obj, indent=4))
    return jsonify(response_obj)
    
@app.route("/fortune/all", methods=["GET"])
def show_all():
    fortunes = get_all_fortunes()
    return jsonify(fortunes)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8081')

    # testing the methods
    # createItem()
    # get_fortune()
