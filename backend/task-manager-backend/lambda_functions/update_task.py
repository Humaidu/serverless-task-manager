import json
import traceback
from shared.dynamodb import update_task_in_db  # Import DynamoDB utility function

def lambda_handler(event, context):
    """
    Lambda function to update an existing task's attributes in DynamoDB.

    Expected input (in JSON body):
        - task_id (str): Required. The unique ID of the task to update.
        - title (str): Optional. New title for the task.
        - description (str): Optional. New description for the task.
        - status (str): Optional. New status for the task (e.g., 'pending', 'in progress', 'completed').

    Returns:
        - 200 OK on success
        - 400 Bad Request if task_id is missing
        - 500 Internal Server Error on exceptions
    """

    try:
        # Log the incoming event (useful for debugging in CloudWatch)
        print("Received event:", json.dumps(event))

        # Parse the JSON body from the event
        body = json.loads(event["body"])

        # Extract fields from the request
        task_id = body.get("task_id")
        title = body.get("title")
        description = body.get("description")
        status = body.get("status")

        # Validate required field
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

        # Build a dictionary of fields to be updated
        updated_fields = {}
        if title:
            updated_fields["title"] = title
        if description:
            updated_fields["description"] = description
        if status:
            updated_fields["status"] = status

        # Log the update operation
        print(f"Updating task_id={task_id} with fields={updated_fields}")
        
        # Call the shared DynamoDB update function
        update_task_in_db(task_id, updated_fields)

        # Return success response with CORS headers
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
        # Log full traceback to CloudWatch for debugging
        print("Exception occurred:", str(e))
        traceback.print_exc()

        # Return error response with details
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({"message": str(e)})
        }
