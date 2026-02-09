# Manual Helm Commands for Todo Application Deployment

## Prerequisites
```bash
# Verify tools are available
kubectl version
helm version
docker version

# Ensure Docker images are built
docker build -f Dockerfile.frontend -t todo-frontend:latest .
docker build -f Dockerfile.backend -t todo-backend:latest .
```

## Create Namespace
```bash
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
```

## Install/Upgrade Helm Chart
```bash
# For the first installation
helm install todo-app ./helm/todo-app --values ./helm/todo-app/values.yaml --create-namespace --namespace todo-app --wait --timeout 10m --atomic

# For upgrading an existing installation
helm upgrade todo-app ./helm/todo-app --values ./helm/todo-app/values.yaml --namespace todo-app --wait --timeout 10m --atomic
```

## Alternative: Install with Development Values
```bash
# Create development values file first
cat > ./helm/todo-app/values-dev.yaml << EOF
frontend:
  replicaCount: 1
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: Never  # Use local images
  service:
    type: NodePort
    port: 80
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
    repository: todo-backend
    tag: latest
    pullPolicy: Never  # Use local images
  service:
    type: ClusterIP
    port: 8000
  resources:
    requests:
      memory: "128Mi"
      cpu: "200m"
    limits:
      memory: "256Mi"
      cpu: "400m"

ingress:
  enabled: true
  className: ""
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix
        - path: /api
          pathType: Prefix
  tls: []
EOF

# Install with development values
helm install todo-app ./helm/todo-app --values ./helm/todo-app/values-dev.yaml --create-namespace --namespace todo-app --wait --timeout 10m --atomic
```

## Troubleshooting Commands
```bash
# Check if release exists
helm list --namespace todo-app

# Uninstall the release if needed
helm uninstall todo-app --namespace todo-app

# Check status of release
helm status todo-app --namespace todo-app

# Get values used for release
helm get values todo-app --namespace todo-app
```