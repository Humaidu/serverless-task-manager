import aws_cdk as core
import aws_cdk.assertions as assertions

from task_manager_backend.task_manager_backend_stack import TaskManagerBackendStack

# example tests. To run these tests, uncomment this file along with the example
# resource in task_manager_backend/task_manager_backend_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TaskManagerBackendStack(app, "task-manager-backend")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
