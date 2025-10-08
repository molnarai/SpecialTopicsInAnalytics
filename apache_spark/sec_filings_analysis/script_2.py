# Create additional configuration files and documentation

# 1. Create an advanced configuration file
config_file = '''# SEC Filing Processor Configuration
# Advanced settings for Spark on Kubernetes with NLP processing

# ==============================================================================
# APPLICATION SETTINGS
# ==============================================================================
app:
  name: "sec-filing-processor"
  version: "1.0.0"
  log_level: "INFO"

# ==============================================================================
# KUBERNETES SETTINGS  
# ==============================================================================
kubernetes:
  namespace: "spark-nlp"
  service_account: "spark-service-account"
  image_pull_policy: "Always"
  
# ==============================================================================
# DOCKER IMAGE SETTINGS
# ==============================================================================
docker:
  registry: "your-registry.com"
  image_name: "sec-filing-spark"
  tag: "latest"
  
# ==============================================================================
# SPARK CONFIGURATION
# ==============================================================================
spark:
  driver:
    memory: "2g"
    cores: "1"
    max_result_size: "1g"
  
  executor:
    memory: "4g"
    cores: "2"
    instances: "4"
    memory_overhead: "512m"
  
  # Dynamic allocation settings
  dynamic_allocation:
    enabled: true
    min_executors: 2
    max_executors: 20
    initial_executors: 4
    
  # Performance tuning
  sql:
    adaptive:
      enabled: true
      coalesce_partitions: true
      skip_skewed_join: true
  
  serializer: "org.apache.spark.serializer.KryoSerializer"
  
# ==============================================================================
# S3 CONFIGURATION
# ==============================================================================
s3:
  input_path: "s3a://your-sec-filings-bucket/input/"
  output_path: "s3a://your-sec-filings-bucket/output/"
  checkpoint_path: "s3a://your-sec-filings-bucket/checkpoints/"
  
  # S3A Configuration
  s3a:
    impl: "org.apache.hadoop.fs.s3a.S3AFileSystem"
    fast_upload: true
    multipart_size: "104857600"  # 100MB
    multipart_threshold: "2147483647"  # 2GB
    connection_maximum: "15"

# ==============================================================================
# NLP PROCESSING SETTINGS
# ==============================================================================
nlp:
  # SpaCy model settings
  spacy:
    model: "en_core_web_sm"
    max_length: 1000000  # Max text length for processing
    
  # Entity types to extract
  entity_types:
    - "PERSON"
    - "ORG" 
    - "GPE"
    - "MONEY"
    - "PERCENT"
    - "DATE"
    - "CARDINAL"
    
  # Text processing settings
  processing:
    max_paragraph_length: 2000
    min_paragraph_length: 50
    sentence_split_threshold: 1000

# ==============================================================================
# MONITORING AND LOGGING
# ==============================================================================
monitoring:
  metrics_enabled: true
  history_server_enabled: true
  event_log_enabled: true
  
logging:
  level: "INFO"
  pattern: "%d{yyyy-MM-dd HH:mm:ss} %-5level %logger{36} - %msg%n"
'''

# Save configuration file
with open('config.yaml', 'w') as f:
    f.write(config_file)

# 2. Create a Kubernetes pod template for advanced configurations
pod_template = '''apiVersion: v1
kind: Pod
metadata:
  labels:
    app: sec-filing-processor
    version: v1.0.0
spec:
  # Security context
  securityContext:
    runAsNonRoot: true
    runAsUser: 185
    fsGroup: 185
    
  # Node selector for specific node types
  nodeSelector:
    workload-type: "spark"
    
  # Tolerations for tainted nodes
  tolerations:
  - key: "spark-workload"
    operator: "Equal"
    value: "true"
    effect: "NoSchedule"
    
  # Affinity rules
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
          - key: instance-type
            operator: In
            values:
            - "memory-optimized"
            - "compute-optimized"
    
    # Pod anti-affinity to spread executors across nodes
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: spark-role
              operator: In
              values:
              - executor
          topologyKey: kubernetes.io/hostname
          
  containers:
  - name: spark
    # Resource limits and requests
    resources:
      requests:
        memory: "4Gi"
        cpu: "2000m"
      limits:
        memory: "4Gi"
        cpu: "2000m"
        
    # Environment variables
    env:
    - name: SPARK_USER
      value: "spark"
    - name: PYTHONPATH
      value: "/app:/opt/spark/python/lib/pyspark.zip:/opt/spark/python/lib/py4j-0.10.9.5-src.zip"
      
    # Volume mounts
    volumeMounts:
    - name: spark-local-dir
      mountPath: /tmp/spark-local
    - name: nlp-models
      mountPath: /opt/nlp-models
      readOnly: true
      
    # Liveness and readiness probes
    livenessProbe:
      exec:
        command:
        - /bin/sh
        - -c
        - "ps aux | grep -v grep | grep java"
      initialDelaySeconds: 30
      periodSeconds: 30
      timeoutSeconds: 10
      
  # Volumes
  volumes:
  - name: spark-local-dir
    emptyDir:
      sizeLimit: "10Gi"
  - name: nlp-models
    configMap:
      name: nlp-models-config
      
  # DNS configuration
  dnsPolicy: ClusterFirst
  dnsConfig:
    options:
    - name: ndots
      value: "2"
    - name: edns0
'''

