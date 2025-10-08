# Multi-stage Dockerfile for SEC Filing Processor
# Optimized for production deployment with minimal image size

# =============================================================================
# Stage 1: Build stage - Download and prepare dependencies
# =============================================================================
FROM python:3.10-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    gcc \
    g++ \
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
RUN apt-get update && apt-get install -y \
    libgomp1 \
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
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import pyspark, spacy, nltk, bs4; print('Dependencies OK')" || exit 1

# Default entrypoint from parent image
# ENTRYPOINT ["/opt/entrypoint.sh"]
