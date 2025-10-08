# SEC Filing Processor - Apache Spark on Kubernetes

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
