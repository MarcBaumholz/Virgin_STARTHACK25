import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from fastapi_app import app
import json

client = TestClient(app)

@pytest.mark.asyncio
async def test_dashboard_loads():
    response = client.get("/")
    assert response.status_code == 200
    print("\nTesting Dashboard Load:")
    print(f"Status Code: {response.status_code}")
    
@pytest.mark.asyncio
async def test_analysis_endpoint():
    types = ["summarize", "labels", "trends"]
    print("\nTesting Analysis Endpoints:")
    for analysis_type in types:
        response = client.get(f"/api/analysis?type={analysis_type}")
        assert response.status_code == 200
        result = response.json()
        print(f"\n{analysis_type.title()} Analysis Result:")
        print(f"{str(result)[:200]}...")

@pytest.mark.asyncio
async def test_query_interaction():
    test_queries = [
        "How many digital projects are there?",
        "What are the main sustainability initiatives?"
    ]
    print("\nTesting Query Interactions:")
    for query in test_queries:
        response = client.post("/query", data={"query": query})
        assert response.status_code == 200
        result = response.json()
        print(f"\nQuery: {query}")
        print(f"Response: {str(result)[:200]}...")
