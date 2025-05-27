#!/usr/bin/env python3
import os

import aws_cdk as cdk

from task_manager_backend.task_manager_backend_stack import TaskManagerBackendStack


app = cdk.App()
TaskManagerBackendStack(app, "TaskManagerBackendStack")

app.synth()
