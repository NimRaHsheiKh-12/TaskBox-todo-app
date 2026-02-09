# PowerShell script to deploy the Todo application to Kubernetes
# This script assumes you have Docker, kubectl, and Helm installed

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("docker-desktop", "minikube")]
    [string]$ClusterType = "docker-desktop",

    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev",

    [Parameter(Mandatory=$false)]
    [string]$Namespace = "todo-app"
)

Write-Host "🚀 Starting deployment of Todo application to Kubernetes..." -ForegroundColor Green

# Function to check if required tools are installed
function Test-CommandExists {
    param (
        [string]$Command
    )

    $result = Get-Command $Command -ErrorAction SilentlyContinue
    return ($null -ne $result)
}

# Check if required tools are installed
$requiredTools = @("docker", "kubectl", "helm")
foreach ($tool in $requiredTools) {
    if (!(Test-CommandExists -Command $tool)) {
        Write-Error "$tool is not installed or not in PATH. Please install $tool and try again."
        exit 1
    }
}

# Function to check if running as Administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check if running as Administrator for Minikube
if ($ClusterType -eq "minikube" -and !(Test-Administrator)) {
    Write-Warning "⚠️  Running Minikube requires Administrator privileges. Please run this script as Administrator."
    $continue = Read-Host "Do you want to continue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        exit 0
    }
}

# Start the appropriate cluster
switch ($ClusterType) {
    "docker-desktop" {
        Write-Host "🐳 Using Docker Desktop Kubernetes..." -ForegroundColor Cyan

        # Verify Docker Desktop Kubernetes is enabled
        try {
            $clusterInfo = kubectl cluster-info 2>$null
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Docker Desktop Kubernetes is not enabled or not accessible. Please ensure Docker Desktop with Kubernetes is running."
                exit 1
            } else {
                Write-Host "✅ Docker Desktop Kubernetes is accessible" -ForegroundColor Green
            }
        } catch {
            Write-Error "Failed to connect to Kubernetes cluster. Please ensure Docker Desktop with Kubernetes is running."
            exit 1
        }
    }
    "minikube" {
        Write-Host "🐹 Starting Minikube cluster..." -ForegroundColor Cyan

        # Attempt to start Minikube
        try {
            Write-Host "Attempting to start Minikube with Hyper-V driver..." -ForegroundColor Yellow
            minikube start --driver=hyperv --cpus=2 --memory=4096mb --disk-size=20g 2>$null
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Hyper-V failed, trying with VirtualBox driver..."
                minikube start --driver=virtualbox --cpus=2 --memory=4096mb --disk-size=20g 2>$null
                if ($LASTEXITCODE -ne 0) {
                    Write-Error "Failed to start Minikube with both Hyper-V and VirtualBox drivers."
                    exit 1
                }
            }

            # Enable ingress addon
            Write-Host "Enabling ingress addon..." -ForegroundColor Yellow
            minikube addons enable ingress 2>$null
            Write-Host "✅ Minikube cluster is running" -ForegroundColor Green
        } catch {
            Write-Error "Failed to start Minikube cluster: $_"
            exit 1
        }
    }
}  # This is the closing brace for the switch statement

# Build Docker images
Write-Host "📦 Building Docker images..." -ForegroundColor Cyan

# Check if Dockerfiles exist
if (!(Test-Path "Dockerfile.frontend")) {
    Write-Error "Dockerfile.frontend not found in current directory"
    exit 1
}

if (!(Test-Path "Dockerfile.backend")) {
    Write-Error "Dockerfile.backend not found in current directory"
    exit 1
}

# Build frontend image
Write-Host "Building frontend image..." -ForegroundColor Yellow
docker build -f Dockerfile.frontend -t todo-frontend:latest . 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build frontend image"
    exit 1
}

# Build backend image
Write-Host "Building backend image..." -ForegroundColor Yellow
docker build -f Dockerfile.backend -t todo-backend:latest . 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build backend image"
    exit 1
}

# Load images into cluster if using Minikube
if ($ClusterType -eq "minikube") {
    Write-Host "📥 Loading images into Minikube..." -ForegroundColor Cyan
    Write-Host "Loading frontend image..." -ForegroundColor Yellow
    minikube image load todo-frontend:latest 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to load frontend image into Minikube"
        exit 1
    }

    Write-Host "Loading backend image..." -ForegroundColor Yellow
    minikube image load todo-backend:latest 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to load backend image into Minikube"
        exit 1
    }
}

# Create namespace if it doesn't exist
Write-Host "🌐 Ensuring namespace '$Namespace' exists..." -ForegroundColor Cyan
$namespaceExists = kubectl get namespace $Namespace -o json 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating namespace '$Namespace'..." -ForegroundColor Yellow
    kubectl create namespace $Namespace 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create namespace '$Namespace'"
        exit 1
    }
    Write-Host "✅ Namespace '$Namespace' created" -ForegroundColor Green
} else {
    Write-Host "✅ Namespace '$Namespace' already exists" -ForegroundColor Green
}

