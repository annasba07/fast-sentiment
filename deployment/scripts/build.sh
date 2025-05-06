#!/bin/bash
set -e

# Default values
DOCKER_REGISTRY="localhost:5000"
IMAGE_NAME="fast-sentiment"
IMAGE_TAG="latest"
BUILD_DIR="../../app"
MODEL_DIR="../../model/distilbert-base-uncased-finetuned-sst2"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --registry)
      DOCKER_REGISTRY="$2"
      shift
      shift
      ;;
    --tag)
      IMAGE_TAG="$2"
      shift
      shift
      ;;
    --help)
      echo "Usage: $0 [OPTIONS]"
      echo "Build Docker image for FastSentiment"
      echo ""
      echo "Options:"
      echo "  --registry REGISTRY    Docker registry to use (default: localhost:5000)"
      echo "  --tag TAG              Image tag (default: latest)"
      echo "  --help                 Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Full image name with registry and tag
FULL_IMAGE_NAME="${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"

# Check if model directory exists
if [ ! -d "$MODEL_DIR" ]; then
  echo "Model directory not found: $MODEL_DIR"
  echo "Please download the model first. See model/README.md for instructions."
  exit 1
fi

# Build the Docker image
echo "Building Docker image: $FULL_IMAGE_NAME"
docker build -t "$FULL_IMAGE_NAME" \
  --build-arg MODEL_PATH="$MODEL_DIR" \
  "$BUILD_DIR"

echo "Image built successfully: $FULL_IMAGE_NAME"

# Push the image to the registry if not local
if [ "$DOCKER_REGISTRY" != "localhost:5000" ]; then
  echo "Pushing image to registry: $DOCKER_REGISTRY"
  docker push "$FULL_IMAGE_NAME"
  echo "Image pushed successfully"
fi

echo "Build process completed successfully!"