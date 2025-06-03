import json
from shared import dynamodb  # Import the shared module to interact with DynamoDB

def lambda_handler(event, context):
    """
    AWS Lambda function to retrieve all tasks from the DynamoDB table.

    This function is typically used by admins to view the full list of tasks in the system.

    Returns:
        A JSON response with a list of tasks and a 200 HTTP status code if successful,
        or an error message with a 500 status code if something goes wrong.
    """
    try:
        # Fetch all tasks from DynamoDB using a helper function
        tasks = dynamodb.get_all_tasks()

        # Log the fetched tasks to CloudWatch for debugging
        print("Fetched tasks:", tasks)

        # Return the list of tasks in a successful HTTP response, along with CORS headers
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow access from all domains (CORS)
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps({"tasks": tasks})  # JSON-encode the list of tasks
        }

    except Exception as e:
        # Catch unexpected errors and return a 500 Internal Server Error with the error message
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