# Determine values file based on environment
$valuesFile = ".\helm\todo-app\values.yaml"
if ($Environment -eq "dev") {
    $valuesFile = ".\helm\todo-app\values-dev.yaml"
    # Create a basic dev values file if it doesn't exist
    if (!(Test-Path $valuesFile)) {
        Write-Host "Creating development values file..." -ForegroundColor Yellow
        $devValuesContent = "frontend:`n  replicaCount: 1`n  image:`n    repository: todo-frontend`n    tag: latest`n    pullPolicy: Never  # Use local images`n  service:`n    type: NodePort`n    port: 80`n  resources:`n    requests:`n      memory: `"64Mi`"`n      cpu: `"100m`"`n    limits:`n      memory: `"128Mi`"`n      cpu: `"200m`"`n`nbackend:`n  replicaCount: 1`n  image:`n    repository: todo-backend`n    tag: latest`n    pullPolicy: Never  # Use local images`n  service:`n    type: ClusterIP`n    port: 8000`n  resources:`n    requests:`n      memory: `"128Mi`"`n      cpu: `"200m`"`n    limits:`n      memory: `"256Mi`"`n      cpu: `"400m`"`n`ningress:`n  enabled: true`n  className: `"`"`n  annotations: {}`n    # kubernetes.io/ingress.class: nginx`n    # kubernetes.io/tls-acme: `"true`"`n  hosts:`n    - host: todo.local`n      paths:`n        - path: /`n          pathType: Prefix`n        - path: /api`n          pathType: Prefix`n  tls: []"
        $devValuesContent | Out-File -FilePath $valuesFile -Encoding utf8
    }
} elseif ($Environment -eq "prod") {
    $valuesFile = ".\helm\todo-app\values-prod.yaml"
    if (!(Test-Path $valuesFile)) {
        Write-Warning "Production values file does not exist at $valuesFile"
    }
}

# Check if Helm chart exists
if (!(Test-Path ".\helm\todo-app")) {
    Write-Error "Helm chart not found at .\helm\todo-app"
    exit 1
}

# Install or upgrade Helm chart
Write-Host "🚢 Installing/Upgrading Helm chart..." -ForegroundColor Cyan

# Check if release already exists
$releaseExists = helm list -n $Namespace --filter "todo-app" --short 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to check for existing Helm release"
    exit 1
}

$helmArgs = @()
if ($releaseExists) {
    Write-Host "🔄 Upgrading existing Helm release..." -ForegroundColor Yellow
    $helmArgs = @("upgrade", "todo-app", ".\helm\todo-app", "--values", $valuesFile, "--namespace", $Namespace, "--wait", "--timeout", "10m", "--atomic")
} else {
    Write-Host "🔄 Installing new Helm release..." -ForegroundColor Yellow
    $helmArgs = @("install", "todo-app", ".\helm\todo-app", "--values", $valuesFile, "--create-namespace", "--namespace", $Namespace, "--wait", "--timeout", "10m", "--atomic")
}

# Execute Helm command
& helm @helmArgs 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install/upgrade Helm chart"
    exit 1
}

# Wait for deployments to be ready
Write-Host "⏳ Waiting for deployments to be ready..." -ForegroundColor Yellow

# Wait for frontend deployment
Write-Host "Waiting for frontend deployment..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=todo-frontend -n $Namespace --timeout=300s 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Frontend deployment might still be initializing..."
}

# Wait for backend deployment
Write-Host "Waiting for backend deployment..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=todo-backend -n $Namespace --timeout=300s 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Backend deployment might still be initializing..."
}

# Show deployment status
Write-Host "`n✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host "📊 Deployment status:" -ForegroundColor Cyan
kubectl get pods,svc,ingress -n $Namespace

# Get service information
$frontendSvc = kubectl get svc todo-frontend -n $Namespace -o json 2>$null | ConvertFrom-Json
$backendSvc = kubectl get svc todo-backend -n $Namespace -o json 2>$null | ConvertFrom-Json

# Provide access information based on cluster type
Write-Host "`n🌐 To access the application:" -ForegroundColor Cyan

if ($ClusterType -eq "minikube") {
    $minikubeIP = minikube ip 2>$null
    Write-Host "Minikube IP: $minikubeIP" -ForegroundColor White

    # Get NodePort for frontend
    $frontendPort = $frontendSvc.spec.ports[0].nodePort
    Write-Host "Frontend: http://$minikubeIP`:$frontendPort" -ForegroundColor White

    # Get NodePort for backend
    $backendPort = $backendSvc.spec.ports[0].nodePort
    Write-Host "Backend: http://$minikubeIP`:$backendPort" -ForegroundColor White
} else {
    # For Docker Desktop, use port forwarding
    Write-Host "For Docker Desktop, use port forwarding:" -ForegroundColor White
    Write-Host "kubectl port-forward svc/todo-frontend -n $Namespace 8080:80" -ForegroundColor White
    Write-Host "Then access the application at http://localhost:8080" -ForegroundColor White
    Write-Host "" -ForegroundColor White
    Write-Host "Or access the backend at:" -ForegroundColor White
    Write-Host "kubectl port-forward svc/todo-backend -n $Namespace 8000:8000" -ForegroundColor White
}

Write-Host "`n🎉 Your Todo application is now deployed on Kubernetes!" -ForegroundColor Green