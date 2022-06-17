from datetime import datetime
from django.db import models

# Create your models here.
class YoutubeVideo(models.Model):
    video_id = models.CharField(max_length=30, db_index=True, primary_key=True)
    channel_id = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    duration = models.IntegerField(default=0, null=True, blank=True)
    channel_name = models.CharField(max_length=30)
    published_at = models.DateTimeField(default=datetime.now())
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "youtube"

    def __str__(self):
        return self.video_id + " " + self.title
