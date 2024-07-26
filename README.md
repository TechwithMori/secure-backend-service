# Secure Backend Service

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Setup and Installation](#setup-and-installation)
- [API Development](#api-development)
  - [Endpoints](#endpoints)
  - [Running the Application](#running-the-application)
  - [Testing with Postman](#testing-with-postman)
- [Deployment](#deployment)
  - [Local Kubernetes Cluster](#local-kubernetes-cluster)
  - [Deploying to a Cloud Provider](#deploying-to-a-cloud-provider)
- [CI/CD Pipeline](#cicd-pipeline)

## Introduction

The Secure Backend Service is a Flask-based application that provides a secure API for managing security records. It includes token-based authentication and demonstrates how to use Kubernetes for container orchestration.

## Features

- Token-based authentication
- CRUD operations for security records
- Kubernetes deployment support
- CI/CD pipeline using GitHub Actions

## Technologies

- Python 3.9
- Flask
- Flask-SQLAlchemy
- SQLite
- Docker
- Kubernetes
- GitHub Actions

## Setup and Installation

### Prerequisites

- Python 3.9
- Docker
- Kubernetes (Minikube or Docker Desktop for local development)
- kubectl
- Git

### Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/secure-backend-service.git
cd secure-backend-service
```

2. Create a virtual environment and activate it:
   
```sh
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

3. install the dependencies:

```sh
pip install -r requirements.txt
```

4. initialize the Database:

```sh
flask db init
flask db migrate
flask db upgrade
```

## API Development
### Endpoints

-Generate Token: POST /auth/token
Request: { "user_id": "test_user" }
Response: { "token": "your_generated_token" }

-Validate Token: POST /auth/validate
Request: { "token": "your_generated_token" }
Response: { "valid": true }

-Create Security Record: POST /security
Request: { "name": "record_name", "description": "record_description" }
Response: { "id": 1 }

-Get Security Record: GET /security/<id>
Response: { "id": 1, "name": "record_name", "description": "record_description", "timestamp": "timestamp" }

-Update Security Record: PUT /security/<id>
Request: { "name": "new_name", "description": "new_description" }
Response: { "id": 1, "name": "new_name", "description": "new_description", "timestamp": "timestamp" }

-Delete Security Record: DELETE /security/<id>
Response: { "message": "Record deleted" }
List Security Records: GET /security

Response: [ { "id": 1, "name": "record_name", "description": "record_description", "timestamp": "timestamp" } ]

### Running the Application
to run the application locally:
```sh
flask run
```
The application will be available at http://127.0.0.1:5000.

### Testing with Postman
1- Generate Token:
  -Method: POST
  -URL: http://127.0.0.1:5000/auth/token
  -Body: { "user_id": "test_user" }

2- Validate Token:
  -Method: POST
  -URL: http://127.0.0.1:5000/auth/validate
  -Body: { "token": "your_generated_token" }

3- Create Security Record:
  -Method: POST
  -URL: http://127.0.0.1:5000/security
  -Headers: { "Authorization": "your_generated_token" }
  -Body: { "name": "record_name", "description": "record_description" }

4- Get Security Record:
  -Method: GET
  -URL: http://127.0.0.1:5000/security/1
  -Headers: { "Authorization": "your_generated_token" }

5- Update Security Record:
  -Method: PUT
  -URL: http://127.0.0.1:5000/security/1
  -Headers: { "Authorization": "your_generated_token" }
  -Body: { "name": "new_name", "description": "new_description" }

6- Delete Security Record:
  -Method: DELETE
  -URL: http://127.0.0.1:5000/security/1
  -Headers: { "Authorization": "your_generated_token" }

7- List Security Records:
  -Method: GET
  -URL: http://127.0.0.1:5000/security
  -Headers: { "Authorization": "your_generated_token" }

## Deployment
### Local Kubernetes Cluster
1-Build Docker Image:
```sh
docker build -t your-docker-image .
```
2-Deploy to Kubernetes:
```sh
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```
3- Access the Application:
```sh
kubectl port-forward service/your-service 8080:80
```
The application will be available at http://localhost:8080.

## Deploying to a Cloud Provider
### Push Docker Image to Docker Hub:
```sh
docker login
docker push your-docker-image
```
### Set Up Kubernetes Cluster on a Cloud Provider:
 -Use a managed Kubernetes service like Google Kubernetes Engine (GKE), Amazon Elastic Kubernetes Service (EKS), or Azure Kubernetes Service (AKS).

### Update Kubernetes Manifests:
 -Update the image in your Kubernetes deployment manifest to use the Docker Hub image.
 
### Deploy to the Cloud:
```sh
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```
### Access the Application:
 -Use the external IP provided by your cloud provider to access the service.
 
## CI/CD Pipeline
The project includes a GitHub Actions workflow for CI/CD. The workflow is triggered on every push to the repository. It performs the following steps:
1- Checks out the code
2- Sets up Python
3- Installs dependencies
4- Builds the Docker image
5- Pushes the Docker image to Docker Hub
6- Deploys the application to Kubernetes
