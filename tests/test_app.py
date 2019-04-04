import pytest
import boto3
import uuid
import json
from moto import mock_dynamodb2
from src import app

app.app.config['TESTING'] = True

@pytest.fixture
def app_client():
    client = app.app.test_client()
    yield client


def test_foo():
    assert 1 == 1

def test_bar():
    assert 3 == 3

def test_home():
    assert app.home() == ('Hello, World!', 200)

def test_test():
    assert app.test_endpoint() == ('Test sent to debug log')

@pytest.fixture
def empty_dynamo():
    with mock_dynamodb2(): # creates the mock database
        dynamodb = boto3.client('dynamodb')

        # Intializing the database by setting up the database schema
        dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            TableName='FortuneCookie',
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 1
            }
        )

        # Creates an item in the database
        dynamodb.put_item(
            TableName="FortuneCookie",
            Item={
                "id" : {'S' : str(uuid.uuid4())},
                "fortune": {'S' : "Test fortune"},
                "author": {'S': "pytest"},
                "approved": {'BOOL':  False}
                }
        )
        yield
    
def test_get_all_fortunes(empty_dynamo):
    all_fortunes = app.get_all_fortunes()
    assert isinstance(all_fortunes, list)
    print(all_fortunes)

def test_createItem(empty_dynamo):
    fortune = {
        'fortune' : 'Create test fortune',
        'author' : 'Create author'
    }

    newItem = app.createItem(fortune)

    assert 'Create test fortune' == newItem['Attributes']['fortune']
    assert 'Create author' == newItem['Attributes']['author']

def test_delete_item(empty_dynamo):
    """
        test_delete_item will delete the one item in the mock database
        and check for an empty database
    """

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    items = response_obj['Items'][0]

    app.delete_fortune(items['id'])

    response_obj = table.scan()

    assert 0 == response_obj['Count']

def test_get_by_id(empty_dynamo):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    items = response_obj['Items'][0]

    response = app.get_by_id(items['id'])

    assert 'Test fortune' == response['fortune']
    assert 'pytest' == response['author']

def test_update_fortune(empty_dynamo):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    items = response_obj['Items'][0]

    response = app.update_fortune(items['id'])

    assert True == response['Attributes']['approved']

    response = app.update_fortune(items['id']) #checks for toggle

    assert False == response['Attributes']['approved']

def test_get_request(empty_dynamo, app_client):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    item = response_obj['Items'][0]

    response_obj = app_client.get("/fortune/{}".format(item['id']))
    data = json.loads(response_obj.data)
    assert item == data
