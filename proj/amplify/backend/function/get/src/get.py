import boto3
import os
import json

def get_user(user_id):
    dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
    table = dynamodb.Table(os.environ["USER_TABLE_NAME"])
    response = table.get_item(Key={"id": user_id})

    if "Item" in response:
        return {
            "statusCode": 200,
            "body": json.dumps(response["Item"])
        }

    return { "statusCode": 404, "body": json.dumps({"error": "User not found"}) }