# Save pod template
with open('pod-template.yaml', 'w') as f:
    f.write(pod_template)

# 3. Create a requirements.txt file with pinned versions
requirements_content = '''# SEC Filing Processor Dependencies
# Pinned versions for reproducible builds

# Core Spark dependencies
pyspark==3.5.0

# NLP Processing Libraries
beautifulsoup4==4.12.2
nltk==3.8.1
spacy==3.7.2
lxml==4.9.3
html5lib==1.1

# SpaCy language models (downloaded separately)
# en-core-web-sm==3.7.1

# AWS Integration
boto3==1.29.57
botocore==1.32.57
s3fs==2023.10.0

# Data Processing
pandas==2.1.3
numpy==1.24.3
pyarrow==14.0.1

# Text Processing Utilities
regex==2023.10.3
textblob==0.17.1
python-dateutil==2.8.2

# HTTP and Web Utilities
requests==2.31.0
urllib3==2.0.7

# Configuration Management
PyYAML==6.0.1

# Logging and Monitoring
py4j==0.10.9.7

# Development and Testing (optional)
pytest==7.4.3
pytest-cov==4.1.0

# Optional: GPU support for SpaCy (uncomment if using GPU nodes)
# cupy-cuda12x==12.3.0
'''

# Save requirements file
with open('requirements.txt', 'w') as f:
    f.write(requirements_content)

# 4. Create a sample Dockerfile with multi-stage build
dockerfile_content = '''# Multi-stage Dockerfile for SEC Filing Processor
# Optimized for production deployment with minimal image size

# =============================================================================
# Stage 1: Build stage - Download and prepare dependencies
# =============================================================================
FROM python:3.10-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    wget \\
    curl \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Download SpaCy model
RUN python -m spacy download en_core_web_sm

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt', download_dir='/opt/nltk_data'); nltk.download('averaged_perceptron_tagger', download_dir='/opt/nltk_data')"

# =============================================================================
# Stage 2: Production stage - Minimal runtime image
# =============================================================================
FROM apache/spark:3.5.0-python3

# Switch to root for installation
USER root

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y \\
    libgomp1 \\
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy NLTK data
COPY --from=builder /opt/nltk_data /opt/nltk_data
ENV NLTK_DATA=/opt/nltk_data

# Set working directory
WORKDIR /app

# Copy application code
COPY sec_filing_processor.py .
COPY config.yaml .

# Create directories for Spark local storage
RUN mkdir -p /tmp/spark-local /tmp/spark-events
RUN chmod 777 /tmp/spark-local /tmp/spark-events

# Set proper permissions
RUN chown -R spark:spark /app /opt/venv /opt/nltk_data

# Switch back to spark user
USER spark

# Set environment variables
ENV SPARK_USER=spark
ENV PYTHONPATH="/app:/opt/spark/python/lib/pyspark.zip:/opt/spark/python/lib/py4j-0.10.9.5-src.zip"
ENV SPARK_LOCAL_DIRS="/tmp/spark-local"
ENV SPARK_LOG_DIR="/tmp/spark-events"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
  CMD python -c "import pyspark, spacy, nltk, bs4; print('Dependencies OK')" || exit 1

# Default entrypoint from parent image
# ENTRYPOINT ["/opt/entrypoint.sh"]
'''

# Save Dockerfile
with open('Dockerfile', 'w') as f:
    f.write(dockerfile_content)

