import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel, Field
from redis import asyncio, RedisError
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Default model path - can be overridden with environment variable
MODEL_PATH = os.environ.get("MODEL_PATH", "../model/distilbert-base-uncased-finetuned-sst2")

# Load the model, tokenizer, and create a classification pipeline
try:
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    classifier = pipeline(
        task="text-classification",
        model=model,
        tokenizer=tokenizer,
        device=-1,  # Use CPU (-1) by default
        top_k=None,  # Return all class scores
    )
except Exception as e:
    # Log the error but don't crash - will show more specific error when API is used
    logging.error(f"Failed to load model: {str(e)}")
    model = None
    tokenizer = None
    classifier = None

# Configure logging
logger = logging.getLogger(__name__)
LOCAL_REDIS_URL = "redis://localhost:6379"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager that initializes the Redis cache connection
    """
    # Get Redis URL from environment or use default local URL
    redis_url = os.environ.get("REDIS_URL", LOCAL_REDIS_URL)
    logger.info(f"Connecting to Redis at {redis_url}")
    
    try:
        # Connect to Redis
        redis = asyncio.from_url(redis_url, encoding="utf8", decode_responses=True)
        # Initialize FastAPI cache with Redis backend
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache-fastsent")
        logger.info("Redis cache initialized successfully")
    except RedisError as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        # Continue without caching if Redis is unavailable
    
    yield


# Create FastAPI sub-application
sub_application_sentiment_predict = FastAPI(
    title="FastSentiment API",
    description="High-performance sentiment analysis endpoints using DistilBERT",
    lifespan=lifespan,
)


class SentimentRequest(BaseModel):
    """
    Request model for sentiment analysis
    """
    text: list[str] = Field(
        ..., 
        description="List of text strings to analyze for sentiment",
        example=["I love this product!", "This is terrible."]
    )


class Sentiment(BaseModel):
    """
    Model for individual sentiment prediction
    """
    label: str = Field(..., description="Sentiment label (POSITIVE or NEGATIVE)")
    score: float = Field(..., description="Confidence score (0-1)")


class SentimentResponse(BaseModel):
    """
    Response model for sentiment analysis predictions
    """
    predictions: list[list[Sentiment]] = Field(
        ..., 
        description="List of sentiment predictions for each input text"
    )


@sub_application_sentiment_predict.post(
    "/bulk-predict", 
    response_model=SentimentResponse,
    summary="Predict sentiment for multiple texts",
    description="Analyze the sentiment of multiple text inputs and return predictions"
)
@cache(expire=300)  # Cache results for 5 minutes
async def predict(sentiments: SentimentRequest):
    """
    Predict sentiment for a list of text inputs
    """
    # Check if model was loaded successfully
    if classifier is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not available. Please check server logs."
        )
    
    try:
        # Run prediction with the classifier
        predictions = classifier(sentiments.text)
        return {"predictions": predictions}
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during prediction: {str(e)}"
        )


@sub_application_sentiment_predict.get(
    "/health",
    summary="Check API health",
    description="Verify that the API and model are functioning correctly"
)
async def health():
    """
    Health check endpoint to verify the API is running
    """
    # Check if model is loaded
    model_status = "healthy" if classifier is not None else "unavailable"
    
    return {
        "status": "healthy",
        "model": model_status,
        "version": "1.0.0"
    }