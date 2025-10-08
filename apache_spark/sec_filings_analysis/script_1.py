# Create the bash script for Kubernetes deployment and job submission
bash_script = '''#!/bin/bash

# SEC Filing Processing - Spark on Kubernetes Deployment Script
# Apache Spark 4.0.1 on Kubernetes with NLP Dependencies

set -e  # Exit on any error

# Configuration Variables
SPARK_APP_NAME="sec-filing-processor"
KUBERNETES_NAMESPACE="spark-nlp"
DOCKER_IMAGE="sec-filing-spark:latest"
DOCKER_REGISTRY="your-registry.com"
S3_INPUT_PATH="s3a://your-sec-filings-bucket/input/"
S3_OUTPUT_PATH="s3a://your-sec-filings-bucket/output/"
SPARK_DRIVER_MEMORY="2g"
SPARK_EXECUTOR_MEMORY="4g"
SPARK_EXECUTOR_CORES="2"
SPARK_EXECUTOR_INSTANCES="4"
KUBERNETES_CONTEXT="your-k8s-context"

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    log_header "Checking Prerequisites"
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    
    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check if we can connect to Kubernetes cluster
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        log_error "Please check your kubectl configuration"
        exit 1
    fi
    
    # Check Kubernetes context
    current_context=$(kubectl config current-context)
    log_info "Current Kubernetes context: $current_context"
    
    if [[ "$current_context" != "$KUBERNETES_CONTEXT" ]]; then
        log_warn "Current context ($current_context) doesn't match expected ($KUBERNETES_CONTEXT)"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    log_info "Prerequisites check completed"
}

# Function to build Docker image
build_docker_image() {
    log_header "Building Docker Image"
    
    # Create Dockerfile if it doesn't exist
    if [[ ! -f "Dockerfile" ]]; then
        log_info "Creating Dockerfile"
        cat > Dockerfile << 'EOL'
# Dockerfile for SEC Filing Processing with Spark 4.0.1
FROM apache/spark:3.5.0-python3

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    wget \\
    curl \\
    unzip \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download SpaCy model
RUN python -m spacy download en_core_web_sm

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Copy application code
COPY sec_filing_processor.py .

# Set user back to spark
USER spark

# Set entrypoint
ENTRYPOINT ["/opt/entrypoint.sh"]
EOL
    fi
    
    # Create requirements.txt if it doesn't exist
    if [[ ! -f "requirements.txt" ]]; then
        log_info "Creating requirements.txt"
        cat > requirements.txt << 'EOL'
# NLP Processing Dependencies
beautifulsoup4==4.12.2
nltk==3.8.1
spacy==3.7.2
lxml==4.9.3
html5lib==1.1

# AWS S3 Integration
boto3==1.29.57
s3fs==2023.10.0

# Additional utilities
pandas==2.1.3
numpy==1.24.3
requests==2.31.0
EOL
    fi
    
    # Build the image
    log_info "Building Docker image: $DOCKER_IMAGE"
    docker build -t $DOCKER_IMAGE .
    
    # Tag for registry if specified
    if [[ "$DOCKER_REGISTRY" != "your-registry.com" ]]; then
        log_info "Tagging image for registry: $DOCKER_REGISTRY"
        docker tag $DOCKER_IMAGE $DOCKER_REGISTRY/$DOCKER_IMAGE
        
        # Push to registry
        log_info "Pushing image to registry"
        docker push $DOCKER_REGISTRY/$DOCKER_IMAGE
        DOCKER_IMAGE="$DOCKER_REGISTRY/$DOCKER_IMAGE"
    fi
    
    log_info "Docker image build completed"
}

# Function to setup Kubernetes resources
setup_kubernetes_resources() {
    log_header "Setting up Kubernetes Resources"
    
    # Create namespace
    log_info "Creating namespace: $KUBERNETES_NAMESPACE"
    kubectl create namespace $KUBERNETES_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    
    # Create service account and RBAC
    log_info "Setting up RBAC for Spark"
    cat << EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark-service-account
  namespace: $KUBERNETES_NAMESPACE
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: spark-cluster-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "create", "update", "delete", "watch"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: spark-cluster-role-binding
subjects:
- kind: ServiceAccount
  name: spark-service-account
  namespace: $KUBERNETES_NAMESPACE
roleRef:
  kind: ClusterRole
  name: spark-cluster-role
  apiGroup: rbac.authorization.k8s.io
EOF
    
    # Create ConfigMap for AWS credentials (if needed)
    if [[ -n "$AWS_ACCESS_KEY_ID" && -n "$AWS_SECRET_ACCESS_KEY" ]]; then
        log_info "Creating AWS credentials ConfigMap"
        kubectl create configmap aws-credentials \\
            --from-literal=AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \\
            --from-literal=AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \\
            --namespace=$KUBERNETES_NAMESPACE \\
            --dry-run=client -o yaml | kubectl apply -f -
    fi
    
    log_info "Kubernetes resources setup completed"
}

# Function to submit Spark job
submit_spark_job() {
    log_header "Submitting Spark Job to Kubernetes"
    
    # Get Kubernetes API server URL
    K8S_SERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')
    log_info "Kubernetes API Server: $K8S_SERVER"
    
    # Prepare spark-submit command
    SPARK_SUBMIT_CMD="/opt/spark/bin/spark-submit \\
        --master k8s://$K8S_SERVER \\
        --deploy-mode cluster \\
        --name $SPARK_APP_NAME \\
        --class sec_filing_processor \\
        --conf spark.app.name=$SPARK_APP_NAME \\
        --conf spark.kubernetes.namespace=$KUBERNETES_NAMESPACE \\
        --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-service-account \\
        --conf spark.kubernetes.container.image=$DOCKER_IMAGE \\
        --conf spark.kubernetes.container.image.pullPolicy=Always \\
        --conf spark.kubernetes.driver.pod.name=$SPARK_APP_NAME-driver \\
        --conf spark.kubernetes.executor.podNamePrefix=$SPARK_APP_NAME-exec \\
        --conf spark.driver.memory=$SPARK_DRIVER_MEMORY \\
        --conf spark.executor.memory=$SPARK_EXECUTOR_MEMORY \\
        --conf spark.executor.cores=$SPARK_EXECUTOR_CORES \\
        --conf spark.executor.instances=$SPARK_EXECUTOR_INSTANCES \\
        --conf spark.sql.adaptive.enabled=true \\
        --conf spark.sql.adaptive.coalescePartitions.enabled=true \\
        --conf spark.serializer=org.apache.spark.serializer.KryoSerializer \\
        --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \\
        --conf spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider \\
        --py-files local:///app/sec_filing_processor.py \\
        local:///app/sec_filing_processor.py"
    
    # Add AWS credentials if available
    if kubectl get configmap aws-credentials -n $KUBERNETES_NAMESPACE &> /dev/null; then
        SPARK_SUBMIT_CMD+=" \\
        --conf spark.kubernetes.driverEnv.AWS_ACCESS_KEY_ID=\\$(AWS_ACCESS_KEY_ID) \\
        --conf spark.kubernetes.driverEnv.AWS_SECRET_ACCESS_KEY=\\$(AWS_SECRET_ACCESS_KEY) \\
        --conf spark.kubernetes.executorEnv.AWS_ACCESS_KEY_ID=\\$(AWS_ACCESS_KEY_ID) \\
        --conf spark.kubernetes.executorEnv.AWS_SECRET_ACCESS_KEY=\\$(AWS_SECRET_ACCESS_KEY)"
    fi
    
    log_info "Executing Spark submit command..."
    echo "Command: $SPARK_SUBMIT_CMD"
    
    # Submit the job
    eval $SPARK_SUBMIT_CMD
    
    log_info "Spark job submitted successfully"
}

# Function to monitor job
monitor_job() {
    log_header "Monitoring Spark Job"
    
    log_info "Watching pods in namespace $KUBERNETES_NAMESPACE"
    log_info "Press Ctrl+C to stop monitoring"
    
    # Monitor pods
    kubectl get pods -n $KUBERNETES_NAMESPACE -w &
    WATCH_PID=$!
    
    # Wait for driver pod to be ready
    log_info "Waiting for driver pod to be ready..."
    kubectl wait --for=condition=Ready pod/$SPARK_APP_NAME-driver -n $KUBERNETES_NAMESPACE --timeout=300s
    
    # Show driver logs
    log_info "Showing driver pod logs (last 50 lines):"
    kubectl logs $SPARK_APP_NAME-driver -n $KUBERNETES_NAMESPACE --tail=50 -f &
    LOGS_PID=$!
    
    # Trap to cleanup background processes
    trap 'kill $WATCH_PID $LOGS_PID 2>/dev/null || true' EXIT
    
    read -p "Press Enter to stop monitoring..."
    kill $WATCH_PID $LOGS_PID 2>/dev/null || true
}

# Function to get job status
get_job_status() {
    log_header "Job Status"
    
    # Get pod status
    kubectl get pods -n $KUBERNETES_NAMESPACE -l spark-app-selector=$SPARK_APP_NAME
    
    # Get recent logs
    if kubectl get pod $SPARK_APP_NAME-driver -n $KUBERNETES_NAMESPACE &> /dev/null; then
        log_info "Recent driver logs:"
        kubectl logs $SPARK_APP_NAME-driver -n $KUBERNETES_NAMESPACE --tail=20
    fi
}

# Function to cleanup resources
cleanup_resources() {
    log_header "Cleaning up Resources"
    
    log_info "Deleting Spark application pods"
    kubectl delete pods -n $KUBERNETES_NAMESPACE -l spark-app-selector=$SPARK_APP_NAME --ignore-not-found=true
    
    read -p "Delete namespace $KUBERNETES_NAMESPACE? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kubectl delete namespace $KUBERNETES_NAMESPACE --ignore-not-found=true
        log_info "Namespace deleted"
    fi
}

# Main function
main() {
    log_header "SEC Filing Processor - Spark on Kubernetes"
    
    # Parse command line arguments
    case "${1:-submit}" in
        "submit")
            check_prerequisites
            build_docker_image
            setup_kubernetes_resources
            submit_spark_job
            ;;
        "monitor")
            monitor_job
            ;;
        "status")
            get_job_status
            ;;
        "cleanup")
            cleanup_resources
            ;;
        "build")
            build_docker_image
            ;;
        "setup")
            setup_kubernetes_resources
            ;;
        *)
            echo "Usage: $0 {submit|monitor|status|cleanup|build|setup}"
            echo ""
            echo "Commands:"
            echo "  submit   - Full pipeline: build, setup, and submit job (default)"
            echo "  monitor  - Monitor running job"
            echo "  status   - Get current job status"
            echo "  cleanup  - Clean up resources"
            echo "  build    - Build Docker image only"
            echo "  setup    - Setup Kubernetes resources only"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
'''

# Save the bash script
with open('deploy_spark_k8s.sh', 'w') as f:
    f.write(bash_script)

# Make the script executable
import os
os.chmod('deploy_spark_k8s.sh', 0o755)

print("✅ Kubernetes deployment script saved as 'deploy_spark_k8s.sh'")
print("📝 Script is now executable")