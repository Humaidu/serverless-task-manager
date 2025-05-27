import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TasksTable') 

def create_task(task):
    table.put_item(Item=task)

def assign_task(task_id, assigned_to):
    table.update_item(
        Key={'task_id': task_id},
        UpdateExpression="set assigned_to=:a",
        ExpressionAttributeValues={':a': assigned_to}
    )

def update_task_status(task_id, status):
    table.update_item(
        Key={'task_id': task_id},
        UpdateExpression="set #s=:s",
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':s': status}
    )

def get_tasks_by_user(assigned_to):
    response = table.scan(
        FilterExpression=Key('assigned_to').eq(assigned_to)
    )
    return response.get('Items', [])

def get_all_tasks():
    response = table.scan()
    return response.get('Items', [])
