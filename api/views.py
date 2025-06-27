"""
api/views.py
Author: bella918@bu.edu
Project: api/views.py
Date: 2025-06-26

defines all views and API endpoints for the image processing application.
It includes user registration, image upload, full image processing, cropped region processing, 
tag management, image deletion, image search, history display (function and class-based), 
and detailed image view.

"""


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import ListView

from datetime import datetime
import os
import json

from django.conf import settings

from .serializers import UploadedImageSerializer, UploadedImageTagSerializer, TagSerializer
from .models import UploadedImage, ProcessingLog, CropRegion, Tag, UploadedImageTag
from .u2net_utils import process_cropped_region
from .utils import build_image_url

# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import UploadedImageSerializer
# from .models import UploadedImage
# from .u2net_utils import process_cropped_region
# from datetime import datetime
# import os
# from django.conf import settings
# from .models import UploadedImage, ProcessingLog, CropRegion, Tag, UploadedImageTag
# from .utils import build_image_url


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    """
    Render the home page.
    """
    return render(request, 'index.html')

@api_view(['POST'])
def upload_image(request):
    """
    Handle image upload via API and save it to the database.
    """
    serializer = UploadedImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user if request.user.is_authenticated else None)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def process_full_image(request):
    """
    Process the full uploaded image using U2NET and save the processed version.
    """
    image_id = request.data.get('image_id')

    try:
        image = UploadedImage.objects.get(id=image_id)
    except UploadedImage.DoesNotExist:
        return Response({'error': 'Image not found.'}, status=404)

    input_path = image.image.path
    output_filename = f"processed_full_{image_id}.png"
    output_path = os.path.join(settings.MEDIA_ROOT, 'processed', output_filename)

    start_time = datetime.now()
    process_cropped_region(input_path, None, output_path)
    duration = (datetime.now() - start_time).total_seconds()

    image.processed_image.name = f"processed/{output_filename}"
    image.save()

    ProcessingLog.objects.create(
        image=image,
        method='full',
        duration=duration,
        notes="Full image processed"
    )

    image_url = build_image_url(request, image.processed_image.url)
    return Response({'status': 'done', 'processed_url': image_url})




@api_view(['POST'])
def process_crop_region(request):
    """
    Process a cropped region of an uploaded image using U2NET and save the result.
    """
    image_id = request.data.get('image_id')
    x = float(request.data.get('x'))
    y = float(request.data.get('y'))
    width = float(request.data.get('width'))
    height = float(request.data.get('height'))

    try:
        image = UploadedImage.objects.get(id=image_id)
    except UploadedImage.DoesNotExist:
        return Response({'error': 'Image not found.'}, status=404)

    input_path = image.image.path

    timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S%f')
    output_filename = f"processed_crop_{image_id}_{timestamp_str}.png"
    output_path = os.path.join(settings.MEDIA_ROOT, 'processed', output_filename)

    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'processed')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'processed'))

    try:
        start_time = datetime.now()
        process_cropped_region(input_path, {'x': x, 'y': y, 'width': width, 'height': height}, output_path)
        duration = (datetime.now() - start_time).total_seconds()

        image.processed_image.name = f"processed/{output_filename}"
        image.save()

        CropRegion.objects.create(image=image, x=x, y=y, width=width, height=height)

        ProcessingLog.objects.create(image=image, method='crop', duration=duration, notes=f'Cropped at x={x}, y={y}, w={width}, h={height}')

        image_url = build_image_url(request, image.processed_image.url)
        return Response({'status': 'done', 'processed_url': image_url})

    except Exception as e:
        print('Error processing crop:', e)
        return Response({'error': 'Internal server error during cropping.'}, status=500)


@api_view(['POST'])
def add_tag_to_image(request):
    """
    Add a tag to the specified image.
    """
    image_id = request.data.get('image_id')
    tag_name = request.data.get('tag')

    try:
        image = UploadedImage.objects.get(id=image_id)
    except UploadedImage.DoesNotExist:
        return Response({'error': 'Image not found.'}, status=404)

    tag, created = Tag.objects.get_or_create(name=tag_name)
    UploadedImageTag.objects.get_or_create(image=image, tag=tag)

    return Response({'status': 'tag added', 'tag': tag.name})


