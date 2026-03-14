from flask import Flask

app = Flask(__name__)

# Dynamic route registered FIRST
@app.get("/tests/<test_id>")
def get_test(test_id):
    return f"dynamic: {test_id}"

# Static route registered SECOND
@app.get("/tests/metrics")
def get_metrics():
    return "static: metrics"

# Print the sorted url_map to see the actual matching order
with app.app_context():
    for rule in app.url_map.iter_rules():
        print(rule.rule, rule.arguments)

# Using a test client to explicitly show precedence
with app.test_client() as client:
    resp = client.get("/tests/metrics")
    print(f"\nResponse from /tests/metrics: {resp.data.decode('utf-8')}")