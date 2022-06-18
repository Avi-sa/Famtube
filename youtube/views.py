from lib2to3.pytree import Base
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from youtube.models import YoutubeVideo

from youtube.scheduled_task import fetch_yt_videos
from .serializer import ApiKeySerializer, YoutubeSerializer
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

class VideoDataViews(APIView, LimitOffsetPagination):
    queryset = YoutubeVideo.objects.all().order_by('-published_at')

    def get(self, request):
        try:
            search_param = self.request.query_params.get('search')
            if search_param:
                results = []
                result_dict = self.queryset.values()
                print(result_dict)
                for result in result_dict:
                    if search_param in result['title'] or search_param in result['description']:
                        results.append(result)
                self.queryset = results
            results = self.paginate_queryset(self.queryset, request, view=self)
            serializer = YoutubeSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)
        except:
            return []
