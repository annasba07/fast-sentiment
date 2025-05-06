from contextlib import AsyncExitStack

from fastapi import FastAPI

from src.sentiment_predict import lifespan, sub_application_sentiment_predict


async def main_lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        # Manage the lifecycle of sub_app
        await stack.enter_async_context(lifespan(sub_application_sentiment_predict))
        yield


app = FastAPI(
    title="FastSentiment",
    description="A high-performance sentiment analysis API using DistilBERT",
    version="1.0.0",
    lifespan=main_lifespan,
)


app.mount("/api", sub_application_sentiment_predict)

@app.get("/")
async def root():
    return {
        "message": "Welcome to FastSentiment",
        "docs": "/docs",
        "api": "/api/bulk-predict"
    }