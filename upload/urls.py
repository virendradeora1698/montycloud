from django.urls import path
from upload import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('images/', views.list_images, name='list_images'),
    path('image/<int:image_id>/', views.view_image, name='view_image'),
    path('image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
]