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

def update_task_status(task_id, new_status):
    table.update_item(
        Key={'task_id': task_id},
        UpdateExpression="set #s=:s",
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':s': new_status}
    )

def get_tasks_by_user(assigned_to):
    response = table.scan(
        FilterExpression=Key('assigned_to').eq(assigned_to)
    )
    return response.get('Items', [])

def get_all_tasks():
    response = table.scan()
    return response.get('Items', [])


def get_task(task_id):
    response = table.get_item(Key={'task_id': task_id})
    return response.get('Item')

def update_task_in_db(task_id, updates):
    update_expression_parts = []
    expression_values = {}
    expression_names = {}

    for k, v in updates.items():
        placeholder = f"#{k}" if k == "status" else k
        value_key = f":{k}"
        update_expression_parts.append(f"{placeholder} = {value_key}")
        expression_values[value_key] = v
        if k == "status":
            expression_names["#status"] = "status"

    update_expression = "SET " + ", ".join(update_expression_parts)

    update_kwargs = {
        "Key": {"task_id": task_id},
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_values,
    }

    if expression_names:
        update_kwargs["ExpressionAttributeNames"] = expression_names

    table.update_item(**update_kwargs)

def delete_task_from_db(task_id):
    table.delete_item(Key={"task_id": task_id})
