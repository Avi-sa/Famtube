from sre_constants import SUCCESS
from celery import shared_task
from googleapiclient.discovery import build
from isodate import parse_duration
from youtube.models import YoutubeVideo

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
PREDEFINED_QUERY = "Cricket"

API_KEY = "AIzaSyBkIua0rxsm_3eCD-CM5JKKDsq8el86rPg"

class GetYoutubeVides:
    def google_api_videos(self, search=PREDEFINED_QUERY, api_key=API_KEY):
        try:
            famtube = build(YOUTUBE_API_SERVICE_NAME, 
                    YOUTUBE_API_VERSION, developerKey=api_key)
            search_result = famtube.search().list(
                                q = search, 
                                part = 'snippet', maxResults=5, type='video',
                                order='date', publishedAfter='2021-01-01T00:00:00Z'
                            ).execute()
            videos_ids = []
            items_list = search_result.get('items', [])
        except Exception:
            return False
        if items_list:
            for item in items_list:
                videos_ids.append(item['id']['videoId'])
            videos_list = famtube.videos().list(id=videos_ids, part='snippet,contentDetails').execute()
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

@shared_task(bind=True)
def fetch_yt_videos(self):
    from youtube.models import APIkey
    keys = APIkey.objects.filter(is_expired=False).order_by('added_on').first()
    if keys:
        GetYoutubeVides().google_api_videos(api_key=keys.api_key)
    else:
        print('Please register a valid API Key in DB')
        pass

@shared_task(bind=True)
def celery_test(self):
    for i in range(5):
        print(f"*********************************** {i}th print *********************")
    return "working"
