from lib2to3.pytree import Base
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from youtube.scheduled_task import fetch_yt_videos
from .serializer import ApiKeySerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def test(request):
    fetch_yt_videos.delay()
    return HttpResponse("Done")


class CreateApiKeyView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        new_api_key = request.data.get('api_key', None)
        if new_api_key:
            if len(new_api_key)<15:
                return Response(
                    {'message': 'Pass a valid Api Key'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ApiKeySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'message': 'Something went Wrong'}, status=status.HTTP_400_BAD_REQUEST)

# class SearchVideo(APIView):
#     http_method_names = ['get']

#     def get(self, request):
        
