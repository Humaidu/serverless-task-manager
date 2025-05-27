import json
from shared import dynamodb

def lambda_handler(event, context):
    try:
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        task_id = body.get("task_id")
        assigned_to = body.get("assigned_to")

        if not task_id or not assigned_to:
            return {
                "statusCode": 400,
                 "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                    "Access-Control-Allow-Methods": "POST,OPTIONS"
                },
                "body": json.dumps({"message": "Missing task_id or assigned_to"})
            }

        dynamodb.assign_task(task_id, assigned_to)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({"message": "Task assigned Successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500, 
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({"message": str(e)})
        }
