import os
import sys
import json
import boto3
import pytest
from moto import mock_dynamodb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
import function.userHandler.src.user_handler as userHandler

TABLE_NAME = "user-dev"

# Petite table DynamoDB factice pour nos tests
@pytest.fixture
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
        os.environ["USER_TABLE_NAME"] = TABLE_NAME
        yield table

# Si on fait un POST on attend une réponse 200
def test_user_handler_post(dynamodb_mock):
    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "id": "u999",
            "email": "post@example.com",
            "nom": "POST",
            "prenom": "Test"
        })
    }

    response = userHandler.handler(event, None)
    assert response["statusCode"] == 200

# Si on fait un GET on attend une réponse 200
def test_user_handler_get(dynamodb_mock):
    dynamodb_mock.put_item(Item={
        "id": "u456",
        "email": "found@example.com",
        "nom": "Nom",
        "prenom": "Prenom"
    })

    event = {
        "httpMethod": "GET",
        "queryStringParameters": {"id": "u456"}
    }

    response = userHandler.handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["email"] == "found@example.com"

# Si on fait un GET sans id on attend une réponse 400
def test_user_handler_get_missing_id(dynamodb_mock):

    event = {
        "httpMethod": "GET",
        "queryStringParameters": {}
    }

    response = userHandler.handler(event, None)
    assert response["statusCode"] == 400
    assert "Missing id" in response["body"]

# Si on fait un GET avec un id inconnu on attend un 404
def test_user_handler_get_not_found(dynamodb_mock):

    event = {
        "httpMethod": "GET",
        "queryStringParameters": {"id": "unknown"}
    }

    response = userHandler.handler(event, None)
    assert response["statusCode"] == 404
