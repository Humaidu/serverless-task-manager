import json
from shared import dynamodb

def lambda_handler(event, context):
    try:
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        assigned_to = body.get("assigned_to")
        if not assigned_to:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing 'assigned_to'"})
            }

        tasks = dynamodb.get_tasks_by_user(assigned_to)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps({"tasks": tasks})
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
