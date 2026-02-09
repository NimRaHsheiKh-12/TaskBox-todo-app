#!/bin/bash

# Script to clean up the Todo application deployment from Minikube

set -e  # Exit immediately if a command exits with a non-zero status

echo "Cleaning up Todo application from Minikube..."

# Uninstall the Helm release
echo "Uninstalling Helm release..."
helm uninstall todo-app || { echo "Helm release may not exist or already removed."; }

# Optionally, stop Minikube
echo "Stopping Minikube cluster..."
minikube stop

echo "Cleanup completed!"