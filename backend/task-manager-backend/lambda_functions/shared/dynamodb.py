import boto3
from boto3.dynamodb.conditions import Key

# Initialize a connection to the DynamoDB service
dynamodb = boto3.resource('dynamodb')

# Reference the DynamoDB table named 'TasksTable'
table = dynamodb.Table('TasksTable') 

# Function to create a new task by inserting a new item into the table
def create_task(task):
    """
    Adds a new task to the DynamoDB table.
    `task` should be a dictionary with keys like 'task_id', 'title', etc.
    """
    table.put_item(Item=task)

# Function to assign a task to a user
def assign_task(task_id, assigned_to):
    """
    Updates the 'assigned_to' field of a task with the given `task_id`.
    """
    table.update_item(
        Key={'task_id': task_id},  # Primary key to identify the item
        UpdateExpression="set assigned_to=:a",  # Update expression
        ExpressionAttributeValues={':a': assigned_to}  # Value to set
    )

# Function to update the status of a task (e.g., from 'todo' to 'done')
def update_task_status(task_id, new_status):
    """
    Updates the 'status' of the task.
    'status' is a reserved keyword, so we alias it using ExpressionAttributeNames.
    """
    table.update_item(
        Key={'task_id': task_id},
        UpdateExpression="set #s=:s",  # #s is an alias for 'status'
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':s': new_status}
    )

# Function to retrieve all tasks assigned to a particular user
def get_tasks_by_user(assigned_to):
    """
    Retrieves tasks assigned to a specific user using scan and filter.
    Note: This performs a table scan and can be expensive on large datasets.
    """
    response = table.scan(
        FilterExpression=Key('assigned_to').eq(assigned_to)
    )
    return response.get('Items', [])

# Function to retrieve all tasks in the table
def get_all_tasks():
    """
    Retrieves all tasks from the table.
    Use with caution for large tables, as scan reads every item.
    """
    response = table.scan()
    return response.get('Items', [])

# Function to retrieve a specific task by its ID
def get_task(task_id):
    """
    Fetches a single task by its primary key (task_id).
    """
    response = table.get_item(Key={'task_id': task_id})
    return response.get('Item')

# Function to update multiple fields of a task at once
def update_task_in_db(task_id, updates):
    """
    Dynamically updates multiple fields of a task.
    Handles special cases like 'status' which is a reserved keyword.
    
    Parameters:
        task_id (str): The unique ID of the task to update.
        updates (dict): A dictionary of fields to update, e.g. {'title': 'New title', 'status': 'done'}
    """
    update_expression_parts = []   # Holds pieces of the SET expression
    expression_values = {}         # Holds placeholder-value pairs for ExpressionAttributeValues
    expression_names = {}          # Used to rename reserved keywords

    for k, v in updates.items():
        placeholder = f"#{k}" if k == "status" else k  # Alias reserved keyword
        value_key = f":{k}"                            # Placeholder for value
        update_expression_parts.append(f"{placeholder} = {value_key}")
        expression_values[value_key] = v
        if k == "status":
            expression_names["#status"] = "status"

    # Construct the full update expression
    update_expression = "SET " + ", ".join(update_expression_parts)

    update_kwargs = {
        "Key": {"task_id": task_id},
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_values,
    }

    # Include ExpressionAttributeNames if needed
    if expression_names:
        update_kwargs["ExpressionAttributeNames"] = expression_names

    table.update_item(**update_kwargs)

# Function to delete a task by ID
def delete_task_from_db(task_id):
    """
    Deletes the task with the given task_id from the table.
    """
    table.delete_item(Key={"task_id": task_id})
