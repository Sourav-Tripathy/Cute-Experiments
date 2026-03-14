from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# Dynamic route registered FIRST
@app.get("/tests/{test_id}")
async def get_test(test_id: str):
    return {"route": "dynamic", "test_id": test_id}

# Static route registered SECOND
@app.get("/tests/metrics")
async def get_metrics():
    return {"route": "static metrics"}

if __name__ == "__main__":
    # Check routing behavior
    # FastAPI/Starlette evaluates routes sequentially (top to bottom).
    print("Testing GET /tests/metrics")
    client = TestClient(app)
    response = client.get("/tests/metrics")
    print(f"Response: {response.json()}")
