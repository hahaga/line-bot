import pytest
import boto3
import uuid
import json
from moto import mock_dynamodb2
from src import app # From package called src, import the app module

app.app.config['TESTING'] = True

@pytest.fixture
def app_client():
    # A client used for testing so you don't have to run a server 
    client = app.app.test_client() # From the app module, it calls the test_client() method from the Flask object app
    yield client


def test_home():
    assert app.home() == ('Hello, World!', 200)

def test_test():
    assert app.test_endpoint() == ('Test sent to debug log')

@pytest.fixture
def non_dynamo():
    with mock_dynamodb2(): # creates the mock database
        
        yield

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
        yield

@pytest.fixture
def mock_dynamo(empty_dynamo):
    dynamodb = boto3.client('dynamodb')

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
    
def test_get_all_fortunes(mock_dynamo):
    all_fortunes = app.get_all_fortunes()
    assert isinstance(all_fortunes, list)

def test_get_all_fortunes_error(non_dynamo):
    with pytest.raises(Exception) as einfo:
        all_fortunes = app.get_all_fortunes()
        assert str(einfo['Error']['Message']) == all_fortunes

def test_createItem(mock_dynamo):
    fortune = {
        'fortune' : 'Create test fortune',
        'author' : 'Create author'
    }

    newItem = app.createItem(fortune)

    assert 'Create test fortune' == newItem['Attributes']['fortune']
    assert 'Create author' == newItem['Attributes']['author']

def test_delete_item(mock_dynamo):
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

def test_delete_item_error(non_dynamo):
    with pytest.raises(Exception) as einfo:
        response = app.delete_fortune("nonexistent-id")
        assert str(einfo['Error']['Message']) == response

def test_get_by_id(mock_dynamo):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    items = response_obj['Items'][0]

    response = app.get_by_id(items['id'])

    assert 'Test fortune' == response['fortune']
    assert 'pytest' == response['author']

def test_update_fortune(mock_dynamo):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    items = response_obj['Items'][0]

    response = app.update_fortune(items['id'])

    assert True == response['Attributes']['approved']

    response = app.update_fortune(items['id']) #checks for toggle

    assert False == response['Attributes']['approved']

def test_handle_id_get(mock_dynamo, app_client):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    item = response_obj['Items'][0]

    response_obj = app_client.get("/fortune/{}".format(item['id']))
    data = json.loads(response_obj.data)
    assert item == data

def test_handle_id_delete(mock_dynamo, app_client):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    item = response_obj['Items'][0]

    response_obj = app_client.delete("/fortune/{}".format(item['id']))

    response_obj = table.scan()

    assert 0 == response_obj['Count']


def test_handle_id_update(mock_dynamo, app_client):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    item = response_obj['Items'][0]

    response_obj = app_client.put("/fortune/{}".format(item['id']))

    data = json.loads(response_obj.data)

    assert True == data['Attributes']['approved']

    response_obj = app_client.put("/fortune/{}".format(item['id'])) #checks for toggle

    data = json.loads(response_obj.data)

    assert False == data['Attributes']['approved']

def test_fortune_get(mock_dynamo, app_client):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FortuneCookie')

    response_obj = table.scan()
    item = response_obj['Items'][0]

    response_obj = app_client.get("/fortune")
    data = json.loads(response_obj.data)

    assert item == data['fortune']

def test_fortune_post(mock_dynamo, app_client):
    fortune = {
        'fortune' : 'Create test fortune',
        'author' : 'Create author'
    }

    response_obj = app_client.post("/fortune", data=json.dumps(fortune), content_type='application/json')

    data = json.loads(response_obj.data)
    print(data)

    assert 'Create test fortune' == data['Attributes']['fortune']
    assert 'Create author' == data['Attributes']['author']
    

def test_fortune_all(mock_dynamo, app_client):
    response_obj = app_client.get("/fortune/all")
    data = json.loads(response_obj.data)
    assert isinstance(data, list)
