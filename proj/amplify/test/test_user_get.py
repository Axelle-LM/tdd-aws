import os
import sys
import json
import boto3
import pytest
from moto import mock_dynamodb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
import function.get.src.get as get

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

# Si l'utilisateur existe get_user doit renvoyer 200
def test_get_user_found(dynamodb_mock):
    dynamodb_mock.put_item(Item={
        "id": "u456",
        "email": "found@example.com",
        "nom": "Nom",
        "prenom": "Prenom"
    })

    response = get.get_user("u456")
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["email"] == "found@example.com"

# Si l'utilisateur n'existe pas get_user doit renvoyer 404
def test_get_user_not_found(dynamodb_mock):
    response = get.get_user("id_inexistant")
    assert response["statusCode"] == 404
