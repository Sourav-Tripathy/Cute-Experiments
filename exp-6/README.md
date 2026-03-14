# Python Web Frameworks: Routing Complexity Experiment

Out of curiosity, I conducted a few experiments to observe the fundamental differences in how various Python web frameworks process HTTP routes under the hood. Specifically, I looked into Sequential Evaluation versus Radix/Tree-Based Compilation.

## 1. The Shadowing Experiment (`main_*.py`)

The initial experiment was to see whether a broad dynamic route could "swallow" or "shadow" a perfectly matching static route if the dynamic route was registered first.

I created an identical setup across 5 major frameworks:
1. Register a dynamic route first, e.g., `/tests/<test_id>`
2. Register a static route second, e.g., `/tests/metrics`
3. Request `/tests/metrics` and observe which handler catches it.

### Observations:
*   **Django & FastAPI**: Routed to the **dynamic** handler (`/tests/<test_id>`). I observed that they evaluate routes sequentially, top-to-bottom. The first regex match wins. Order matters.
*   **Flask, Falcon, & Sanic**: Routed to the **static** handler (`/tests/metrics`). They appear to "smart-sort" or compile routes into states/trees, properly identifying that a static string match is more specific than a parameterized variable match, regardless of registration order.

You can observe this by running any of the `main_*.py` files:
```bash
python3 main_django.py    # Outputs dynamic
python3 main_fastapi.py   # Outputs dynamic

python3 main_flask.py     # Outputs static
python3 main_falcon.py    # Outputs static
python3 main_sanic.py     # Outputs static
```

---

## 2. The Benchmarks

After looking at the functional differences, I set up some benchmarks (bypassing the HTTP network/socket layer entirely) to measure raw algorithmic behavior of the underlying URL resolvers. 

I generated `N` dynamic paths (10, 100, 1000) *before* appending a single static target path to the routing configuration.

### A. Routing Time (`benchmark.py`)
This measures the time it takes the routing engine to successfully match an incoming string to the target route handler 10,000 times.

*   **Django / FastAPI**: Matching time appeared to scale linearly. To find the route at the bottom of the list, they evaluate previous dynamic routes sequentially.
*   **Flask / Sanic**: Showed a perfectly flat horizontal matching time relative to the number of routes. The radix tree/hash map matches requested URLs in roughly constant time.
*   **Falcon**: Appeared to be very fast, curving up only slightly logarithmically.

### B. Startup / Compilation Time (`benchmark_startup.py`)
This measures how long it takes the framework to instantiate the App and configure the routes for 100 startups. This allowed me to observe the tradeoff for faster routing times.

*   **Django**: Showed near instantaneous startup. It simply appends patterns to a Python list. 
*   **Sanic / Flask / Falcon**: Showed slower startup times. They incur a cost upfront to parse, validate, and convert paths into their optimized structures.

*Note: FastAPI also exhibited a slow startup time, but mostly due to parsing Pydantic annotations and generating OpenAPI schemas.*

---

## Limitations

It is important to note a few limitations in how these experiments and benchmarks were conducted:
1. **HTTP/TCP Overhead Ignored**: These tests isolated the routing logic exclusively. In a real-world scenario, the majority of a server's request time is typically spent parsing HTTP headers, managing connections, and sending bytes over the network. Microsecond differences in routing trees are often completely overshadowed by these broader network costs.
2. **No Garbage Collection Accounting**: I did not explicitly force Python's garbage collector (`gc.collect()`) to run between loop iterations during the startup benchmarks. As a result, memory fragmentation from generating tens of thousands of routes in a tight loop might have triggered GC pauses, marginally impacting some recorded times.
3. **Regex Strictness**: Each framework translates path parameters (like `<str:id>` vs `{id}`) into Regular Expressions differently. Some variations are stricter than others, which could inherently cause minute differences in string matching times that aren't purely due to the routing data structure.

---

## How to Replicate

**1. Create a virtual environment and load dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install django flask falcon sanic sanic-testing fastapi uvicorn httpx matplotlib
```

**2. Test the Routing Match Behavior:**
```bash
python3 main_django.py
python3 main_flask.py
# (etc.)
```

**3. Run the Benchmarks:**
```bash
python3 benchmark.py
python3 benchmark_startup.py
```
*(This will compute iterations and generate `benchmark_results.json` and `benchmark_startup_results.json`)*

**4. Visualize the Results:**
Run the graphing script to convert the JSON outputs into cleanly plotted PNG graphs.
```bash
python3 visualize.py
```
This will produce `routing_complexity_graph.png` and `startup_complexity_graph.png` in the directory so you can visually examine the algorithmic tradeoffs.

---
*(Environment tracked during testing: CPython 3.10.12 | Django 5.2.12 | Flask 3.1.3 | Falcon 4.2.0 | Sanic 25.12.0 | FastAPI 0.115.6 on  dual-boot Ubuntu 22.04, 8GB RAM, 512GB SSD).*
