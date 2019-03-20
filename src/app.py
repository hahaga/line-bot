import boto3
import json
import decimal
import uuid
import random
from flask import Flask, jsonify
from flask_cors import CORS
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

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
    createItem()
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

    ##########
    # BATTLE PLAN
    # - Put fortunes in a hash table so that they have 0-n indeces
    # - Random generate a number to pick a random fortune
    # - Return fortune 
    # 
    # BABY STEPS
    # x Print id of fortune (extract ids from list)
    # - Put fortunes in a hashtable and print first fortune
    # - Random generate a number and print fortune
    ##########

    chosen = random.randint(0, len(fortunes)-1)
    #print(f"{chosen} {fortunes[chosen]['id']}")
    print(fortunes[chosen])
    
    response_obj = {
        "fortune" : fortunes[chosen],
        "status": "success" 
    }
    print("got to here!")
    return jsonify(response_obj)




    #return jsonify(response_obj) this is for Dustin
    


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8081')

    # testing the methods
    # createItem()
    #get_fortune()
