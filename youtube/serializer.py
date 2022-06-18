from dataclasses import field
from .models import APIkey
from rest_framework import serializers

class ApiKeySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = APIkey
        fields = '__all__'
