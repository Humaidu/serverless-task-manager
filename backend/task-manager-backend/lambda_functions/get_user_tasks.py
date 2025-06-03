import json
from shared import dynamodb  # Import shared DynamoDB utility module

def lambda_handler(event, context):
    """
    AWS Lambda function to fetch tasks assigned to a specific user.

    This function expects a query string parameter `assigned_to`, typically the user's email.
    It queries the DynamoDB table to retrieve all tasks assigned to that email.

    Example request: GET /tasks/user?assigned_to=user@example.com

    Returns:
        200 OK: List of tasks assigned to the user.
        400 Bad Request: If the 'assigned_to' parameter is missing.
        500 Internal Server Error: For any unhandled exceptions.
    """
    try:
        # Get query parameters safely from the event (supports API Gateway proxy integration)
        params = event.get("queryStringParameters") or {}
        assigned_to = params.get("assigned_to")

        # Validate that the required query parameter is provided
        if not assigned_to:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # CORS header to allow frontend access
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "GET,OPTIONS"
                },
                "body": json.dumps({"message": "Missing assigned_to parameter"})  # Informative error
            }

        # Fetch all tasks assigned to the given user from DynamoDB
        tasks = dynamodb.get_tasks_by_user(assigned_to)

        # Return the tasks with appropriate CORS headers
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET,OPTIONS"
            },
            "body": json.dumps({"tasks": tasks})  # Wrap the response in a "tasks" key
        }

    except Exception as e:
        # Handle unexpected errors gracefully
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": str(e)})  # Return the exception message
        }
