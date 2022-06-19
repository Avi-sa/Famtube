from django.urls import path
from . import views

urlpatterns = [
    # path("", views.test, name="test"), #Test View
    path('set_key/', views.CreateApiKeyView.as_view(), name='create_api_key'),
    path('videos/', views.VideoDataViews.as_view(), name='video_list'),
    path('dashboard/', views.fetchData, name='videos'),
]
