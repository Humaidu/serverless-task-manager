# Task Management Frontend (Angular)

The Serverless Task Manager is a full-stack application built with Angular for the frontend and AWS serverless technologies (API Gateway, Lambda, DynamoDB, Cognito) for the backend. This Angular frontend provides a responsive interface for task management with secure authentication.

It allows an Admin to create tasks, assign tasks, and mark them as completed or pending. Users can also view assigned task.

*Live App*: **http://task-manager-frontend-app-04.s3-website-eu-west-1.amazonaws.com**

---

## Features

- **User Authentication**:
  - Sign up, login, and logout using AWS Cognito
  - Protected routes with auth guards
  - JWT token management

- **Task Management**:
  - Create new tasks with title, description, assignee, and deadline
  - View all assigned tasks in a responsive Bootstrap grid
  - Mark tasks as completed
  - Assign tasks
  - Connects to AWS Lambda functions via API Gateway
  - Styled with Bootstrap 5

- **Technical Features**:
  - Angular 15+ (check your actual version)
  - RxJS for state management
  - Angular Material UI components
  - HTTP interceptors for API requests
  - Form validation with Reactive Forms
  - Environment-based configuration

---

## Project Structure

src/
├── app/
│ ├── components/
│ │ ├── task-list/
│ │ └── create-task/
│ ├── services/
│ │ └── task.service.ts
│ ├── app-routing.module.ts
│ ├── app.component.html
│ └── app.module.ts
└── index.html

---

## Prerequisites

Make sure you have the following installed:

- [Node.js](https://nodejs.org/) (v16+ recommended)
- [Angular CLI](https://angular.io/cli)
- npm v8.x or higher (or yarn)
- AWS backend services deployed:
  - API Gateway
  - Lambda functions
  - DynamoDB tables
  - Cognito User Pool

Install Angular CLI globally if you haven't:

```bash
npm install -g @angular/cli

```

---

## Installation

Clone the repository and install dependencies:

```
git clone https://github.com/Humaidu/task-manager-frontend.git
cd frontend/task-manager-frontend
npm install

```
---
## Install Dependencies

```
npm install
# or
yarn install

```

---
## Environment Configuration

Create a file called **environment.ts** in **src/environments/**:

```
export const environment = {
  production: false,
  apiBaseUrl: 'https://your-api-gateway-id.execute-api.region.amazonaws.com/prod'  // Update with your actual API Gateway URL
};

```

---

## Run Locally

```
ng serve

```

Then navigate to **http://localhost:4200/**.

---

## Build for Production

```
ng build

```

The output will be in the **dist/** directory.

---

## API Endpoints

These APIs are provided by the AWS Lambda backend (through API Gateway):

| Endpoint               | Method | Description        |
| ---------------------- | ------ | ------------------ |
| `/tasks`               | POST   | Create a new task  |
| `/tasks/all`           | GET    | Get all tasks      |
| `/tasks/assign`        | POST   | Assign a task      |
| `/tasks/update-status` | POST   | Update task status |

---

## Roles and Access

### User

- Allowed Actions:

    - View assigned tasks: GET /api/user/tasks

### Admin

- Allowed Actions:

    - Create task: POST /api/admin/task
    - Assign task: PUT /api/admin/task/:id/assign
    - Update task: PUT /api/admin/task/:id
    - Change task status: PUT /api/admin/task/:id/status
    - Delete task: DELETE /api/admin/task/:id

---

## Login Flow

- UI for login
- Upon successful login:

  - JWT is extracted from the URL
  - Token is saved in localStorage or memory
  - axiosInstance attaches the token to all requests
  - User is redirected to appropriate route based on group (User or Admin)

---

## Axios Interceptor (axiosInstance.ts)

```
import axios from 'axios';

const axiosInstance = axios.create();

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('id_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default axiosInstance;

```
---
## Frontend Deployment to AWS S3 (Static Hosting)

You can deploy your Angular frontend to an Amazon S3 bucket for static website hosting. Optionally, use CloudFront for CDN and HTTPS support.

---

### Step 1: Build Angular App for Production

```bash
ng build --configuration production

```
This will generate the build artifacts in the dist/ folder, typically:

```
dist/task-manager-frontend/

```

---
### Step 2: Create and Configure an S3 Bucket

**Create an s3 bucket**

Bucket name is `task-manager-frontend-app-04`

```
aws s3 mb s3://task-manager-frontend-app-04

```

---

**Enable Static website hosting**

```
aws s3 website  s3://task-manager-frontend-app-04 --index-document index.html --error-document index.html

```

---

**Set Bucket Policy (Public Read Access)**

Create a `policy.json` file

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::task-manager-frontend/*"
    }
  ]
}

```

*Then run:*

```
aws s3api put-bucket-policy --bucket s3://task-manager-frontend-app-04 --policy file://policy.json

```

---

**Upload the Angular Build to S3**

```
aws s3 sync ./dist/task-manager-frontend/ s3://task-manager-frontend-app-04 --delete

```

*Make sure your AWS CLI is configured:*

```
aws configure

```

---
## Access the Hosted App

- http://task-manager-frontend-app-04.s3-website-eu-west-1.amazonaws.com

---

 ## 🤖 CI/CD: Deploy Frontend to S3 via GitHub Actions

This GitHub Actions workflow automatically deploys your Angular frontend to an S3 bucket on every push to the `main` branch.

---

### 📝 Prerequisites

1. **AWS credentials** (IAM user with `AmazonS3FullAccess`)
2. Add the following GitHub Secrets to your repository:

| Secret Name         | Description                     |
|---------------------|---------------------------------|
| `AWS_ACCESS_KEY_ID` | Your AWS Access Key ID          |
| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Access Key  |
| `AWS_REGION`        | Your AWS region (e.g., `eu-west-1`) |
| `S3_BUCKET_NAME`    | Your S3 bucket name             |

---
### 🧾 `.github/workflows/deploy.yml`

```yaml
name: Task Manage Frontend Angular App to S3

on:
  push:
    branches:
      - main  

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'  

    - name: Install dependencies
      run: |
        cd frontend/task-manager-frontend
        npm install

    - name: Build Angular app
      run: |
        cd frontend/task-manager-frontend
        npm run build -- --configuration production

    - name: Upload to S3
      uses: jakejarvis/s3-sync-action@v0.5.1
      with:
        args: --delete
      env:
        AWS_S3_BUCKET: ${{ secrets.S3_BUCKET_NAME }}
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        AWS_REGION: ${{ secrets.AWS_REGION }}
        SOURCE_DIR: frontend/task-manager-frontend/dist/task-manager-frontend

```

---

## What It Does
- Runs on every push to main
- Builds the Angular app with production config
- Syncs the build output to your S3 bucket
- Deletes outdated files from S3

---

## Security Tip

Always use GitHub Secrets to store AWS credentials — never hardcode them in your repo.









