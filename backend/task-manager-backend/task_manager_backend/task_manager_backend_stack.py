from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_apigateway as apigw,
    aws_cognito as cognito,
    Duration,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct
import os

class TaskManagerBackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

         # Cognito User Pool
        user_pool = cognito.UserPool(
            self, "TaskUserPool",
            user_pool_name="TaskUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False,
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
        )
        
        # App Client (Frontend or API calls)
        app_client = user_pool.add_client(
            "TaskAppClient",
            auth_flows=cognito.AuthFlow(user_password=True),
            prevent_user_existence_errors=True
        )

        # Admin Group
        cognito.CfnUserPoolGroup(self, "AdminGroup",
            group_name="Admin",
            user_pool_id=user_pool.user_pool_id
        )

        # User Group
        cognito.CfnUserPoolGroup(self, "UserGroup",
            group_name="User",
            user_pool_id=user_pool.user_pool_id
        )
        
        # Expose values
        self.user_pool = user_pool
        self.app_client = app_client
        
        cognito_authorizer = apigw.CognitoUserPoolsAuthorizer(self,     "TaskCognitoAuthorizer", cognito_user_pools=[self.user_pool]
        )

        CfnOutput(self, "UserPoolId", value=user_pool.user_pool_id)
        CfnOutput(self, "AppClientId", value=app_client.user_pool_client_id)
        CfnOutput(self, "UserPoolRegion", value=self.region)

        # DynamoDB table
        tasks_table = ddb.Table(
            self, "TasksTable",
            table_name="TasksTable",
            partition_key=ddb.Attribute(name="task_id", type=ddb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
        )

        lambda_env = {
            "TABLE_NAME": tasks_table.table_name
        }

        lambda_path = "lambda_functions"

        function_names = [
            "create_task",
            "assign_task",
            "update_task_status",
            "get_user_tasks",
            "get_all_tasks",
            "update_task",
            "delete_task"
        ]

        lambda_functions = {}

        for fn_name in function_names:
            fn = _lambda.Function(
                self, f"{fn_name}_function",
                runtime=_lambda.Runtime.PYTHON_3_12,
                handler=f"{fn_name}.lambda_handler",
                code=_lambda.Code.from_asset(lambda_path),
                environment=lambda_env,
                timeout=Duration.seconds(10)
            )
            tasks_table.grant_read_write_data(fn)
            lambda_functions[fn_name] = fn

        # API Gateway
        api = apigw.RestApi(
            self, "TaskAPI", 
            rest_api_name="Task Manager Service",
            default_cors_preflight_options=apigw.CorsOptions(
            allow_origins=["*"],
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization"],
            allow_credentials=False
            )
        )

        # /tasks 
        tasks = api.root.add_resource("tasks")
        
         # /tasks POST
        tasks.add_method(
            "POST",
            apigw.LambdaIntegration(lambda_functions["create_task"]),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=cognito_authorizer 
        )

        # /tasks/all GET
        all_tasks = tasks.add_resource("all")
        all_tasks.add_method(
            "GET", 
            apigw.LambdaIntegration(lambda_functions["get_all_tasks"]),   
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=cognito_authorizer 
        )

        # /tasks/assign POST
        assign = tasks.add_resource("assign")
        assign.add_method(
            "POST", 
            apigw.LambdaIntegration(lambda_functions["assign_task"]),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=cognito_authorizer 
        )

        # /tasks/update-status POST
        update = tasks.add_resource("update-status")
        update.add_method(
            "POST",
            apigw.LambdaIntegration(lambda_functions["update_task_status"]),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=cognito_authorizer 
        )

        # /tasks/user GET
        user = tasks.add_resource("user")
        user.add_method(
            "GET", 
            apigw.LambdaIntegration(lambda_functions["get_user_tasks"]),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=cognito_authorizer 
        )
        
        # /tasks/update POST
        update = update = tasks.add_resource("update")
        update.add_method(
            "POST",
            apigw.LambdaIntegration(lambda_functions["update_task"]),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=cognito_authorizer 
        )
        
        # /tasks/delete DELETE
        delete = tasks.add_resource("delete")
        delete.add_method(
            "DELETE",
            apigw.LambdaIntegration(lambda_functions["delete_task"]),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=cognito_authorizer 
        )

    
      
      
