from django.contrib import admin

from youtube.models import YoutubeVideo, APIkey

# Register your models here.
admin.site.register(YoutubeVideo)
admin.site.register(APIkey)
