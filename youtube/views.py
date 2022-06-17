from django.http.response import HttpResponse
from django.shortcuts import render

from .scheduled_task import celery_test

# Create your views here.
def test(request):
    celery_test.delay()
    return HttpResponse("Done")
