import json
from datetime import datetime
from shared.dynamodb import table  # Import DynamoDB table instance from shared module
import boto3

# Initialize the SNS client to send notifications
sns = boto3.client('sns')

def lambda_handler(event, context):
    """
    AWS Lambda function to send task due date reminders.

    This function scans all tasks in the DynamoDB table and identifies those that:
    - Have a due date within the next 24 hours (but not past due)
    - Are not marked as 'completed'

    For each such task, it sends a reminder using Amazon SNS.

    Returns:
        200 OK: JSON object with the number of reminders sent.
    """
    now = datetime.utcnow()  # Get the current UTC time
    response = table.scan()  # Scan the entire DynamoDB table (Note: Not recommended for large tables)
    messages = []  # Collect messages sent for logging or verification

    for task in response['Items']:
        # Parse the due_date field into a datetime object
        due_date = datetime.fromisoformat(task['due_date'])

        # Check if task is due in <= 1 day and not completed
        if 0 < (due_date - now).days <= 1 and task['status'] != 'completed':
            message = f"Reminder: Task '{task['title']}' is due soon!"

            # Send a notification via Amazon SNS
            # Replace 'YOUR_SNS_TOPIC_ARN' with a valid SNS topic ARN
            sns.publish(TopicArn='YOUR_SNS_TOPIC_ARN', Message=message)

            # Store message for confirmation
            messages.append(message)

    # Return HTTP response with CORS headers for frontend compatibility
    return {
        "statusCode": 200, 
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps({"reminders_sent": len(messages)})  # Include number of reminders sent in response
    }
