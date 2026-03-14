import falcon
from falcon import testing

class DynamicResource:
    def on_get(self, req, resp, test_id):
        resp.text = f"dynamic: {test_id}"

class StaticResource:
    def on_get(self, req, resp):
        resp.text = "static: metrics"

app = falcon.App()

# Dynamic route registered FIRST
app.add_route("/tests/{test_id}", DynamicResource())

# Static route registered SECOND
app.add_route("/tests/metrics", StaticResource())

if __name__ == "__main__":
    # Check routing behavior
    client = testing.TestClient(app)
    result = client.simulate_get("/tests/metrics")
    
    print("Testing GET /tests/metrics")
    print(f"Response: {result.text}")
