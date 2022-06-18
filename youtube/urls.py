from django.urls import path
from . import views

urlpatterns = [
    path("", views.test, name="test"),
    path('set_key/', views.CreateApiKeyView.as_view(), name='create_api_key')
]
