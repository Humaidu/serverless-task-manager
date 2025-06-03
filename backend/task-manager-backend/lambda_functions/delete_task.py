import json
from shared.dynamodb import delete_task_from_db  # Import the function that deletes a task from DynamoDB

def lambda_handler(event, context):
    """
    AWS Lambda function to delete a task from the task management system using its task_id.

    Expected input:
    - task_id passed as a query string parameter (e.g., ?task_id=1234-abcd)

    Returns:
        JSON response indicating success or error, with appropriate HTTP status code.
    """
    try:
        # Extract task_id from query string parameters
        task_id = event["queryStringParameters"].get("task_id")

        # If task_id is missing, return a 400 Bad Request response
        if not task_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing task_id"})
            }

        # Call the helper function to delete the task from the DynamoDB database
        delete_task_from_db(task_id)

        # If deletion is successful, return a 200 OK response with CORS headers
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow requests from any domain
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "DELETE,OPTIONS"
            },
            "body": json.dumps({"message": "Task deleted"})
        }

    except Exception as e:
        # Catch any unexpected exceptions and return a 500 Internal Server Error response
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
