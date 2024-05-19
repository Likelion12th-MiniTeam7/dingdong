from django.urls import path
from .views import get_qr_image

urlpatterns = [
    path('get-qr-image/', get_qr_image, name='get_qr_image'),
]
