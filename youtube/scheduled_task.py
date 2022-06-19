from datetime import datetime
from sre_constants import SUCCESS
from celery import shared_task
from googleapiclient.discovery import build
from isodate import parse_duration
from youtube.models import APIkey, YoutubeVideo
from decouple import config


# API_KEY = config('API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
PREDEFINED_QUERY = "Cricket"

# Class to store videos in DB.
class GetYoutubeVides:
    def __init__(self, api_key):
        self.famtube = build(YOUTUBE_API_SERVICE_NAME, 
                    YOUTUBE_API_VERSION, developerKey=api_key)

    def youtube_search(self, search, nextToken):
        search_result = self.famtube.search().list(
                    q = search, 
                    part = 'snippet', maxResults=5, type='video',
                    order='date', publishedAfter='2021-01-01T00:00:00Z',
                    pageToken = nextToken
                ).execute()
        return search_result

    # Function to save videos based on search Parameter.
    def google_api_videos(self, search=PREDEFINED_QUERY):
        items_list = []
        try:
            nextToken = None
            for i in range(3):
                search_result = self.youtube_search(search, nextToken)
                nextToken = search_result.get('nextPageToken')
                items_list.extend(search_result.get('items', []))
        except Exception as E:
            print('Inside exception', E)
            return False
        videos_ids = list()
        if items_list:
            for item in items_list:
                videos_ids.append(item['id']['videoId'])
            videos_list = self.famtube.videos().list(id=videos_ids, part='snippet,contentDetails').execute()
            items_list = videos_list.get('items', [])
            for item in items_list:
                video_id = item['id']
                published_at = item['snippet']['publishedAt']
                channel_id = item['snippet']['channelId']
                title = item['snippet']['title']
                description = item['snippet']['description']
                channel_title = item['snippet']['channelTitle']
                thumbnails = item['snippet']['thumbnails']
                duration = int(parse_duration(item['contentDetails']['duration']).total_seconds() / 60)
                youtube = YoutubeVideo(
                    video_id = video_id,
                    channel_id = channel_id,
                    title = title,
                    description = description,
                    channel_title = channel_title,
                    thumbnail_urls = thumbnails,
                    published_at = published_at,
                    duration = duration
                )
                youtube.save()
                print('Video saved in model')
            return True
        return False


# Shared task that runs in each 60 seconds and stores data in DB.
@shared_task(bind=True)
def fetch_yt_videos(self):
    from youtube.models import APIkey
    from django.utils import timezone
    keys = APIkey.objects.filter(is_expired=False).order_by('added_on')
    if keys:
        for i in range(keys.count()):
            featched_videos = GetYoutubeVides(api_key=keys[i].api_key).google_api_videos()
            if not featched_videos:
                api_obj = APIkey.objects.get(api_key=keys[i].api_key)
                api_obj.expired_on = datetime.now(tz=timezone.utc)
                api_obj.is_expired = True
                api_obj.save()
            else:
                break
    else:
        print('*************************Please register a valid API Key in DB*********************')
        pass

@shared_task(bind=True)
def celery_test(self):
    for i in range(5):
        print(f"*********************************** {i}th print *********************")
    return "working"
