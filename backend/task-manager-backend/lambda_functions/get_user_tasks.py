import json
from shared import dynamodb

def lambda_handler(event, context):
    try:
        # Expecting a GET request with ?assigned_to=email
        params = event.get("queryStringParameters") or {}
        assigned_to = params.get("assigned_to")

        if not assigned_to:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "GET,OPTIONS"
                },
                "body": json.dumps({"message": "Missing assigned_to parameter"})
            }

        tasks = dynamodb.get_tasks_by_user(assigned_to)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET,OPTIONS"
            },
            "body": json.dumps({"tasks": tasks})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": str(e)})
        }
