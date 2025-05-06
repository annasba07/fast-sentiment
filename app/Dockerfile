# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set build arguments and environment variables
ARG MODEL_PATH="../model/distilbert-base-uncased-finetuned-sst2"
ENV MODEL_PATH="/app/model"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install --no-cache-dir poetry==1.6.1

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Install dependencies without dev dependencies
RUN poetry install --without dev --no-root

# Copy application code
COPY src ./src
COPY tests ./tests

# Copy the model files - these should be downloaded before building the image
COPY ${MODEL_PATH} ./model

# Create non-root user for security
RUN adduser --disabled-password --gecos "" appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose the application port
EXPOSE 8000

# Set health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run the FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]