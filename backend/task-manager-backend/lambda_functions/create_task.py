import json
import uuid
import datetime
from shared import dynamodb  # Import the shared module that handles DynamoDB operations

def lambda_handler(event, context):
    """
    AWS Lambda function to create a new task in the task management system.

    Expected input (in the event body):
    - title: Title of the task
    - description: Description of the task
    - deadline: ISO formatted deadline (e.g., "2025-06-15T23:59:59Z")

    The function generates a unique task ID, sets the initial status to "pending",
    records the creation timestamp, and initializes the task as unassigned.

    Returns:
        JSON response with status code and the created task data.
    """
    try:
        # Extract the request body (API Gateway might wrap it in a "body" key as a string)
        if "body" in event:
            body = json.loads(event["body"])  # Parse JSON string to dict
        else:
            body = event["body"]  # Use as-is for direct invocation (e.g., local test)

        # Retrieve required fields from request body
        title = body.get("title")
        description = body.get("description")
        deadline = body.get("deadline")

        # Validate presence of required fields
        if not all([title, description, deadline]):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing required fields"})  # Inform the client of the issue
            }

        # Generate a unique ID for the task
        task_id = str(uuid.uuid4())

        # Get current UTC timestamp for task creation time
        created_at = datetime.datetime.utcnow().isoformat()

        # Construct the task object to store in DynamoDB
        task = {
            "task_id": task_id,
            "title": title,
            "description": description,
            "status": "pending",         # Initial status of the task
            "created_at": created_at,    # Creation timestamp
            "deadline": deadline,        # User-provided deadline
            "assigned_to": ""            # Empty string means not yet assigned
        }

        # Store the task in DynamoDB using the shared module
        dynamodb.create_task(task)

        # Return a success response with CORS headers and the created task
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": json.dumps({
                "message": "Task created Successfully",
                "task": task
            })
        }

    except Exception as e:
        # Catch and return any unexpected error
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
