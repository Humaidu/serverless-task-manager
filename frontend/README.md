# Task Management Frontend (Angular)

This is the frontend of the **Serverless Task Management System** built with **Angular**. It allows users to create tasks, view assigned tasks, and mark them as completed.

---

## Features

- ✅ Create new tasks with title, description, assignee, and deadline
- 📋 View all assigned tasks in a responsive Bootstrap grid
- ✅ Mark tasks as completed
- 🌐 Connects to AWS Lambda functions via API Gateway
- 🎨 Styled with Bootstrap 5

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

Install Angular CLI globally if you haven't:

```bash
npm install -g @angular/cli

```

---

## Installation

Clone the repository and install dependencies:

```
git clone https://github.com/Humaidu/task-manager-frontend.git
cd task-manager-frontend
npm install

```

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
