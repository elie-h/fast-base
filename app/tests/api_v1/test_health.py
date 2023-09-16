from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routes.v1.endpoints.health import router

app = FastAPI()

app.include_router(router)


def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == "ok"
