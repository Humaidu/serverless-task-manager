import json
from shared import dynamodb

def lambda_handler(event, context):
    try:
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        task_id = body.get("task_id")
        status = body.get("status")

        if not task_id or not status:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing task_id or status"})
            }

        dynamodb.update_task_status(task_id, status)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps({"message": "Task status updated succesfully"})
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
