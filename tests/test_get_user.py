import pytest
import boto3
import os
from moto import mock_aws
from decimal import Decimal
from index import handler

@pytest.fixture
def setup_dynamodb():
    with mock_aws():
        ddb = boto3.resource('dynamodb', region_name='eu-west-1')

        users_table = ddb.create_table(
            TableName='users',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )

        addresses_table = ddb.create_table(
            TableName='asdresses',
            KeySchema=[{'AttributeName': 'address_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'address_id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[{
                'IndexName': 'user_ids',
                'KeySchema': [{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'}
            }],
            BillingMode='PAY_PER_REQUEST'
        )

        users_table.put_item(Item={
            'id': 'user-123',
            'email': 'test@example.com',
            'firstName': 'John',
            'lastName': 'Doe',
            'size': Decimal(180)
        })

        addresses_table.put_item(Item={
            'address_id': 'addr-1',
            'user_id': 'user-123',
            'street': '123 Rue Test',
            'city': 'Paris',
            'zipCode': '75001',
            'country': 'France'
        })

        os.environ['STORAGE_USERS_NAME'] = 'users'
        os.environ['STORAGE_ADDRESSES_NAME'] = 'asdresses'

        yield  # ⬅️ important pour exécuter le bloc avant les tests

def test_get_user_success(setup_dynamodb):
    event = {
        "requestContext": {
            "identity": {
                "cognitoAuthenticationProvider": "cognito-idp.eu-west-1.amazonaws.com/eu-west-1_123,cognito-idp.eu-west-1.amazonaws.com/eu-west-1_123:CognitoSignIn:user-123"
            }
        }
    }

    response = handler(event, None)
    body = eval(response["body"])

    assert response["statusCode"] == 200
    assert body["email"] == "test@example.com"
    assert len(body["addresses"]) == 1
    assert body["addresses"][0]["city"] == "Paris"
