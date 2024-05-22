# attendance/models.py
from django.db import models
from django.utils import timezone
from Users.models import User
from Clubs.models import Club

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    attendance_date = models.DateTimeField(default=timezone.now)
    qr_code_enter = models.CharField(max_length=255)
