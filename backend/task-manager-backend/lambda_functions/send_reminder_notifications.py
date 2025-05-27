import json
from datetime import datetime
from shared.dynamodb import table
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    now = datetime.utcnow()
    response = table.scan()
    messages = []

    for task in response['Items']:
        due_date = datetime.fromisoformat(task['due_date'])
        if 0 < (due_date - now).days <= 1 and task['status'] != 'completed':
            message = f"Reminder: Task '{task['title']}' is due soon!"
            # Replace with actual phone/email if available
            sns.publish(TopicArn='YOUR_SNS_TOPIC_ARN', Message=message)
            messages.append(message)

    return {
        "statusCode": 200, 
        "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
        "body": json.dumps({"reminders_sent": len(messages)})
        
    }
