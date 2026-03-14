import timeit
import sys

def setup_django(n):
    from django.conf import settings
    from django.urls import path
    import django

    if not settings.configured:
        settings.configure()
        django.setup()

    def dummy_view(request): pass

    urlpatterns = []
    for i in range(n):
        urlpatterns.append(path(f"tests/dynamic_{i}/<str:id>/", dummy_view))
    urlpatterns.append(path("tests/metrics/", dummy_view))
    
    from django.urls import clear_url_caches, set_urlconf
    
    module_name = f"django_urls_{n}"
    module = type(sys)(module_name)
    module.urlpatterns = urlpatterns
    sys.modules[module_name] = module
    
    set_urlconf(module_name)
    clear_url_caches()
    
    from django.urls import resolve
    def match():
        return resolve("/tests/metrics/")
    
    try:
        match()
    except Exception as e:
        print("Django prime failed:", e)
    return match

def setup_flask(n):
    from flask import Flask
    app = Flask(f"app_{n}")
    for i in range(n):
        app.add_url_rule(f"/tests/dynamic_{i}/<id>", f"dyn_{i}", lambda id: "")
    app.add_url_rule("/tests/metrics", "metrics", lambda: "")
    
    adapter = app.url_map.bind("")
    def match():
        return adapter.match("/tests/metrics")
    
    match()
    return match

def setup_falcon(n):
    import falcon
    app = falcon.App()
    class Dummy:
        def on_get(self, req, resp): pass
    
    for i in range(n):
        app.add_route(f"/tests/dynamic_{i}/{{id}}", Dummy())
    app.add_route("/tests/metrics", Dummy())
    
    def match():
        return app._router.find("/tests/metrics")
    
    match()
    return match

def setup_sanic(n):
    import logging
    logging.getLogger("sanic").setLevel(logging.CRITICAL)
    from sanic import Sanic
    if Sanic._app_registry:
        Sanic._app_registry.clear()
    app = Sanic(f"app_{n}")
    async def dummy(req): pass
    for i in range(n):
        app.add_route(dummy, f"/tests/dynamic_{i}/<id>")
    app.add_route(dummy, "/tests/metrics")
    
    app.router.finalize()
    
    def match():
        return app.router.get("/tests/metrics", "GET", "")
        
    match()
    return match

def setup_fastapi(n):
    from fastapi import FastAPI
    app = FastAPI()
    for i in range(n):
        @app.get(f"/tests/dynamic_{i}/{{id}}")
        async def dummy_dyn(id: str): pass
        
    @app.get("/tests/metrics")
    async def dummy_stat(): pass
    
    scope = {"type": "http", "method": "GET", "path": "/tests/metrics"}
    def match():
        for route in app.router.routes:
            m, _ = route.matches(scope)
            if m == 2: # Match.FULL
                return route
        return None
        
    match()
    return match

import json

sizes = [10, 100, 1000]
frameworks = {
    "Django": setup_django,
    "Flask": setup_flask,
    "Falcon": setup_falcon,
    "Sanic": setup_sanic,
    "FastAPI": setup_fastapi,
}

results = {}

for name, setup_fn in frameworks.items():
    print(f"--- {name} ---")
    results[name] = {}
    for n in sizes:
        match_fn = setup_fn(n)
        
        # Benchmark
        loops = 10000
        t = timeit.timeit(match_fn, number=loops)
        print(f"Routes: {n:4d} | Time per 10k routes: {t:.4f}s")
        results[name][n] = t

with open("benchmark_results.json", "w") as f:
    json.dump({"sizes": sizes, "loops": 10000, "data": results}, f, indent=4)
print("Saved routing benchmark results to benchmark_results.json")
