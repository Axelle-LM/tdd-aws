import boto3
import os

def add_user(user):
    dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
    table = dynamodb.Table(os.environ["USER_TABLE_NAME"])
    table.put_item(Item=user)
    return {"statusCode": 200}
