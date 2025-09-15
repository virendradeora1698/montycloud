import os
import uuid
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import redirect
from upload.db import (
    save_image_metadata,
    get_image_metadata,
    delete_image_metadata,
    list_images_metadata
)
from upload.models import Image

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        name =  image_file.name

        # Create a new image entry
        user = request.POST.get('user', '')
        image = Image(user=user, image=image_file,  name=name)
        image.save()

        url = image.image.url
        save_image_metadata(str(image.id), user, name, url)

        return JsonResponse({
            'id': image.id,
            'user': image.user,
            'image': image.image.url,
            'name': image.name,
            'created_at': image.created_at,
            'updated_at': image.updated_at
        }, status=201)
        

    return JsonResponse({"error": "No image provided."}, status=400)



def list_images(request):
    name = request.GET.get('name', None)
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)
    images = list_images_metadata(name=name, from_date=from_date, to_date=to_date)

    return JsonResponse(images, safe=False)

def view_image(request, image_id):
    image_id = str(image_id)
    image = get_image_metadata(image_id)
    if not image:
        return JsonResponse({"error": "Image not found."}, status=404)

    return redirect(image['image_url'])

@csrf_exempt
def delete_image(request, image_id):
    image_id = str(image_id)
    image = get_image_metadata(image_id)
    if not image:
        return JsonResponse({"error": "Image not found."}, status=404)

    # Check if the current user owns the image (assuming request.user.username)
    # if image['user'] != getattr(request.user, 'username', ''):
        # return JsonResponse({"error": "You do not have permission to delete this image."}, status=403)

    # Delete image file
    file_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(image['image_url']))
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete metadata from DynamoDB
    delete_image_metadata(image_id)
    return JsonResponse({"message": "Image deleted successfully."}, status=204)



@csrf_exempt
def update_image(request, image_id):
    if request.method == 'PUT':
        image = get_image_metadata(image_id)
        if not image:
            return JsonResponse({"error": "Image not found."}, status=404)

        data = json.loads(request.body.decode("utf-8"))
        new_name = data.get("name", image['name'])
        new_user = data.get("user", image['user'])

        # Update DynamoDB
        save_image_metadata(str(image_id), new_user, new_name, image['image_url'])
        return JsonResponse({"message": "Image updated successfully."})

