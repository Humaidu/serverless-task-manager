import json
import uuid
import datetime
from shared import dynamodb

def lambda_handler(event, context):
    try:
        # Parse input
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        # Validate input
        title = body.get("title")
        description = body.get("description")
        deadline = body.get("deadline")

        if not all([title, description, deadline]):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing required fields"})
            }

        task_id = str(uuid.uuid4())
        created_at = datetime.datetime.utcnow().isoformat()

        task = {
            "task_id": task_id,
            "title": title,
            "description": description,
            "status": "pending",
            "created_at": created_at,
            "deadline": deadline,
            "assigned_to": ""
        }

        dynamodb.create_task(task)

        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": json.dumps({ "message": "Task created Succesfully", "task": task })
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
