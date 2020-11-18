from rest_framework import serializers
from .google_cloud_bucket_models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"