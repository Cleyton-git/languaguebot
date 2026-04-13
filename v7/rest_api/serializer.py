from rest_framework import serializers
from . import models

class IdSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)
    
    class Meta:
        model = models.Id
        fields = "__all__"
        