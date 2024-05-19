from django.db import models

class QRCode(models.Model):
    image_url = models.CharField(max_length=255)

    class Meta:
        db_table = 'dingdong_qr'