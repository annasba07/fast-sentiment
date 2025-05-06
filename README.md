# FastSentiment

A high-performance sentiment analysis API built with FastAPI, PyTorch, and Hugging Face Transformers. FastSentiment demonstrates how to deploy machine learning models as efficient, scalable APIs with advanced caching, containerization, and cloud-native infrastructure.

<p align="center">
    <!--Hugging Face-->
    <img src="https://user-images.githubusercontent.com/1393562/197941700-78283534-4e68-4429-bf94-dce7ab43a941.svg" width=7% alt="Hugging Face">
    <!--PLUS SIGN-->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width=7% alt="Plus">
    <!--FASTAPI-->
    <img src="https://user-images.githubusercontent.com/1393562/190876570-16dff98d-ccea-4a57-86ef-a161539074d6.svg" width=7% alt="FastAPI">
    <!--PLUS SIGN-->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width=7% alt="Plus">
    <!--REDIS LOGO-->
    <img src="https://user-images.githubusercontent.com/1393562/190876644-501591b7-809b-469f-b039-bb1a287ed36f.svg" width=7% alt="Redis">
    <!--PLUS SIGN-->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width=7% alt="Plus">
    <!--KUBERNETES-->
    <img src="https://user-images.githubusercontent.com/1393562/190876683-9c9d4f44-b9b2-46f0-a631-308e5a079847.svg" width=7% alt="Kubernetes">
</p>

## Features

- **Natural Language Processing**: Sentiment analysis using fine-tuned DistilBERT model
- **Modern API**: FastAPI with automatic OpenAPI documentation
- **Performance Optimization**:
  - Redis caching to reduce load and improve response times
  - Model bundled at build time for faster container startup
- **Horizontal Scaling**: Kubernetes ready with efficient resource utilization
- **Monitoring & Testing**: Includes load testing scripts and metrics collection
- **Container-based**: Docker for consistent development and deployment

## Model Architecture

This project leverages [DistilBERT](https://arxiv.org/abs/1910.01108), a compressed version of BERT optimized for speed and efficiency while maintaining high performance. The model has been fine-tuned on the SST-2 dataset for sentiment analysis.

## API Usage

The API accepts text input and returns sentiment predictions:

### Request Format
```json
{
    "text": ["example text 1", "example text 2"]
}
```

### Response Format
```json
{
    "predictions": [
        [
            {
                "label": "POSITIVE",
                "score": 0.7127904295921326
            },
            {
                "label": "NEGATIVE",
                "score": 0.2872096002101898
            }
        ],
        [
            {
                "label": "POSITIVE",
                "score": 0.7186233401298523
            },
            {
                "label": "NEGATIVE",
                "score": 0.2813767194747925
            }
        ]
    ]
}
```

## Getting Started

### Download the Model

Before running the application, you'll need to download the fine-tuned DistilBERT model:

```bash
git lfs install
git clone https://huggingface.co/winegarj/distilbert-base-uncased-finetuned-sst2 model/distilbert-base-uncased-finetuned-sst2
```

### Local Development

1. Install dependencies:
```bash
cd app
poetry install
```

2. Run Redis for caching:
```bash
docker run -d --name redis -p 6379:6379 redis:alpine
```

3. Run the API locally:
```bash
cd app
poetry run uvicorn src.main:app --reload
```

4. Access the API documentation at http://localhost:8000/docs

### Docker Deployment

Build and run with Docker:

```bash
docker build -t sentiment-analysis-api ./app
docker run -p 8000:8000 --name sentiment-api sentiment-analysis-api
```

### Kubernetes Deployment

Deploy to Kubernetes:

```bash
cd deployment/kubernetes
kubectl apply -k .
```

## Performance

The API is optimized for performance:

- Processes 10+ requests/second under load
- p99 latency under 2 seconds at 10 concurrent users
- 95% cache hit rate reduces load on the model
- Horizontally scalable to handle increased traffic

## Load Testing

Load tests are included in the `/load-testing` directory:

```bash
cd load-testing
k6 run --summary-trend-stats "min,avg,med,max,p(90),p(95),p(99)" load.js
```

## Architecture

The application follows clean architecture principles:

- `src/main.py` - FastAPI application setup
- `src/sentiment_predict.py` - Model loading and prediction endpoints
- `model/` - Pre-trained model files
- `deployment/` - Kubernetes and deployment configuration

## License

MIT