import json
from shared import dynamodb  # Custom module to interact with DynamoDB

def lambda_handler(event, context):
    """
    AWS Lambda function to assign a task to a specific user.

    This function expects the incoming event to contain a JSON body with:
    - 'task_id': the unique identifier of the task
    - 'assigned_to': the user ID or email to whom the task is assigned

    It uses a helper function `assign_task` from the `dynamodb` module to update the assignment.

    Returns:
        A JSON response indicating success or failure, along with appropriate HTTP status codes and CORS headers.
    """
    try:
        # Parse the request body from the event
        # This handles both direct calls (like testing locally) and API Gateway events
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        # Extract the task ID and the user it should be assigned to
        task_id = body.get("task_id")
        assigned_to = body.get("assigned_to")

        # Return an error response if required fields are missing
        if not task_id or not assigned_to:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # CORS header
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                    "Access-Control-Allow-Methods": "POST,OPTIONS"
                },
                "body": json.dumps({"message": "Missing task_id or assigned_to"})
            }

        # Call the helper function to assign the task in DynamoDB
        dynamodb.assign_task(task_id, assigned_to)

        # Return a success response with CORS headers
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
        # Return a generic error response with the exception message
        return {
            "statusCode": 500, 
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({"message": str(e)})
        }
