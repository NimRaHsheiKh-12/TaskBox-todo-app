#!/bin/bash

# Script to deploy the Todo application to Kubernetes
# This script assumes you have Docker, kubectl, and Helm installed

set -e  # Exit immediately if a command exits with a non-zero status

# Default values
CLUSTER_TYPE="${1:-docker-desktop}"
ENVIRONMENT="${2:-dev}"
NAMESPACE="${3:-todo-app}"

echo "🚀 Starting deployment of Todo application to Kubernetes..."

# Check if required tools are installed
for tool in docker kubectl helm; do
    if ! command -v $tool &> /dev/null; then
        echo "❌ $tool is not installed or not in PATH. Please install $tool and try again."
        exit 1
    fi
done

# Function to check if running as root for Minikube
is_root_for_minikube() {
    if [ "$CLUSTER_TYPE" = "minikube" ]; then
        if [[ $EUID -ne 0 ]]; then
            echo "⚠️  Running Minikube may require elevated privileges."
            read -p "Do you want to continue anyway? (y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 0
            fi
        fi
    fi
}

# Check if running as root for Minikube
is_root_for_minikube

case $CLUSTER_TYPE in
    "docker-desktop")
        echo "🐳 Using Docker Desktop Kubernetes..."
        
        # Verify Docker Desktop Kubernetes is enabled
        if ! kubectl cluster-info &> /dev/null; then
            echo "❌ Docker Desktop Kubernetes is not enabled or not accessible. Please enable Kubernetes in Docker Desktop settings."
            exit 1
        else
            echo "✅ Docker Desktop Kubernetes is accessible"
        fi
        ;;
    "minikube")
        echo "🐹 Starting Minikube cluster..."
        
        # Attempt to start Minikube
        if ! minikube start --driver=hyperv --cpus=2 --memory=4096mb --disk-size=20g 2>/dev/null; then
            echo "Trying with VirtualBox driver..."
            if ! minikube start --driver=virtualbox --cpus=2 --memory=4096mb --disk-size=20g; then
                echo "❌ Failed to start Minikube with both Hyper-V and VirtualBox drivers."
                exit 1
            fi
        fi
        
        # Enable ingress addon
        minikube addons enable ingress
        echo "✅ Minikube cluster is running"
        ;;
    *)
        echo "❌ Unknown cluster type: $CLUSTER_TYPE"
        echo "Supported types: docker-desktop, minikube"
        exit 1
        ;;
esac

# Build Docker images
echo "📦 Building Docker images..."
docker build -f Dockerfile.frontend -t todo-frontend:latest .
if [ $? -ne 0 ]; then
    echo "❌ Failed to build frontend image"
    exit 1
fi

docker build -f Dockerfile.backend -t todo-backend:latest .
if [ $? -ne 0 ]; then
    echo "❌ Failed to build backend image"
    exit 1
fi

# Load images into cluster if using Minikube
if [ "$CLUSTER_TYPE" = "minikube" ]; then
    echo "📥 Loading images into Minikube..."
    minikube image load todo-frontend:latest
    if [ $? -ne 0 ]; then
        echo "❌ Failed to load frontend image into Minikube"
        exit 1
    fi
    
    minikube image load todo-backend:latest
    if [ $? -ne 0 ]; then
        echo "❌ Failed to load backend image into Minikube"
        exit 1
    fi
fi

# Create namespace
echo "🌐 Creating namespace: $NAMESPACE"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Determine values file based on environment
VALUES_FILE="./helm/todo-app/values.yaml"
if [ "$ENVIRONMENT" = "dev" ]; then
    VALUES_FILE="./helm/todo-app/values-dev.yaml"
    # Create a basic dev values file if it doesn't exist
    if [ ! -f "$VALUES_FILE" ]; then
        cat > "$VALUES_FILE" << EOF
frontend:
  replicaCount: 1
  image:
    pullPolicy: Always
  resources:
    requests:
      memory: "64Mi"
      cpu: "100m"
    limits:
      memory: "128Mi"
      cpu: "200m"

backend:
  replicaCount: 1
  image:
    pullPolicy: Always
  resources:
    requests:
      memory: "128Mi"
      cpu: "200m"
    limits:
      memory: "256Mi"
      cpu: "400m"
EOF
    fi
elif [ "$ENVIRONMENT" = "prod" ]; then
    VALUES_FILE="./helm/todo-app/values-prod.yaml"
fi

# Install Helm chart
echo "🚢 Installing Helm chart..."
helm install todo-app ./helm/todo-app \
    --values "$VALUES_FILE" \
    --create-namespace \
    --namespace "$NAMESPACE" \
    --wait \
    --timeout 10m

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Helm chart"
    exit 1
fi

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-frontend -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=ready pod -l app=todo-backend -n $NAMESPACE --timeout=300s

# Show deployment status
echo
echo "✅ Deployment completed successfully!"
echo "📊 Deployment status:"
kubectl get pods,svc,ingress -n $NAMESPACE

# Provide access information based on cluster type
if [ "$CLUSTER_TYPE" = "minikube" ]; then
    echo
    echo "🌐 To access the application:"
    echo "Run 'minikube tunnel' in a separate terminal, then access the application at the configured ingress host (default: todo.local)"
else
    echo
    echo "🌐 To access the application:"
    echo "Use 'kubectl port-forward' to access services locally, or configure ingress for external access"
fi

echo
echo "🎉 Your Todo application is now deployed on Kubernetes!"