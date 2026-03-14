import asyncio
from sanic import Sanic
from sanic.response import text

app = Sanic("RouterExp")

# Dynamic route registered FIRST
@app.get("/tests/<test_id>")
async def get_test(request, test_id):
    return text(f"dynamic: {test_id}")

# Static route registered SECOND
@app.get("/tests/metrics")
async def get_metrics(request):
    return text("static: metrics")

if __name__ == "__main__":
    # Check routing behavior
    # Sanic resolves routes using a radix tree.
    # We can just simulate a request using its TestClient.
    request, response = app.test_client.get("/tests/metrics")
    
    print("Testing GET /tests/metrics")
    print(f"Response: {response.text}")
