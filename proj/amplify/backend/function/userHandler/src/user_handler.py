import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'add', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'get', 'src')))
import json
from add import add_user
from get import get_user

def handler(event, context):
    if event.get("httpMethod") == "POST":
        user = json.loads(event.get("body", "{}"))
        return add_user(user)
    if event.get("httpMethod") == "GET":
        query_params = event.get("queryStringParameters") or {}
        user_id = query_params.get("id")

        if not user_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing id"})
            }

        return get_user(user_id)
    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Unsupported method"})
    }
