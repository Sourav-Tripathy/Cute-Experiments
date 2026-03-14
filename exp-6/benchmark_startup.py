import timeit
import sys
import uuid

def measure_django_startup(n):
    from django.conf import settings
    from django.urls import path
    import django

    if not settings.configured:
        settings.configure()
        django.setup()

    def dummy_view(request): pass

    def test():
        urlpatterns = []
        for i in range(n):
            urlpatterns.append(path(f"tests/dynamic_{i}/<str:id>/", dummy_view))
        urlpatterns.append(path("tests/metrics/", dummy_view))
        
        from django.urls import clear_url_caches, set_urlconf
        module_name = f"django_urls_{uuid.uuid4().hex}"
        module = type(sys)(module_name)
        module.urlpatterns = urlpatterns
        sys.modules[module_name] = module
        
        set_urlconf(module_name)
        clear_url_caches()
        
        # Django compiles the url patterns lazily on first resolve
        from django.urls import resolve
        resolve("/tests/metrics/")
    
    return test

def measure_flask_startup(n):
    from flask import Flask
    def test():
        app = Flask(f"app_{uuid.uuid4().hex}")
        for i in range(n):
            app.add_url_rule(f"/tests/dynamic_{i}/<id>", f"dyn_{i}", lambda id: "")
        app.add_url_rule("/tests/metrics", "metrics", lambda: "")
        
        # compile the url map and build the matching rules
        adapter = app.url_map.bind("")
        adapter.match("/tests/metrics")
    
    return test

def measure_falcon_startup(n):
    import falcon
    class Dummy:
        def on_get(self, req, resp): pass
    def test():
        app = falcon.App()
        for i in range(n):
            app.add_route(f"/tests/dynamic_{i}/{{id}}", Dummy())
        app.add_route("/tests/metrics", Dummy())
        
        # compile any regexes and tree
        app._router.find("/tests/metrics")
        
    return test

def measure_sanic_startup(n):
    import logging
    logging.getLogger("sanic").setLevel(logging.CRITICAL)
    from sanic import Sanic
    
    async def dummy(req): pass
    
    def test():
        if Sanic._app_registry:
            Sanic._app_registry.clear()
        app = Sanic(f"app_{uuid.uuid4().hex}")
        for i in range(n):
            app.add_route(dummy, f"/tests/dynamic_{i}/<id>")
        app.add_route(dummy, "/tests/metrics")
        
        # Sanic finalizes the router tree here
        app.router.finalize()
        app.router.get("/tests/metrics", "GET", "")
        
    return test

def measure_fastapi_startup(n):
    from fastapi import FastAPI
    def test():
        app = FastAPI()
        for i in range(n):
            @app.get(f"/tests/dynamic_{i}/{{id}}")
            async def dummy_dyn(id: str): pass
            
        @app.get("/tests/metrics")
        async def dummy_stat(): pass
        
        # simulate initialization first match
        scope = {"type": "http", "method": "GET", "path": "/tests/metrics"}
        for route in app.router.routes:
            m, _ = route.matches(scope)
            if m == 2:
                break
                
    return test

import json

sizes = [10, 100, 1000]
frameworks = {
    "Django": measure_django_startup,
    "Flask": measure_flask_startup,
    "Falcon": measure_falcon_startup,
    "Sanic": measure_sanic_startup,
    "FastAPI": measure_fastapi_startup,
}

results = {}

for name, setup_fn in frameworks.items():
    print(f"--- {name} Startup ---")
    results[name] = {}
    for n in sizes:
        startup_fn = setup_fn(n)
        
        # Benchmark
        # Executing route registration and tree generation 100 times
        loops = 100
        t = timeit.timeit(startup_fn, number=loops)
        print(f"Routes: {n:4d} | Startup time for 100 inits: {t:.4f}s")
        results[name][n] = t

with open("benchmark_startup_results.json", "w") as f:
    json.dump({"sizes": sizes, "loops": 100, "data": results}, f, indent=4)
print("Saved startup benchmark results to benchmark_startup_results.json")
