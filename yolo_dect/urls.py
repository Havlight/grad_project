from django.urls import path
from .views import UploadImage

urlpatterns = [
    path('', UploadImage.as_view(), name='UploadImage'),
]
