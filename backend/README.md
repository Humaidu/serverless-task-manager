# Serverless Task Management System (AWS CDK + Python)

A fully serverless backend system for managing tasks assigned to field team members. Admins can create and assign tasks, and team members can log in to view and update their assigned tasks. The solution is built using **AWS Lambda (Python)**, **Amazon DynamoDB**, **API Gateway**, **Amazon Cognito**, and deployed with **AWS CDK (Python)**.

---

## Features

- 🔐 **User authentication** via Amazon Cognito (admin and team members)
- ✅ **Task creation** and **assignment** by admin
- 📋 **Task status update** by team members
- ⏰ **Deadline tracking** with timestamps
- 📩 **Secure API** with Cognito JWT integration
- ⚙️ **Serverless architecture** with AWS CDK
- 🧪 Testable locally via `curl` and Postman using tokens

---

## 🧱 Architecture Overview

---

## Prerequisites

- AWS CLI configured (`aws configure`)
- CDK installed (`npm install -g aws-cdk`)
- Python 3.8+ and `pip`
- Virtual environment:
  ```bash
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt

  ```

---

## Clone the Repo & Setup Project

```
git clone https://github.com/your-username/serverless-task-manager.git
cd serverless-task-manager

```

---

## Bootstrap & Deploy the CDK Stack

```
cdk bootstrap
cdk deploy

```

**This will:**

- Create DynamoDB table: TasksTable
- Deploy all Lambda functions
- Create API Gateway with /tasks routes
- Set up Cognito User Pool and Client
- Connect everything securely

---

## Lambda Functions

**All Lambda functions are written in Python and located under:**

```
task-manager-backend/lambda_functions/
├── create_task.py
├── assign_task.py
├── get_all_tasks.py
├── update_task_status.py
└── get_user_tasks.py

```

Each function handles a specific part of task lifecycle and interacts with DynamoDB securely.

---

## 🧾 DynamoDB Schema

A single table `TasksTable` with the following schema:

| Field        | Type   | Description                         |
|--------------|--------|-------------------------------------|
| `task_id`    | String | Primary Key (UUID)                  |
| `title`      | String | Task title                          |
| `description`| String | Task details                        |
| `assigned_to`| String | Email/username of assignee          |
| `status`     | String | Task status (e.g., pending)         |
| `deadline`   | String | ISO 8601 date string                |
| `created_at` | String | Timestamp of creation               |

---

## Permissions and IAM
Each Lambda function is granted read/write access only to the DynamoDB table:

```
tasks_table.grant_read_write_data(my_lambda)

```
API Gateway uses Cognito Authorizer to protect routes.

---

## API Gateway Implementation

**API Gateway is configured using CDK to:**

- Expose a REST API
- Create resource path /tasks
- Add HTTP methods:
    - POST /tasks → create_task.py
    - GET /tasks → get_tasks.py
    - PUT /tasks/{task_id} → update_task_status.py
- Attach a Cognito User Pool Authorizer to all endpoints

---

## Cognito Authorizer Setup

**In CDK:**
```
authorizer = apigateway.CognitoUserPoolsAuthorizer(
    self, "TasksAuthorizer",
    cognito_user_pools=[user_pool]
)

tasks_resource = api.root.add_resource("tasks")

tasks_resource.add_method(
    "POST",
    apigateway.LambdaIntegration(create_task_fn),
    authorizer=authorizer,
    authorization_type=apigateway.AuthorizationType.COGNITO
)

```
---

## API Documentation

> **Note:** All endpoints require a valid **Cognito JWT Token** in the `Authorization` header.

---

### POST `/tasks`
**Create a new task** (Admin only)

#### Headers:
```
Authorization: <Cognito JWT Token>
Content-Type: application/json

```

#### Body:

```
{
  "title": "Inspect server",
  "description": "Check the logs for errors",
  "assigned_to": "tech1@example.com",
  "deadline": "2025-06-01T00:00:00Z"
}

```
#### Response:

```
{ "message": "Task created", "task_id": "uuid" }

```

---


### GET `/tasks`
**Fetch tasks assigned to the current user.** 

#### Headers:
```
Authorization: <Cognito JWT Token>

```

#### Response:

```
[
  {
    "task_id": "uuid",
    "title": "Inspect server",
    "description": "Check the logs for errors",
    "status": "pending",
    "deadline": "2025-06-01T00:00:00Z",
    "created_at": "2025-05-25T12:00:00Z"
  }
]

```

---


### 🔸 PUT `/tasks/{task_id}`
**Create a new task** (Admin only)

#### Headers:
```
Authorization: <Cognito JWT Token>
Content-Type: application/json

```

#### Body:

```
{ "status": "completed" }

```
#### Response:

```
{ "message": "Task updated successfully" }

```



