import boto3
import json
import decimal
import uuid
import random
import sys
from loguru import logger
from flask import Flask, jsonify, request
from flask_cors import CORS
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")

# Helper class to convert DynamoDB item to JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, o): # pylint: disable=E0202
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
            return super(DecimalEncoder, self).default(o)

# Helper functions
def get_all_fortunes():
    """
        Returns all fortunes
    """

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('FortuneCookie')

    try:
        response_obj = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        items = response_obj['Items']
        return items

def delete_fortune(fortune_id):
    """
        Deletes a fortune from the database given an id
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('FortuneCookie')

    try:
        response = table.delete_item(
            Key={
                'id' : fortune_id
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        logger.debug("DeleteItem succeeded")
        logger.debug(json.dumps(response, indent=4))
        logger.debug(json.dumps(get_all_fortunes(), indent=4))
        return response

def createItem(fortune_item):
    """
        Adds a fortune to the database given the fortune and author
    """
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('FortuneCookie')

    response = table.put_item(
        Item={
            "id" : str(uuid.uuid4()),
            "fortune": fortune_item['fortune'],
            "author": fortune_item['author'],
            "approved": False
        }
    )
    logger.debug("Item inserted to database.")
    return response

def get_by_id(fortune_id):
    """
        Returns a fortune given an id
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('FortuneCookie')

    try:
        fortune = table.get_item(
            Key={
                "id" : fortune_id
            }
        )
    except ClientError as e:
        logger.debug(e.response['Error']['Message'])
    else:
        logger.debug("Get item by ID succeeded")
        logger.debug(json.dumps(fortune, indent=4))
        return fortune['Item']

def update_fortune(fortune_id):
    """
        Toggles the approved item of a fortune given the fortune id
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('FortuneCookie')

    fortune = get_by_id(fortune_id)

    logger.debug(f"Approved: {fortune['approved']}")
    if fortune['approved'] == True:
        response = table.update_item(
            Key={
                "id" : fortune_id
            },
            UpdateExpression="set approved = :a",
            ExpressionAttributeValues={
                 ':a': False
            },
            ReturnValues="UPDATED_NEW"
        )
    else:
        response = table.update_item(
            Key={
                "id" : fortune_id
            },
            UpdateExpression="set approved = :a",
            ExpressionAttributeValues={
                ':a': True
            },
            ReturnValues="UPDATED_NEW"
        )
    logger.debug("Update succeeded")
    logger.debug(json.dumps(get_all_fortunes(), indent=4))
    return response

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/test")
def test_endpoint():
    return "Test sent to debug log"

@app.route("/fortune/<_id>", methods=["PUT", "DELETE", "GET"])
def handle_id(_id):
    logger.debug(f"Calling handle_id on id: {_id}")
    response_obj = "Error"

    if request.method == "PUT":
        response_obj = update_fortune(_id)

    if request.method == "DELETE":
        response_obj = delete_fortune(_id)

    if request.method == "GET":
        response_obj = get_by_id(_id)

    logger.debug(json.dumps(response_obj, indent=4))
    return jsonify(response_obj)

@app.route("/fortune", methods=["GET", "POST"])
def fortune(): 
    response_obj = "Error"

    if request.method == "GET":
        fortunes = get_all_fortunes()
        response_obj = {
            "fortune" : random.choice(fortunes),
            "status": "success" 
        }

    if request.method == "POST":
        response_obj = createItem(request.json)

    logger.debug(json.dumps(response_obj, indent=4))
    return jsonify(response_obj)
    
@app.route("/fortune/all", methods=["GET"])
def fortune_all():
    fortunes = get_all_fortunes()
    logger.debug(json.dumps(fortunes, indent=4))
    return jsonify(fortunes)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8081')