@api_view(['GET'])
def view_processing_logs(request, image_id=None):
    if image_id:
        logs = ProcessingLog.objects.filter(image__id=image_id).order_by('-timestamp')
    else:
        logs = ProcessingLog.objects.all().order_by('-timestamp')

    data = []
    for log in logs:
        data.append({
            'image_id': log.image.id,
            'method': log.method,
            'timestamp': log.timestamp,
            'duration': log.duration,
            'notes': log.notes,
            'processed_url': build_image_url(request, log.image.processed_image.url) if log.image.processed_image else None
        })
    return Response(data)

from .serializers import UploadedImageSerializer, UploadedImageTagSerializer, TagSerializer

@api_view(['GET'])
def list_uploaded_images(request):
    images = UploadedImage.objects.all().order_by('-uploaded_at')
    result = []

    for image in images:
        tags = UploadedImageTag.objects.filter(image=image).select_related('tag')
        tag_list = [t.tag.name for t in tags]

        result.append({
            'id': image.id,
            'image': build_image_url(request, image.image.url),
            'processed_image': build_image_url(request, image.processed_image.url) if image.processed_image else None,
            'uploaded_at': image.uploaded_at,
            'tags': tag_list
        })
    return Response(result)


@api_view(['GET'])
def list_images_by_tag(request):
    tag_name = request.GET.get('tag')
    if not tag_name:
        return Response({'error': 'Tag name is required.'}, status=400)

    tag = Tag.objects.filter(name=tag_name).first()
    if not tag:
        return Response({'error': 'Tag not found.'}, status=404)

    image_tags = UploadedImageTag.objects.filter(tag=tag)
    result = []

    for it in image_tags:
        image = it.image
        tags = UploadedImageTag.objects.filter(image=image).select_related('tag')
        tag_list = [t.tag.name for t in tags]

        result.append({
            'id': image.id,
            'image': build_image_url(request, image.image.url),
            'processed_image': build_image_url(request, image.processed_image.url) if image.processed_image else None,
            'uploaded_at': image.uploaded_at,
            'tags': tag_list
        })
    return Response(result)

def home_view(request):
    return render(request, 'index.html')



def history_view(request):
    """
    Render the image history page. Supports filtering by tag and pagination.
    """
    tag = request.GET.get('tag')
    page_number = request.GET.get('page', 1)

    if tag:
        image_tags = UploadedImageTag.objects.filter(tag__name=tag)
        images = UploadedImage.objects.filter(id__in=[it.image.id for it in image_tags]).order_by('-uploaded_at')
    else:
        images = UploadedImage.objects.all().order_by('-uploaded_at')

    paginator = Paginator(images, 5)  # 每页 5 张
    page_obj = paginator.get_page(page_number)

    image_list = []
    for image in page_obj:
        tags = UploadedImageTag.objects.filter(image=image).select_related('tag')
        tag_list = [t.tag.name for t in tags]

        image_list.append({
            'id': image.id,
            'image': build_image_url(request, image.image.url),
            'processed_image': build_image_url(request, image.processed_image.url) if image.processed_image else None,
            'tags': tag_list,
        })

    return render(request, 'history.html', {
        'images': image_list,
        'page_obj': page_obj,
        'current_tag': tag,
    })



@api_view(['GET'])
def search_by_tag(request):
    """
    Search images by tag using partial match.
    """
    tag_query = request.GET.get('tag')
    if not tag_query:
        return Response({'error': 'Tag is required.'}, status=400)

    image_tags = UploadedImageTag.objects.filter(tag__name__icontains=tag_query)
    results = []
    for image_tag in image_tags:
        image = image_tag.image
        results.append({
            'id': image.id,
            'image_url': image.image.url,
            'processed_url': image.processed_image.url if image.processed_image else ''
        })
    return Response({'results': results})




