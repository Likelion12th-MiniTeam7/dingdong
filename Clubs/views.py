from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Club
from .serializers import ClubSerializer, ClubMemberInfoSerializer, ClubListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied


class ClubListCreateAPIView(generics.ListCreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        # 현재 로그인한 사용자 정보를 얻음
        user = self.request.user
        # 동아리 생성 시 사용자 정보 추가
        serializer.save(created_by=user)


class ClubListAPIView(generics.ListCreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubListSerializer

class ClubUpdateAPIView(generics.UpdateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    lookup_field = 'club_id'
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        club = self.get_object()
        if self.request.user != club.created_by:
            raise PermissionDenied("You do not have permission to edit this club.")
        serializer.save()

class ClubRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    lookup_field = 'club_id'



class ClubJoinAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, club_id):
        # 사용자가 로그인하지 않은 경우 오류 메시지 반환
        if not request.user.is_authenticated:
            return Response({"detail": "You must be logged in to join a club."}, status=status.HTTP_401_UNAUTHORIZED)

        club = get_object_or_404(Club, pk=club_id)

        # POST 데이터에서 club_code_enter를 가져옴
        club_code_enter = request.data.get('club_code_enter')

        if club_code_enter is None:
            return Response({"detail": "Club code is required."}, status=status.HTTP_400_BAD_REQUEST)

        # club_code_enter가 club_code와 일치하는지 확인
        if club_code_enter != club.club_code:
            return Response({"detail": "The club code is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        # 동아리 만든 사람인지 확인 
        if club.created_by == request.user:
            return Response({"detail": "You are already a member of this club."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 이미 가입한 사용자인지 확인
        if club.members.filter(pk=request.user.pk).exists():
            return Response({"detail": "You are already a member of this club."}, status=status.HTTP_400_BAD_REQUEST)

        # 동아리에 가입
        club.members.add(request.user)
        
        # 회원 수 업데이트
        club.member_count = club.members.count()
        club.save()

        # ClubSerializer를 사용하여 동아리 정보를 직렬화하여 반환
        serializer = ClubMemberInfoSerializer(club)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


User = get_user_model()

class MyPageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        # 현재 로그인한 사용자와 요청한 사용자가 일치하는지 확인
        if request.user != user:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        # 사용자가 등록한 동아리
        registered_clubs = Club.objects.filter(created_by=user)
        registered_clubs_data = [
            {
                "club_id": club.club_id,
                "name": club.club_name,
                "QR": club.qr_code() 
            }
            for club in registered_clubs
        ]

        # 사용자가 가입한 동아리
        joined_clubs = Club.objects.filter(members=user)
        joined_clubs_data = [
            {
                "club_id": club.club_id,
                "name": club.club_name
            }
            for club in joined_clubs
        ]

        data = {
            "user_id": user.id,
            "name": user.username,  # 혹은 user.get_full_name() 등 필요에 따라 변경
            "registered_clubs": registered_clubs_data,
            "joined_clubs": joined_clubs_data
        }

        return Response(data, status=status.HTTP_200_OK)