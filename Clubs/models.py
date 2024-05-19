from django.db import models
from django.utils import timezone

class Club(models.Model):
    club_id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=100)
    club_time = models.CharField(max_length=100)
    club_introduction = models.TextField()
    club_details = models.TextField()
    club_contact = models.CharField(max_length=100)
    club_open = models.BooleanField(default=True)
    club_open_start = models.DateField(default=timezone.now)
    club_open_end = models.DateField()

    @property
    def remaining_days(self):
        remaining_days = (self.club_open_end - self.club_open_start).days
        return remaining_days

    def __str__(self):
        return self.club_name
