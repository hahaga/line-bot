import pytest
import boto3
import uuid
from moto import mock_dynamodb2
from src import app

def test_foo():
    assert 1 == 1

def test_bar():
    assert 3 == 3

def test_home():
    assert app.home() == ('Hello, World!', 200)

@pytest.fixture
def empty_dynamo():
    with mock_dynamodb2():
        dynamodb = boto3.client('dynamodb')
        table = dynamodb.create_table(
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
    # Create mock dynamodb table
    all_fortunes = app.get_all_fortunes()
    print(all_fortunes)