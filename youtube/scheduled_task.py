from sre_constants import SUCCESS
from celery import shared_task
from googleapiclient.discovery import build
from isodate import parse_duration
from youtube.models import YoutubeVideo

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
PREDEFINED_QUERY = "Cricket"

API_KEY = "AIzaSyBkIua0rxsm_3eCD-CM5JKKDsq8el86rPg"


def google_api():
    famtube = build(YOUTUBE_API_SERVICE_NAME, 
                    YOUTUBE_API_VERSION, developerKey=API_KEY)
    search_result = famtube.search().list(
                        q = PREDEFINED_QUERY, 
                        part = 'snippet', maxResults=5, type='video',
                        order='date', publishedAfter='2021-01-01T00:00:00Z'
                    ).execute()
    videos_ids = []
    items_list = search_result.get('items', [])
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
        # youtube = YoutubeVideo(
        #     video_id = video_id,
        #     channel_id = channel_id,
        #     title = title,
        #     description = description,
        #     channel_name = channel_title,
        #     thumbnail_urls = thumbnails,
        #     published_at = published_at,
        #     duration = duration
        # )
        print('SUCCESS', ' ', video_id, channel_id, published_at, title, description, channel_title, duration)
        print('\n\n')
        # youtube.save()

@shared_task(bind=True)
def celery_test(self):
    for i in range(5):
        print(f"*********************************** {i}th print *********************")
    return "working"