def search_view(request):
    """
    Render the search results page based on tag query. Supports pagination.
    """
    tag_query = request.GET.get('tag')
    results = []

    if tag_query:
        images = UploadedImageTag.objects.filter(tag__name__icontains=tag_query)
        for img_tag in images:
            image = img_tag.image
            tags = UploadedImageTag.objects.filter(image=image).select_related('tag')
            tag_list = [t.tag.name for t in tags]

            results.append({
                'id': image.id,
                'image_url': image.image.url,
                'processed_url': image.processed_image.url if image.processed_image else '',
                'tags': tag_list,
                'username': image.user.username if image.user else None,
            })

    paginator = Paginator(results, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {'tag': tag_query, 'page_obj': page_obj})


def register_view(request):
    """
    Render the user registration page and handle registration form submission.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



@api_view(['POST'])
def delete_image(request):
    """
    Delete an uploaded image by ID.
    """
    image_id = request.data.get('image_id')
    try:
        image = UploadedImage.objects.get(id=image_id)
        image.delete()
        return Response({'status': 'deleted'}, status=status.HTTP_200_OK)
    except UploadedImage.DoesNotExist:
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    



def image_detail_view(request, image_id):
    """
    Render the detail page for a specific image, showing tags and processing logs.
    """
    image = UploadedImage.objects.get(id=image_id)
    tags = UploadedImageTag.objects.filter(image=image).select_related('tag')
    tag_list = [t.tag.name for t in tags]

    logs = ProcessingLog.objects.filter(image=image).order_by('-timestamp')

    method = logs[0].method if logs.exists() else 'Unknown'

    crop_region = None
    if method == 'crop':
        crop = CropRegion.objects.filter(image=image).order_by('-created_at').first()
        if crop:
            crop_region = {'x': crop.x, 'y': crop.y, 'width': crop.width, 'height': crop.height}

    context = {
        'image': {
            'id': image.id,
            'image': build_image_url(request, image.image.url),
            'processed_image': build_image_url(request, image.processed_image.url) if image.processed_image else None,
            'tags': tag_list,
            'method': method,
            'crop_params': crop_region
        }
    }
    return render(request, 'image_detail.html', context)



@csrf_exempt
def update_tag_view(request, image_id):
    """
    Update the tag of a specified image. Accepts JSON request body.
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            new_tag_name = body.get('tag').strip()

            if not new_tag_name:
                return JsonResponse({'status': 'error', 'message': 'Tag cannot be empty.'})

            image = UploadedImage.objects.get(id=image_id)

            # 清除旧标签
            UploadedImageTag.objects.filter(image=image).delete()

            # 创建新标签
            new_tag, created = Tag.objects.get_or_create(name=new_tag_name)
            UploadedImageTag.objects.create(image=image, tag=new_tag)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print('Update tag error:', e)
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})




class HistoryListView(ListView):
    """
    Class-based view for displaying image history with optional tag filtering and pagination.
    """
    model = UploadedImage
    template_name = 'history.html'
    context_object_name = 'images'  # 页面用 {% for image in images %}
    paginate_by = 5

    def get_queryset(self):
        """
        Get filtered or all images for the current page.
        """
        tag = self.request.GET.get('tag')
        if tag:
            image_tags = UploadedImageTag.objects.filter(tag__name=tag)
            return UploadedImage.objects.filter(id__in=[it.image.id for it in image_tags]).order_by('-uploaded_at')
        return UploadedImage.objects.all().order_by('-uploaded_at')

    def get_context_data(self, **kwargs):
        """
        Add image detail, tags, and usernames to context.
        """
        context = super().get_context_data(**kwargs)
        tag = self.request.GET.get('tag')
        context['current_tag'] = tag

        image_list = []
        for image in context['page_obj']:
            tags = UploadedImageTag.objects.filter(image=image).select_related('tag')
            tag_list = [t.tag.name for t in tags]

            image_list.append({
                'id': image.id,
                'image_url': build_image_url(self.request, image.image.url),
                'processed_image_url': build_image_url(self.request, image.processed_image.url) if image.processed_image else None,
                'tags': tag_list,
                'username': image.user.username if image.user else None,  # ✅ 关键字段
            })

        context['images'] = image_list
        return context

