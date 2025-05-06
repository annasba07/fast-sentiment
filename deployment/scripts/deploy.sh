#!/bin/bash
set -e

# Default values
DOCKER_REGISTRY="localhost:5000"
IMAGE_TAG="latest"
NAMESPACE="fast-sentiment"
KUBE_CONTEXT=""
KUBE_CONFIG_PATH=""

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
    --namespace)
      NAMESPACE="$2"
      shift
      shift
      ;;
    --context)
      KUBE_CONTEXT="$2"
      shift
      shift
      ;;
    --kubeconfig)
      KUBE_CONFIG_PATH="$2"
      shift
      shift
      ;;
    --help)
      echo "Usage: $0 [OPTIONS]"
      echo "Deploy FastSentiment to Kubernetes"
      echo ""
      echo "Options:"
      echo "  --registry REGISTRY    Docker registry to use (default: localhost:5000)"
      echo "  --tag TAG              Image tag (default: latest)"
      echo "  --namespace NAMESPACE  Kubernetes namespace (default: fast-sentiment)"
      echo "  --context CONTEXT      Kubernetes context to use"
      echo "  --kubeconfig PATH      Path to kubeconfig file"
      echo "  --help                 Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Set kubectl context and config if provided
if [ -n "$KUBE_CONTEXT" ]; then
  KUBECTL="kubectl --context $KUBE_CONTEXT"
else
  KUBECTL="kubectl"
fi

if [ -n "$KUBE_CONFIG_PATH" ]; then
  KUBECTL="$KUBECTL --kubeconfig $KUBE_CONFIG_PATH"
fi

# Create namespace if it doesn't exist
echo "Ensuring namespace $NAMESPACE exists"
$KUBECTL get namespace $NAMESPACE >/dev/null 2>&1 || $KUBECTL create namespace $NAMESPACE

# Apply kustomization with the specified image and registry
echo "Deploying application to namespace $NAMESPACE"
cd ../kubernetes

# Set up the environment variable for kustomize
DOCKER_REGISTRY=$DOCKER_REGISTRY \
$KUBECTL apply -k . -n $NAMESPACE

echo "Deployment initiated. Checking status..."

# Wait for deployment to be ready
$KUBECTL rollout status deployment/fast-sentiment -n $NAMESPACE

echo "Deployment completed successfully!"
echo ""
echo "You can access the API at: https://fast-sentiment.example.com/api/bulk-predict"
echo "Or via port forwarding:"
echo "  kubectl port-forward svc/fast-sentiment-service 8000:8000 -n $NAMESPACE"
echo "  Then visit: http://localhost:8000/api/bulk-predict"