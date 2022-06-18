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
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def test(request):
    fetch_yt_videos.delay()
    return HttpResponse("Done")

# A POST API to store new API Key in DB. It will be used automatically once the old api key expires.
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
                search_param = search_param.lower().split(' ')
                word_list = list()
                for result in result_dict:
                    word_list.extend(result['title'].lower().split(' '))
                    word_list.extend(result['description'].lower().split(' '))
                    if (set(search_param) & set(word_list)):
                        results.append(result)
                    word_list.clear()
                self.queryset = results
            results = self.paginate_queryset(self.queryset, request, view=self)
            serializer = YoutubeSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)
        except:
            return []

def fetchData(request):
    videoData = YoutubeVideo.objects.all()
    search = request.GET.get('order_by', None)
    search_param = request.GET.get('search_box', None)
    duration = request.GET.get('duration', None)
    if search:
        videoData = videoData.order_by(search)
    if duration:
        duration = int(duration.strip())
        if duration:
            videoData = videoData.filter(duration__lte=int(duration))
    if search_param:
        search_param = search_param.lower().split(' ')
        word_list = list()
        exclude_list = []
        for result in videoData:
            word_list.extend(result.__dict__['title'].lower().split(' '))
            word_list.extend(result.__dict__['description'].lower().split(' '))
            if not (set(search_param) & set(word_list)):
                exclude_list.append(result.video_id)
            word_list.clear()
        videoData = videoData.exclude(video_id__in = exclude_list)
    paginator = Paginator(videoData, 9)
    page = request.GET.get('page', 1)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request, 'video_dashboard.html', { 'videos': videos })