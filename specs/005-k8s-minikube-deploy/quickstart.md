# Quickstart Guide: Deploy Todo Application to Kubernetes (Minikube)

## Prerequisites

Before deploying the Todo application to Minikube, ensure you have the following tools installed:

- [Docker](https://docs.docker.com/get-docker/) (with Docker Buildx)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)

## Step 1: Start Minikube Cluster

Start your local Minikube cluster with sufficient resources for the Todo application:

```bash
minikube start --cpus=2 --memory=4g --disk-size=20g
```

## Step 2: Clone or Navigate to Your Todo Application Repository

```bash
cd /path/to/your/todo-fullstack-app
```

## Step 3: Build Docker Images

Build Docker images for both frontend and backend components:

```bash
# Build frontend image
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Build backend image
docker build -f Dockerfile.backend -t todo-backend:latest .
```

If Dockerfiles don't exist yet, create them based on the application's requirements:

**Dockerfile.frontend example:**
```Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ ./
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Dockerfile.backend example:**
```Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY backend/package*.json ./
RUN npm ci --only=production
COPY backend/ ./
EXPOSE 8000
CMD ["npm", "start"]
```

## Step 4: Load Images into Minikube

Load the built images into the Minikube cluster:

```bash
# Load frontend image
minikube image load todo-frontend:latest

# Load backend image
minikube image load todo-backend:latest
```

## Step 5: Install Helm Chart

Navigate to the Helm chart directory and install the chart:

```bash
cd helm/todo-app

# Install the Helm chart
helm install todo-app . --values values.yaml
```

## Step 6: Verify Deployment

Check that all resources are running correctly:

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Check deployments
kubectl get deployments
```

## Step 7: Access the Application

Get the external IP/URL for the frontend service:

```bash
minikube service todo-frontend-service --url
```

Or, if using an ingress controller:

```bash
minikube addons enable ingress
minikube tunnel  # Run in a separate terminal
```

Then access the application at the configured ingress host.

## Step 8: Troubleshooting

If you encounter issues:

1. Check pod status and logs:
   ```bash
   kubectl get pods
   kubectl logs <pod-name>
   ```

2. Verify service endpoints:
   ```bash
   kubectl get svc
   kubectl describe svc <service-name>
   ```

3. Check ingress if using:
   ```bash
   kubectl get ingress
   kubectl describe ingress <ingress-name>
   ```

## Cleanup

To remove the application from your Minikube cluster:

```bash
# Uninstall the Helm release
helm uninstall todo-app

# Optionally, stop Minikube
minikube stop
```

## Using kubectl-ai (Optional)

If kubectl-ai is available, you can use natural language commands:

```bash
# Install kubectl-ai plugin
kubectl krew install ai

# Example usage
kubectl ai "show me all pods in the default namespace"
kubectl ai "describe the todo-frontend deployment"
```

## Next Steps

1. Customize the `values.yaml` file to adjust resource allocations, replica counts, etc.
2. Add health checks to the deployments
3. Implement persistent storage if needed
4. Set up monitoring and logging
5. Configure SSL certificates for HTTPS

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

6. For Helm-related issues:
   ```bash
   # Check Helm release status
   helm status todo-app

   # Check Helm history
   helm history todo-app

   # Rollback to previous version
   helm rollback todo-app
   ```