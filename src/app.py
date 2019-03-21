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
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
            return super(DecimalEncoder, self).default(o)

# Helper functions
def get_all_fortunes():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('FortuneCookie')

    try:
        response_obj = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        items = response_obj['Items']
        return items

def delete_fortune(id):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('FortuneCookie')

    try:
        response = table.delete_item(
            Key={
                'id' : id
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        logger.debug("DeleteItem succeeded")
        logger.debug(json.dumps(get_all_fortunes(), indent=4))

def createItem(fortune_item):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('FortuneCookie')

    id = str(uuid.uuid4())

    response = table.put_item(
        Item={
            "id" : id,
            "fortune": fortune_item['fortune'],
            "author": fortune_item['author'],
            "approved": False
        }
    )
    logger.debug("Item inserted to database.")
    logger.debug(json.dumps(get_all_fortunes(), indent=4))

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/test")
def test_endpoint():
    
    return "Test sent to debug log"

@app.route("/fortune", methods=["GET"])
def get_fortune():
    fortunes = get_all_fortunes()

    response_obj = {
        "fortune" : random.choice(fortunes),
        "status": "success" 
    }

    logger.debug("Random fortune: ")
    logger.debug(json.dumps(response_obj, indent=4))
    return jsonify(response_obj)
    
@app.route("/fortune/all", methods=["GET"])
def show_all():
    fortunes = get_all_fortunes()
    logger.debug(json.dumps(fortunes, indent=4))
    return jsonify(fortunes)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8081')
