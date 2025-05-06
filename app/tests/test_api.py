import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from src.main import app


@pytest.fixture
def client():
    """
    Test client fixture with memory caching for testing
    """
    FastAPICache.init(InMemoryBackend())
    with TestClient(app) as c:
        yield c


def test_root(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Welcome to the Sentiment Analysis API" in response.json()["message"]


def test_health(client):
    """Test the health endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_positive_negative(client):
    """Test sentiment prediction with positive and negative examples"""
    data = {"text": ["I hate you.", "I love you."]}
    response = client.post(
        "/api/bulk-predict",
        json=data,
    )
    assert response.status_code == 200
    
    # Check response structure
    result = response.json()
    assert "predictions" in result
    assert isinstance(result["predictions"], list)
    assert len(result["predictions"]) == 2  # Two input texts
    
    # Check first prediction (negative sentiment)
    assert isinstance(result["predictions"][0], list)
    assert isinstance(result["predictions"][0][0], dict)
    assert set(result["predictions"][0][0].keys()) == {"label", "score"}
    assert "NEGATIVE" in [pred["label"] for pred in result["predictions"][0]]
    assert "POSITIVE" in [pred["label"] for pred in result["predictions"][0]]
    
    # Check second prediction (positive sentiment)
    assert isinstance(result["predictions"][1], list)
    assert isinstance(result["predictions"][1][0], dict)
    assert set(result["predictions"][1][0].keys()) == {"label", "score"}
    assert "NEGATIVE" in [pred["label"] for pred in result["predictions"][1]]
    assert "POSITIVE" in [pred["label"] for pred in result["predictions"][1]]
    
    # Verify the prediction is as expected (first text should be negative, second positive)
    neg_scores = [pred for pred in result["predictions"][0] if pred["label"] == "NEGATIVE"]
    pos_scores = [pred for pred in result["predictions"][1] if pred["label"] == "POSITIVE"]
    
    assert len(neg_scores) == 1
    assert len(pos_scores) == 1
    assert neg_scores[0]["score"] > 0.5  # Confidence in negative for first text
    assert pos_scores[0]["score"] > 0.5  # Confidence in positive for second text


def test_predict_multiple_texts(client):
    """Test sentiment prediction with multiple texts"""
    data = {"text": ["Amazing product!", "Terrible experience", "Neutral statement"]}
    response = client.post(
        "/api/bulk-predict",
        json=data,
    )
    assert response.status_code == 200
    
    # Check correct number of predictions
    result = response.json()
    assert len(result["predictions"]) == 3
    
    # All predictions should have both POSITIVE and NEGATIVE labels
    for prediction in result["predictions"]:
        labels = [pred["label"] for pred in prediction]
        assert "POSITIVE" in labels
        assert "NEGATIVE" in labels
        
        # Scores should sum to approximately 1
        scores = [pred["score"] for pred in prediction]
        assert sum(scores) > 0.99  # Allow for small floating point discrepancies


def test_invalid_request(client):
    """Test invalid request handling"""
    # Empty text list
    data = {"text": []}
    response = client.post(
        "/api/bulk-predict",
        json=data,
    )
    assert response.status_code == 200  # ValidationError handled by FastAPI
    
    # Invalid request structure
    data = {"invalid_field": "test"}
    response = client.post(
        "/api/bulk-predict",
        json=data,
    )
    assert response.status_code == 422  # Validation error