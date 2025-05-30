import boto3
import os
from dotenv import load_dotenv

load_dotenv()

USER_POOL_ID =  os.getenv("USER_POOL_ID")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
GROUP_NAME = os.getenv("GROUP_NAME")

client = boto3.client('cognito-idp')

# 1. Create user
client.admin_create_user(
    UserPoolId=USER_POOL_ID,
    Username=USERNAME,
    TemporaryPassword=PASSWORD,
    UserAttributes=[{'Name': 'email', 'Value': USERNAME}],
    MessageAction='SUPPRESS'
)

# 2. Set permanent password
client.admin_set_user_password(
    UserPoolId=USER_POOL_ID,
    Username=USERNAME,
    Password=PASSWORD,
    Permanent=True
)

# 3. Add to group
client.admin_add_user_to_group(
    UserPoolId=USER_POOL_ID,
    Username=USERNAME,
    GroupName=GROUP_NAME
)

print(f"✅ User {USERNAME} created and added to {GROUP_NAME}.")
