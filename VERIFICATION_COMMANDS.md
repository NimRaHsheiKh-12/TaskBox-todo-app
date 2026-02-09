# Verification Commands for Todo Application on Kubernetes

## Check Cluster Status
```bash
# Verify cluster connectivity
kubectl cluster-info

# Check node status
kubectl get nodes

# Check namespaces
kubectl get namespaces
```

## Check Application Resources
```bash
# Get all resources in the todo-app namespace
kubectl get all -n todo-app

# Check pods specifically
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check deployments
kubectl get deployments -n todo-app

# Check ingress (if configured)
kubectl get ingress -n todo-app
```

## Detailed Resource Information
```bash
# Describe pods for detailed information
kubectl describe pods -n todo-app

# Check logs of frontend pods
kubectl logs -l app=todo-frontend -n todo-app

# Check logs of backend pods
kubectl logs -l app=todo-backend -n todo-app

# Follow logs in real-time
kubectl logs -l app=todo-frontend -n todo-app -f
```

## Port Forwarding for Local Access
```bash
# Port forward frontend service
kubectl port-forward svc/todo-frontend -n todo-app 8080:80

# Port forward backend service
kubectl port-forward svc/todo-backend -n todo-app 8000:8000

# Access the application at:
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
```

## Health Checks
```bash
# Check readiness and health of pods
kubectl get pods -n todo-app -o wide

# Check resource utilization
kubectl top pods -n todo-app

# Check events in the namespace
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

## Helm-Specific Verification
```bash
# Check Helm release status
helm status todo-app -n todo-app

# List Helm releases in the namespace
helm list -n todo-app

# Get values used in the release
helm get values todo-app -n todo-app

# Get manifest of the release
helm get manifest todo-app -n todo-app
```

## Network Connectivity
```bash
# Test connectivity to services from within the cluster
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- bash
# Inside the shell, you can test connectivity:
# curl http://todo-backend.todo-app.svc.cluster.local:8000/
# curl http://todo-frontend.todo-app.svc.cluster.local:80/
```