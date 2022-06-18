from dataclasses import field
from .models import APIkey, YoutubeVideo
from rest_framework import serializers

class ApiKeySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = APIkey
        fields = '__all__'

class YoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeVideo
        fields = '__all__'
