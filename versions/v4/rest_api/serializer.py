from rest_framework import serializers
from . import models

class WordSerializer(serializers.ModelSerializer):
    word = serializers.CharField(required=True)
    setences = serializers.CharField(required=True)
    anki = serializers.BooleanField(required=True)
    
    class Meta:
        model = models.Word
        fields = "__all__"
        