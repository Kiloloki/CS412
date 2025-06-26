from rest_framework import serializers
from .models import UploadedImage, CropRegion, ProcessingLog, Tag, UploadedImageTag

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'

class CropRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropRegion
        fields = '__all__'

class ProcessingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingLog
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class UploadedImageTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImageTag
        fields = '__all__'
