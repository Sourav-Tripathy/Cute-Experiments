import django
from django.conf import settings
settings.configure(ROOT_URLCONF=__name__)
django.setup()
from django.urls import path
from django.http import HttpResponse
from django.test import RequestFactory

def get_test(request, test_id):
    return HttpResponse(f"dynamic: {test_id}")

def get_metrics(request):

    return HttpResponse("static: metrics")

# Dynamic route registered FIRST, static route second

urlpatterns = [

    path("tests/<str:test_id>/", get_test),

    path("tests/metrics/", get_metrics),

]
factory = RequestFactory()
request = factory.get("/tests/metrics/")
from django.urls import resolve
match = resolve("/tests/metrics/")

print(match.func.__name__)  # prints get_test, swallowing get_metrics