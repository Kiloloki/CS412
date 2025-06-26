from django.contrib import admin

# Register your models here.
from .models import UploadedImage, CropRegion, ProcessingLog, Tag, UploadedImageTag

admin.site.register(UploadedImage)
admin.site.register(CropRegion)
admin.site.register(ProcessingLog)
admin.site.register(Tag)
admin.site.register(UploadedImageTag)
