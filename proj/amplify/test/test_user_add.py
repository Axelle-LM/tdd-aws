import os
import sys
import json
import boto3
import pytest
from moto import mock_dynamodb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
import function.add.src.add as add

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

# Si on fait un add_user on attend une réponse 200
def test_add_user_success(dynamodb_mock):
    user = {
        "id": "u123",
        "email": "add@example.com",
        "nom": "Add",
        "prenom": "Test"
    }

    response = add.add_user(user)
    assert response["statusCode"] == 200

    stored_item = dynamodb_mock.get_item(Key={"id": user["id"]})
    assert "Item" in stored_item
    assert stored_item["Item"]["email"] == user["email"]
