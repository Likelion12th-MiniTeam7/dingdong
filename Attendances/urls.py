# attendance/urls.py
from django.urls import path
from .views import ScanQRAPIView, AttendanceListAPIView

urlpatterns = [
    path('mypage/clubs/<int:club_id>/scan_qr/<int:qr_id>/', ScanQRAPIView.as_view(), name='scan-qr'),
    path('mypage/clubs/<int:club_id>/attendance/', AttendanceListAPIView.as_view(), name='attendance-list'),

]
