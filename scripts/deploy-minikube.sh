#!/bin/bash

# Script to deploy the Todo application to Minikube

set -e  # Exit immediately if a command exits with a non-zero status

echo "Deploying Todo application to Minikube..."

# Ensure Minikube is running
echo "Checking if Minikube is running..."
minikube status || { echo "Minikube is not running. Starting Minikube..."; minikube start; }

# Load frontend image into Minikube
echo "Loading frontend image into Minikube..."
minikube image load todo-frontend:latest

# Load backend image into Minikube
echo "Loading backend image into Minikube..."
minikube image load todo-backend:latest

# Navigate to the Helm chart directory
cd helm/todo-app

# Install the Helm chart
echo "Installing Helm chart..."
helm install todo-app . --values values.yaml

echo "Application deployed successfully!"
echo "Access the application using: minikube service todo-frontend-service --url"