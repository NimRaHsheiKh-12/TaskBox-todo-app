# Todo Application - Kubernetes Deployment

This repository contains the deployment configuration for the Todo application on Kubernetes using Minikube. The application consists of a frontend and backend service that are containerized and deployed using Helm charts.

## Architecture

The deployment consists of:
- **Frontend Service**: A React-based web application served via Nginx
- **Backend Service**: A FastAPI-based REST API
- **Ingress Controller**: Routes traffic to frontend and backend services
- **Helm Chart**: Package manager for Kubernetes deployment

## Prerequisites

Before deploying the application, ensure you have the following tools installed:

- [Docker](https://docs.docker.com/get-docker/) (with Docker Buildx)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)

Choose one of the following Kubernetes solutions:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Kubernetes enabled (recommended for beginners on Windows)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) (for local development)

## Quick Deployment

For a quick deployment using our automated script:

### On Windows (PowerShell):
```powershell
# For Docker Desktop Kubernetes
.\deploy_k8s.ps1 -ClusterType docker-desktop -Environment dev

# For Minikube
# Run PowerShell as Administrator, then:
.\deploy_k8s.ps1 -ClusterType minikube -Environment dev
```

### On Windows with WSL/Git Bash:
```bash
# Make the script executable
chmod +x deploy_k8s.sh

# For Docker Desktop Kubernetes
./deploy_k8s.sh docker-desktop dev

# For Minikube (run as root/administrator)
sudo ./deploy_k8s.sh minikube dev
```

## Manual Deployment Steps

### 1. Set up Kubernetes Cluster

#### Option A: Using Docker Desktop (Recommended for beginners)
1. Open Docker Desktop Settings
2. Go to the "Kubernetes" tab
3. Check "Enable Kubernetes"
4. Click "Apply & Restart"
5. Once Docker Desktop restarts, Kubernetes will be available

#### Option B: Using Minikube
1. Run Command Prompt or PowerShell as Administrator
2. Start Minikube cluster:
   ```bash
   minikube start --driver=hyperv --cpus=2 --memory=4096mb --disk-size=20g
   ```
   (For VirtualBox, replace `--driver=hyperv` with `--driver=virtualbox`)

### 2. Build Docker Images

Build Docker images for both frontend and backend components:

```bash
# Build frontend image
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Build backend image
docker build -f Dockerfile.backend -t todo-backend:latest .
```

### 3. Load Images into Cluster

#### For Minikube:
```bash
# Load frontend image
minikube image load todo-frontend:latest

# Load backend image
minikube image load todo-backend:latest
```

#### For Docker Desktop:
Images are automatically available since Docker Desktop shares the same Docker daemon as your host.

### 4. Install Helm Chart

Install the Helm chart with default values:

```bash
# Install the Helm chart
helm install todo-app ./helm/todo-app --values ./helm/todo-app/values.yaml --create-namespace --namespace todo-app
```

### 5. Verify Deployment

Check that all resources are running correctly:

```bash
# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get services -n todo-app

# Check deployments
kubectl get deployments -n todo-app

# Check ingress
kubectl get ingress -n todo-app
```

### 6. Access the Application

#### For Docker Desktop:
Use port forwarding to access the services:
```bash
# Forward frontend service
kubectl port-forward -n todo-app svc/todo-frontend-service 3000:80

# In another terminal, forward backend service
kubectl port-forward -n todo-app svc/todo-backend-service 8000:8000
```

Then access the frontend at http://localhost:3000

#### For Minikube:
```bash
minikube addons enable ingress
minikube tunnel  # Run in a separate terminal
```

Then access the application at the configured ingress host (default: `todo.local`).

## Configuration

The application can be configured using the `values.yaml` file in the Helm chart. Key configuration options include:

- `frontend.replicaCount`: Number of frontend pods to run
- `backend.replicaCount`: Number of backend pods to run
- `frontend.service.type`: Service type for frontend (ClusterIP, NodePort, LoadBalancer)
- `backend.service.type`: Service type for backend
- `resources`: CPU and memory limits/requests for containers
- `database.url`: Database connection string

## Upgrading the Deployment

To upgrade the deployment with new configuration:

```bash
# Update the values.yaml file with new configuration
# Then run:
helm upgrade todo-app ./helm/todo-app --values ./helm/todo-app/values.yaml --namespace todo-app
```

## Rolling Back

To rollback to a previous version:

```bash
helm rollback todo-app --namespace todo-app
```

## Uninstalling

To remove the application from your Minikube cluster:

```bash
# Uninstall the Helm release
helm uninstall todo-app -n todo-app

# Optionally, stop Minikube
minikube stop
```

## Troubleshooting

If you encounter issues:

1. Check pod status and logs:
   ```bash
   kubectl get pods -n todo-app
   kubectl logs -n todo-app <pod-name>
   ```

2. Verify service endpoints:
   ```bash
   kubectl get svc -n todo-app
   kubectl describe svc -n todo-app <service-name>
   ```

3. Check ingress if using:
   ```bash
   kubectl get ingress -n todo-app
   kubectl describe ingress -n todo-app <ingress-name>
   ```

4. If images fail to pull, ensure they are loaded in Minikube:
   ```bash
   minikube image load todo-frontend:latest
   minikube image load todo-backend:latest
   ```

5. If services are not accessible, check Minikube tunnel:
   ```bash
   minikube tunnel  # Run in a separate terminal
   ```

## Development

For local development, you can use the provided docker-compose.yml:

```bash
docker-compose up --build
```

## Monitoring and Logging

The deployment includes basic health checks for both frontend and backend services. For more advanced monitoring and logging, consider integrating with Prometheus and ELK stack.

## Security Considerations

- Containers run as non-root users
- Resource limits are configured to prevent resource exhaustion
- Network policies can be added to restrict traffic between services
- Secrets management should be implemented for sensitive data