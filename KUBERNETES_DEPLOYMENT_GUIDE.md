# Kubernetes Deployment Guide for Todo Fullstack Application

This guide provides detailed steps to deploy your fullstack Todo application on Kubernetes using Helm charts.

## Prerequisites

Before deploying the application, ensure you have the following tools installed:

- [Docker](https://docs.docker.com/get-docker/) (with Docker Buildx)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) (for local deployment) or access to a Kubernetes cluster

## Local Setup with Minikube or Docker Desktop

### Option 1: Using Docker Desktop with Kubernetes (Recommended for beginners)

Docker Desktop for Windows includes a built-in Kubernetes server that can be enabled:

1. Open Docker Desktop Settings
2. Go to the "Kubernetes" tab
3. Check "Enable Kubernetes"
4. Click "Apply & Restart"
5. Once Docker Desktop restarts, Kubernetes will be available

6. Verify Kubernetes is running:
   ```bash
   kubectl cluster-info
   ```

### Option 2: Using Minikube

#### 1. Prerequisites for Windows

On Windows, you'll need to run commands with administrator privileges. Open Command Prompt or PowerShell as Administrator before proceeding.

Additionally, you may need to enable Hyper-V or install VirtualBox/VMware for Minikube to work properly:

##### Option A: Using Hyper-V (Recommended for Windows)
1. Enable Hyper-V feature in Windows:
   - Go to "Turn Windows features on or off"
   - Check "Hyper-V" and click OK
   - Restart your computer

2. Run the following commands in an Administrator Command Prompt:
   ```bash
   # Create a virtual switch in Hyper-V (if not already created)
   New-VMSwitch -Name "minikube-switch" -NetAdapterName "Ethernet" -AllowManagementOS $true

   # Start Minikube with Hyper-V driver
   minikube start --driver=hyperv --hyperv-virtual-switch=minikube-switch --cpus=2 --memory=4096mb --disk-size=20g
   ```

##### Option B: Using VirtualBox
1. Download and install VirtualBox from https://www.virtualbox.org/
2. Run the following command in an Administrator Command Prompt:
   ```bash
   minikube start --driver=virtualbox --cpus=2 --memory=4096mb --disk-size=20g
   ```

### 2. Enable Ingress Addon

Enable the ingress addon in Minikube to route traffic to your services:

```bash
minikube addons enable ingress
```

## Building and Loading Docker Images

### 1. Build Docker Images

Build Docker images for both frontend and backend components:

```bash
# Build frontend image
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Build backend image
docker build -f Dockerfile.backend -t todo-backend:latest .
```

### 2. Load Images into Minikube (for local development)

Load the built images into the Minikube cluster:

```bash
# Load frontend image
minikube image load todo-frontend:latest

# Load backend image
minikube image load todo-backend:latest
```

### 3. Push Images to Container Registry (for production)

For cloud deployment, you'll need to push your images to a container registry like Docker Hub, Google Container Registry, or AWS ECR:

```bash
# Tag images for your registry
docker tag todo-frontend:latest <your-registry>/todo-frontend:latest
docker tag todo-backend:latest <your-registry>/todo-backend:latest

# Push images
docker push <your-registry>/todo-frontend:latest
docker push <your-registry>/todo-backend:latest
```

For Docker Hub, the commands would look like:
```bash
# Tag images for Docker Hub
docker tag todo-frontend:latest <dockerhub-username>/todo-frontend:latest
docker tag todo-backend:latest <dockerhub-username>/todo-backend:latest

# Push images to Docker Hub
docker push <dockerhub-username>/todo-frontend:latest
docker push <dockerhub-username>/todo-backend:latest
```

## Deploying with Helm Charts

### 1. Install Helm Chart

Navigate to the Helm chart directory and install the chart:

```bash
# Install the Helm chart
helm install todo-app ./helm/todo-app --values ./helm/todo-app/values.yaml --create-namespace --namespace todo-app
```

### 2. Verify Deployment

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

### 3. Access the Application

Get the external IP/URL for the frontend service:

```bash
minikube service todo-frontend-service -n todo-app --url
```

Or, if using an ingress controller:

```bash
minikube tunnel  # Run in a separate terminal
```

Then access the application at the configured ingress host (default: `todo.local`).

## Production Deployment on Cloud Kubernetes

### 1. Push Images to Container Registry

For cloud deployment, you'll need to push your images to a container registry like Docker Hub, Google Container Registry, or AWS ECR:

```bash
# Tag images for your registry
docker tag todo-frontend:latest <your-registry>/todo-frontend:latest
docker tag todo-backend:latest <your-registry>/todo-backend:latest

# Push images
docker push <your-registry>/todo-frontend:latest
docker push <your-registry>/todo-backend:latest
```

### 2. Update Values File

Update the `values.yaml` file to reference your container registry:

```yaml
frontend:
  image:
    repository: <your-registry>/todo-frontend
    tag: latest
    pullPolicy: Always

backend:
  image:
    repository: <your-registry>/todo-backend
    tag: latest
    pullPolicy: Always
```

### 3. Deploy to Cloud Kubernetes

Deploy to your cloud Kubernetes cluster (GKE, EKS, AKS, etc.):

```bash
# Install the Helm chart
helm install todo-app ./helm/todo-app --values ./helm/todo-app/values.yaml --create-namespace --namespace todo-app
```

## Configuration Options

The application can be configured using the `values.yaml` file in the Helm chart. Key configuration options include:

- `frontend.replicaCount`: Number of frontend pods to run
- `backend.replicaCount`: Number of backend pods to run
- `frontend.service.type`: Service type for frontend (ClusterIP, NodePort, LoadBalancer)
- `backend.service.type`: Service type for backend
- `resources`: CPU and memory limits/requests for containers
- `database.url`: Database connection string

### Environment-Specific Values Files

For different environments (dev, staging, prod), create separate values files:

1. Create `values-dev.yaml` for development:
```yaml
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
```

2. Create `values-prod.yaml` for production:
```yaml
frontend:
  replicaCount: 3
  image:
    pullPolicy: IfNotPresent
  resources:
    requests:
      memory: "128Mi"
      cpu: "200m"
    limits:
      memory: "256Mi"
      cpu: "500m"

backend:
  replicaCount: 3
  image:
    pullPolicy: IfNotPresent
  resources:
    requests:
      memory: "256Mi"
      cpu: "300m"
    limits:
      memory: "512Mi"
      cpu: "600m"

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: yourdomain.com
      paths:
        - path: /
          pathType: Prefix
        - path: /api
          pathType: Prefix
```

3. Deploy with environment-specific values:
```bash
# For development
helm install todo-app ./helm/todo-app --values ./helm/todo-app/values-dev.yaml --create-namespace --namespace todo-app

# For production
helm install todo-app ./helm/todo-app --values ./helm/todo-app/values-prod.yaml --create-namespace --namespace todo-app
```

## Adding a Database

Currently, the application doesn't include a database in the Kubernetes manifests. To add PostgreSQL:

### 1. Create a PostgreSQL StatefulSet

Create a file `k8s/database.yaml`:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: todo-app
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: todo_db
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 1Gi
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: todo-app
spec:
  type: ClusterIP
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
---
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: todo-app
type: Opaque
data:
  username: dXNlcg==  # base64 encoded 'user'
  password: cGFzc3dvcmQ=  # base64 encoded 'password'
```

### 2. Update Backend Deployment

Update the backend deployment to connect to the PostgreSQL service:

```yaml
# In backend-deployment.yaml
env:
- name: DATABASE_URL
  value: "postgresql://user:password@postgres.todo-app.svc.cluster.local:5432/todo_db"
```

Apply the database configuration:

```bash
kubectl apply -f k8s/database.yaml
```

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

To remove the application from your Kubernetes cluster:

```bash
# Uninstall the Helm release
helm uninstall todo-app -n todo-app

# Optionally, delete the namespace
kubectl delete namespace todo-app
```

## Monitoring and Logging

The deployment includes basic health checks for both frontend and backend services. For more advanced monitoring and logging:

1. Install Prometheus and Grafana for metrics
2. Install ELK (Elasticsearch, Logstash, Kibana) or EFK (Elasticsearch, Fluentd, Kibana) stack for centralized logging

## Security Considerations

- Containers run as non-root users
- Resource limits are configured to prevent resource exhaustion
- Network policies can be added to restrict traffic between services
- Secrets management should be implemented for sensitive data
- RBAC (Role-Based Access Control) should be properly configured

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

4. If images fail to pull, ensure they are available in your registry:
   ```bash
   # For Minikube, ensure images are loaded
   minikube image load <image-name>:<tag>

   # For cloud deployments, ensure pull secrets are configured if using private registries
   ```

5. If services are not accessible, check your ingress controller and DNS configuration:
   ```bash
   kubectl get pods -n ingress-nginx  # Check if ingress controller is running
   ```

6. Common Windows-specific issues:
   - Make sure you're running commands as Administrator
   - If using Minikube with Hyper-V, ensure Hyper-V is enabled and properly configured
   - If using Docker Desktop Kubernetes, make sure it's enabled in Docker Desktop settings
   - Check that your kubectl context is pointing to the correct cluster:
     ```bash
     kubectl config get-contexts
     kubectl config use-context <correct-context>
     ```

7. If you get "connection refused" errors:
   - Ensure your Kubernetes cluster is running
   - Check that kubectl is properly configured to connect to your cluster
   - Verify that the Kubernetes API server is accessible

8. For Helm-related issues:
   - If Helm install fails due to Tiller issues (older versions), try:
     ```bash
     helm repo update
     helm install --generate-name <chart-name>
     ```
   - If you get "release already exists" error:
     ```bash
     helm uninstall <release-name> -n <namespace>
     ```

9. For resource constraints:
   - If pods are stuck in Pending state, check available resources:
     ```bash
     kubectl describe nodes
     kubectl top nodes  # if metrics server is enabled
     ```
   - Adjust resource requests/limits in your values.yaml file as needed