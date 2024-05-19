from django.urls import path
from .views import ClubListCreateAPIView, ClubRetrieveAPIView

urlpatterns = [
    path('clubs/register/', ClubListCreateAPIView.as_view(), name='club-register'),
    path('allclubs/', ClubListCreateAPIView.as_view(), name='all-clubs-list'),
    path('allclubs/<int:club_id>/', ClubRetrieveAPIView.as_view(), name='all-clubs-detail'),
]
