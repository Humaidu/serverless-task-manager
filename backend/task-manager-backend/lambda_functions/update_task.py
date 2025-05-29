import json
import traceback
from shared.dynamodb import update_task_in_db

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))  # Log raw event

        body = json.loads(event["body"])
        task_id = body.get("task_id")
        title = body.get("title")
        description = body.get("description")
        status = body.get("status")

        if not task_id:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
                "body": json.dumps({"message": "Missing task_id"})
            }

        updated_fields = {}
        if title: updated_fields["title"] = title
        if description: updated_fields["description"] = description
        if status: updated_fields["status"] = status
        
        print(f"Updating task_id={task_id} with fields={updated_fields}")
        
        # Call the DB update
        update_task_in_db(task_id, updated_fields)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({"message": "Task updated"})
        }

    except Exception as e:
        print("Exception occurred:", str(e))
        traceback.print_exc()  # Shows the full error in CloudWatch
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({"message": str(e)})
        }