# 5. Create a README with usage instructions
readme_content = '''# SEC Filing Processor - Apache Spark on Kubernetes

A distributed NLP pipeline for processing SEC filings using Apache Spark 4.0.1 on Kubernetes with Beautiful Soup, NLTK, and SpaCy.

## 🚀 Features

- **Scalable Processing**: Distributed processing of large SEC filing datasets
- **Advanced NLP**: Named entity recognition and paragraph extraction using SpaCy
- **HTML Cleaning**: Beautiful Soup integration for clean text extraction
- **Cloud Native**: Kubernetes-native deployment with auto-scaling
- **S3 Integration**: Direct integration with AWS S3 for data storage
- **Production Ready**: Multi-stage Docker builds, health checks, and monitoring

## 📋 Prerequisites

- Kubernetes cluster (v1.20+)
- kubectl configured and connected to your cluster
- Docker for building images
- Apache Spark 4.0.1+ support in your cluster
- AWS S3 access (for data storage)

## 🏗️ Architecture

```
S3 Input → Spark Driver → [Executor Pods] → NLP Processing → S3 Output
           (Kubernetes)    (Beautiful Soup)
                          (NLTK + SpaCy)
                          (Entity Extraction)
```

## 🛠️ Quick Start

1. **Clone and Configure**
   ```bash
   # Update configuration in config.yaml
   # Set your S3 paths, Kubernetes settings, etc.
   ```

2. **Deploy and Run**
   ```bash
   # Full pipeline: build, deploy, and run
   ./deploy_spark_k8s.sh submit
   
   # Or step by step:
   ./deploy_spark_k8s.sh build    # Build Docker image
   ./deploy_spark_k8s.sh setup    # Setup K8s resources
   ./deploy_spark_k8s.sh submit   # Submit Spark job
   ```

3. **Monitor Job**
   ```bash
   ./deploy_spark_k8s.sh monitor  # Watch job execution
   ./deploy_spark_k8s.sh status   # Get current status
   ```

4. **Cleanup**
   ```bash
   ./deploy_spark_k8s.sh cleanup  # Remove resources
   ```

## 📁 File Structure

```
├── sec_filing_processor.py    # Main Spark application
├── deploy_spark_k8s.sh       # Deployment script
├── config.yaml               # Configuration file
├── requirements.txt          # Python dependencies
├── Dockerfile               # Multi-stage Docker build
├── pod-template.yaml        # K8s pod template
└── README.md               # This file
```

## ⚙️ Configuration

### Spark Settings
- **Driver**: 2GB memory, 1 core
- **Executors**: 4GB memory, 2 cores each
- **Dynamic Allocation**: 2-20 executors
- **Adaptive Query Execution**: Enabled

### NLP Processing
- **SpaCy Model**: en_core_web_sm
- **Entity Types**: PERSON, ORG, GPE, MONEY, PERCENT
- **Text Cleaning**: HTML tag removal, whitespace normalization

### Kubernetes
- **Namespace**: spark-nlp
- **Service Account**: RBAC enabled
- **Resource Management**: Requests and limits defined
- **Pod Templates**: Advanced scheduling and affinity rules

## 🔧 Advanced Usage

### Custom Entity Types
```python
# Edit sec_filing_processor.py
entity_types = ['PERSON', 'ORG', 'GPE', 'MONEY', 'PERCENT', 'LAW', 'PRODUCT']
```

### GPU Support
```bash
# Uncomment cupy in requirements.txt
# Add GPU resource requests in pod template
```

### Different SpaCy Models
```python
# Use larger models for better accuracy
nlp = spacy.load("en_core_web_lg")  # or en_core_web_md
```

## 📊 Output Format

The processor outputs CSV files with the following schema:
- `filename`: Source SEC filing filename
- `entity_text`: Extracted entity text
- `entity_label`: Entity type (PERSON, ORG, etc.)
- `paragraph_id`: Paragraph identifier
- `paragraph_text`: Full paragraph containing the entity
- `entity_start`: Start position in original text
- `entity_end`: End position in original text

## 🐛 Troubleshooting

### Common Issues

1. **Pod Scheduling Issues**
   - Check node resources and taints
   - Review pod template affinity rules

2. **S3 Access Denied**
   - Verify AWS credentials in ConfigMap
   - Check S3 bucket policies

3. **SpaCy Model Loading**
   - Ensure model is downloaded in Docker build
   - Check available disk space on nodes

4. **Memory Issues**
   - Adjust executor memory settings
   - Enable dynamic allocation
   - Review GC settings

### Debugging Commands

```bash
# Check pod logs
kubectl logs <driver-pod-name> -n spark-nlp

# Describe pod issues
kubectl describe pod <pod-name> -n spark-nlp

# Check resource usage
kubectl top pods -n spark-nlp

# Access Spark UI
kubectl port-forward <driver-pod-name> 4040:4040 -n spark-nlp
```

## 🚀 Performance Tuning

### For Large Datasets
```yaml
spark:
  executor:
    memory: "8g"
    instances: "10"
  sql:
    shuffle:
      partitions: 400
```

### For Better NLP Performance
```python
# Process in smaller chunks
# Enable text preprocessing caching
# Use distributed spaCy processing
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0.
'''

# Save README
with open('README.md', 'w') as f:
    f.write(readme_content)

print("✅ Created additional configuration files:")
print("📄 config.yaml - Application configuration")
print("🐳 Dockerfile - Multi-stage Docker build")
print("📋 requirements.txt - Python dependencies")
print("☸️  pod-template.yaml - Kubernetes pod template")
print("📖 README.md - Complete documentation")
print("\n🎉 All files are ready for deployment!")