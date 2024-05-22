from django.urls import path
from .views import ClubListCreateAPIView, ClubRetrieveAPIView, ClubUpdateAPIView, ClubJoinAPIView, ClubListAPIView, MyPageAPIView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('clubs/register/', ClubListCreateAPIView.as_view(), name='club-register'),
    path('allclubs/', ClubListAPIView.as_view(), name='all-clubs-list'),
    path('allclubs/<int:club_id>/', ClubRetrieveAPIView.as_view(), name='all-clubs-detail'),
    path('clubs/<int:club_id>/update/', ClubUpdateAPIView.as_view(), name='club-update'),
    path('clubs/<int:club_id>/club_code/', ClubJoinAPIView.as_view(), name='club-join'),
    path('mypage/<int:user_id>/', MyPageAPIView.as_view(), name='my-page'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
