from django.db import models
from django.utils import timezone
from QRs.models import QRCode 
from Users.models import User


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
    club_pic = models.ImageField(upload_to='club_pics/', null=True, blank=True)  

    club_code = models.CharField(max_length=50)  

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clubs')

    members = models.ManyToManyField(User, related_name='joined_clubs')  # Many-to-Many 필드 추가
    member_count = models.PositiveIntegerField(default=0)  # 회원 수를 저장할 필드 추가


    @property
    def remaining_days(self):
        remaining_days = (self.club_open_end - self.club_open_start).days
        return remaining_days

    def save(self, *args, **kwargs):
        # 두 날짜 간의 차이 계산
        time_diff = (self.club_open_end - self.club_open_start).days
        # 차이가 음수이면 club_open을 False로 설정
        if time_diff < 0:
            self.club_open = False
        super().save(*args, **kwargs)    

    def __str__(self):
        return self.club_name

    def qr_code(self):
        qr_code = QRCode.objects.first()
        if qr_code is not None:
            qr_code = qr_code.image_url
            return qr_code
        else:
            return None
        
    def save(self, *args, **kwargs):
        today = timezone.now().date()
        if self.club_open_start <= today <= self.club_open_end:
            self.club_open = True
        else:
            self.club_open = False
        super().save(*args, **kwargs)
    
    def update_member_count(self):
        self.member_count = self.members.count()
        self.save()