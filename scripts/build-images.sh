#!/bin/bash

# Script to build Docker images for the Todo application

set -e  # Exit immediately if a command exits with a non-zero status

echo "Building Docker images for Todo application..."

# Build frontend image
echo "Building frontend image..."
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Build backend image
echo "Building backend image..."
docker build -f Dockerfile.backend -t todo-backend:latest .

echo "Images built successfully!"
echo "Frontend image: todo-frontend:latest"
echo "Backend image: todo-backend:latest"