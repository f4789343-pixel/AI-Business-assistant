import pytest
from backend.api import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_chat():
  response = client.post("/chat",json={"data": "How can you help me?"})
  assert response.status_code == 200
  assert response.json() is not None

def test_tool_calling():
  response = client.post("/chat", json={"data": "Total count of orders?"})
  response2 = client.post("/chat", json={"data": "find customer with name of priya"})
  assert response.status_code == 200
  assert response2.status_code == 200
  assert response.json() is not None
  assert response2.json() is not None


 
  