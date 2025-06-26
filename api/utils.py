from django.conf import settings

def build_image_url(request, image_field_url):
    if settings.DEBUG:
        return f"http://{request.get_host()}{image_field_url}"
    else:
        return image_field_url
