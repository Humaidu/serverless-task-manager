import json
from shared import dynamodb  # Import custom DynamoDB utility module

def lambda_handler(event, context):
    """
    Lambda function to update the status of a task in DynamoDB.

    This function expects a JSON payload containing:
    - task_id: The unique ID of the task
    - status: The new status to be assigned (e.g., "completed", "in progress")

    Returns:
        200 OK on success,
        400 Bad Request if required fields are missing,
        500 Internal Server Error if an exception occurs.
    """

    try:
        # Parse request body whether it comes from API Gateway or a direct invocation
        if "body" in event:
            body = json.loads(event["body"])  # When triggered by API Gateway
        else:
            body = event  # When invoked directly (e.g., during testing)

        # Extract required fields from request
        task_id = body.get("task_id")
        status = body.get("status")

        # Validate input
        if not task_id or not status:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing task_id or status"})
            }

        # Update task status using shared dynamodb utility
        dynamodb.update_task_status(task_id, status)

        # Return success response with proper CORS headers
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow frontend access
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps({"message": "Task status updated successfully"})
        }

    except Exception as e:
        # Return error message in case of unexpected failure
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
