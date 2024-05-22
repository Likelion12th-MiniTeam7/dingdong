from django.http import JsonResponse
from .models import QRCode

def get_qr_image(request):
    qr_code = QRCode.objects.first()
    if qr_code is not None:
        qr_code = qr_code.image_url
        return JsonResponse({'qr_image_url': qr_code})
    else:
        return JsonResponse({'error': 'No QRCode found'}, status=404)
