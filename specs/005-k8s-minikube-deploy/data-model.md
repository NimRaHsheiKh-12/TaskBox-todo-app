# Data Model: Todo Application for Kubernetes Deployment

## Overview
This document describes the data model for the Todo application being deployed to Kubernetes (Minikube). The model focuses on the application entities and their relationships as they relate to the containerized deployment.

## Key Entities

### 1. Todo Item
The primary entity representing a todo item in the application.

#### Fields
- **id** (string/UUID): Unique identifier for the todo item
- **title** (string): Title or description of the todo item
- **completed** (boolean): Status indicating if the todo item is completed
- **createdAt** (datetime): Timestamp when the item was created
- **updatedAt** (datetime): Timestamp when the item was last updated
- **userId** (string/UUID, optional): Identifier for the user who owns the todo item (if user authentication is implemented)

#### Relationships
- Belongs to a User (optional, if user authentication is implemented)

#### Validation Rules
- `title` must be between 1 and 255 characters
- `completed` defaults to false
- `createdAt` is automatically set on creation
- `updatedAt` is automatically updated on modification

#### State Transitions
- `pending` → `completed` when marked as done
- `completed` → `pending` when unmarked

### 2. User (Optional)
User entity if authentication is implemented in the Todo application.

#### Fields
- **id** (string/UUID): Unique identifier for the user
- **username** (string): Username for login
- **email** (string): Email address of the user
- **passwordHash** (string): Hashed password for authentication
- **createdAt** (datetime): Timestamp when the user account was created
- **updatedAt** (datetime): Timestamp when the user account was last updated

#### Relationships
- Has many Todo Items

#### Validation Rules
- `username` must be unique and between 3 and 50 characters
- `email` must be a valid email format and unique
- `passwordHash` must be present and meet security requirements

## Service Architecture Entities

### 3. Frontend Service
Represents the frontend component of the Todo application in the Kubernetes deployment.

#### Fields
- **name** (string): Service name (e.g., "todo-frontend")
- **port** (integer): Port number for the service (e.g., 80)
- **targetPort** (integer): Internal port of the container (e.g., 3000)
- **type** (string): Service type (ClusterIP, NodePort, LoadBalancer)
- **replicas** (integer): Number of pod replicas to maintain
- **image** (string): Docker image reference for the frontend

#### Relationships
- Connects to Backend Service for API calls

### 4. Backend Service
Represents the backend API component of the Todo application in the Kubernetes deployment.

#### Fields
- **name** (string): Service name (e.g., "todo-backend")
- **port** (integer): Port number for the service (e.g., 8080)
- **targetPort** (integer): Internal port of the container (e.g., 8000)
- **type** (string): Service type (ClusterIP, NodePort, LoadBalancer)
- **replicas** (integer): Number of pod replicas to maintain
- **image** (string): Docker image reference for the backend
- **environment** (map): Environment variables for the service

#### Relationships
- Connected to by Frontend Service for API requests
- May connect to Database Service (if persistence is added)

## Deployment Configuration Entities

### 5. Kubernetes Deployment
Configuration for deploying the Todo application components to Kubernetes.

#### Fields
- **name** (string): Name of the deployment
- **namespace** (string): Kubernetes namespace for the deployment
- **labels** (map): Labels for identifying the deployment
- **selector** (map): Selector for matching pods
- **template** (object): Pod template specification
- **replicas** (integer): Desired number of pod replicas
- **resources** (object): Resource limits and requests

### 6. Kubernetes Service
Configuration for exposing the Todo application components in Kubernetes.

#### Fields
- **name** (string): Name of the service
- **type** (string): Service type (ClusterIP, NodePort, LoadBalancer)
- **ports** (array): Array of port configurations
- **selector** (map): Selector for matching pods to serve traffic

### 7. Ingress Configuration
Configuration for routing external traffic to the Todo application.

#### Fields
- **host** (string): Hostname for the ingress rule
- **path** (string): Path pattern for routing
- **serviceName** (string): Name of the service to route to
- **servicePort** (integer/string): Port of the service to route to

## Data Flow
1. User interacts with the Frontend Service through the browser
2. Frontend Service communicates with the Backend Service via API calls
3. Backend Service processes requests and manages Todo Items
4. (Future) Backend Service may persist data to a database if persistence is implemented

## Assumptions
- The current Todo application stores data in-memory or client-side
- Persistence to a database will be implemented in future iterations
- Authentication is optional and may be added in future iterations
- The application follows a microservices architecture with separate frontend and backend services