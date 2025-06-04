import boto3
import os
from dotenv import load_dotenv

load_dotenv()

USER_POOL_ID =  os.getenv("USER_POOL_ID")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")  # This will be the **temporary** password
GROUP_NAME = os.getenv("GROUP_NAME")

client = boto3.client('cognito-idp')

# 1. Create user with a temporary password
client.admin_create_user(
    UserPoolId=USER_POOL_ID,
    Username=USERNAME,
    TemporaryPassword=PASSWORD,
    UserAttributes=[{'Name': 'email', 'Value': USERNAME}],
    MessageAction='SUPPRESS',  # prevent email notification
    DesiredDeliveryMediums=[]  # optional: suppresses email delivery completely
)

# 2. Add user to group
client.admin_add_user_to_group(
    UserPoolId=USER_POOL_ID,
    Username=USERNAME,
    GroupName=GROUP_NAME
)

print(f"User {USERNAME} created with temporary password and added to {GROUP_NAME}.")
print(f"User {USERNAME} will be required to change password on first login.")

