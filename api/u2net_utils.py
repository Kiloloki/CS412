"""
api/u2net_utils.py

This module handles image background removal using the U2NET model.
It supports processing full images and cropped regions, and logs the processing details.

Author: bella918@bu.edu
Project: api/u2net_utils.py
Date: 2025-06-26
"""


import torch
from torchvision import transforms
from PIL import Image
import numpy as np
import os
from .models import UploadedImage
from model.u2net import U2NET  
from django.conf import settings
from .models import UploadedImage, CropRegion, ProcessingLog

# Set the device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_u2net(model_path='saved_models/u2net/u2net.pth'):
    """
    Load the pre-trained U2NET model.
    """
    net = U2NET(3, 1)
    net.load_state_dict(torch.load(model_path, map_location=device))
    net.to(device)
    net.eval()
    return net


# Load the model once when the module is imported
u2net_model = load_u2net()


def process_cropped_region(input_path, crop_region, output_path):
    """
    Process an image or cropped region using U2NET to remove the background.
    Save the processed image with transparency to the specified output path.

    Args:
        input_path (str): Path to the input image.
        crop_region (dict or None): Crop parameters {x, y, width, height}, or None for full image.
        output_path (str): Path to save the processed image.
    """
    image = Image.open(input_path).convert("RGB")

    if crop_region:
        x = int(crop_region['x'])
        y = int(crop_region['y'])
        width = int(crop_region['width'])
        height = int(crop_region['height'])
        image = image.crop((x, y, x + width, y + height))

    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])

    input_tensor = transform(image).unsqueeze(0)
    input_tensor = input_tensor.to(device)

    with torch.no_grad():
        d1, *_ = u2net_model(input_tensor)
        pred = d1[:, 0, :, :]
        pred = (pred - pred.min()) / (pred.max() - pred.min())
        pred = pred.squeeze().cpu().numpy()

    mask = Image.fromarray((pred * 255).astype(np.uint8)).resize(image.size)
    rgba = image.convert("RGBA")
    datas = rgba.getdata()

    new_data = []
    for i, item in enumerate(datas):
        r, g, b, _ = item
        a = mask.getpixel((i % image.width, i // image.width))
        new_data.append((r, g, b, a))
    rgba.putdata(new_data)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rgba.save(output_path)

def process_full_image_object(image_obj):
    """
    Process a full uploaded image object using U2NET.
    Update the processed image path and create a processing log.

    Args:
        image_obj (UploadedImage): The image object to process.
    """

    input_path = image_obj.image.path
    output_filename = f'processed/processed_{image_obj.id}.png'
    output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

    process_cropped_region(input_path, crop_region=None, output_path=output_path)

    image_obj.processed_image.name = output_filename
    image_obj.save()

    from .models import ProcessingLog
    ProcessingLog.objects.create(image=image_obj, method='full', notes='Processed full image')


def process_cropped_region_object(crop_obj):
    """
    Process a cropped region of an uploaded image object using U2NET.
    Update the processed image path and create a processing log.

    Args:
        crop_obj (CropRegion): The crop region object to process.
    """
    image_obj = crop_obj.image
    crop_data = {
        'x': crop_obj.x,
        'y': crop_obj.y,
        'width': crop_obj.width,
        'height': crop_obj.height
    }

    input_path = image_obj.image.path
    output_filename = f'processed/cropped_processed_{image_obj.id}.png'
    output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

    process_cropped_region(input_path, crop_data, output_path)

    image_obj.processed_image.name = output_filename
    image_obj.save()

    from .models import ProcessingLog
    ProcessingLog.objects.create(image=image_obj, method='crop', notes='Processed cropped region')
