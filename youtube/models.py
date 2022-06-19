from datetime import datetime
from django.db import models
from django.utils.timezone import now

# Create your models here.
class YoutubeVideo(models.Model):
    '''
        Table to store video data.
    '''
    video_id = models.CharField(max_length=30, db_index=True, primary_key=True)
    channel_id = models.CharField(max_length=30)
    title = models.CharField(max_length=70)
    description = models.TextField()
    thumbnail_urls = models.JSONField()
    duration = models.IntegerField(default=0, null=True, blank=True)
    channel_title = models.CharField(max_length=30)
    published_at = models.DateTimeField(default=now)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "youtube"

    def __str__(self):
        return self.video_id + " " + self.title

class APIkey(models.Model):
    api_key = models.CharField(max_length=100)
    is_expired = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    expired_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "youtube"

    def __str__(self):
        return self.api_key + " " + str(self.is_expired)