import json
from shared.dynamodb import delete_task_from_db

def lambda_handler(event, context):
    try:
        task_id = event["queryStringParameters"].get("task_id")

        if not task_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing task_id"})
            }

        delete_task_from_db(task_id)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "DELETE,OPTIONS"
            },
            "body": json.dumps({"message": "Task deleted"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
