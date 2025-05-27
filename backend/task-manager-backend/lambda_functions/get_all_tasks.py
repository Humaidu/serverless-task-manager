import json
from shared import dynamodb

def lambda_handler(event, context):
    try:
        tasks = dynamodb.get_all_tasks()
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
