from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status


from .models import Attendance
from Users.models import User
from Clubs.models import Club

class ScanQRAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, club_id, qr_id):
        # 요청에서 사용자 가져오기
        user = request.user

        # 주어진 QR 코드 값
        given_qr_code = "https://shorturl.at/hovAJ"

        # 오늘 출석한 내역이 있는지 확인
        if Attendance.objects.filter(user=user, club_id=club_id, attendance_date=timezone.now().strftime('%Y-%m-%d')).exists():
            return Response({'status': 'error', 'message': '오늘 이미 출석하셨습니다.'}, status=status.HTTP_400_BAD_REQUEST)


        # 주어진 QR 코드 값과 입력된 qr_code_enter 값 비교
        if request.data.get('qr_code_enter') == given_qr_code:
            # QR 코드가 일치할 경우
            attendance_date = timezone.now().strftime('%Y-%m-%d')
            # 출석 정보 생성
            Attendance.objects.create(
                user=user,
                club_id=club_id,
                attendance_date=attendance_date,
                qr_code_enter=given_qr_code
            )
            # 현재 시간과 사용자 ID 및 사용자명 반환
            return Response({
                'status': 'success',
                'club_id': club_id,
                'message': 'QR 코드가 일치합니다.',
                'attendance_date': attendance_date,
                'user_id': user.id,
                'username': user.username
            })
        else:
            # QR 코드가 일치하지 않을 경우
            return Response({'status': 'error', 'message': 'QR 코드가 일치하지 않습니다.'})



class AttendanceListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, club_id):
        # 요청 본문에서 날짜 가져오기
        date_str = request.data.get('date')
        if not date_str:
            return Response({'status': 'error', 'message': '날짜가 제공되지 않았습니다.'}, status=400)

        try:
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'status': 'error', 'message': '유효한 날짜 형식이 아닙니다. (예: YYYY-MM-DD)'}, status=400)

        # 해당 클럽의 출석 기록 조회
        club = get_object_or_404(Club, club_id=club_id)
        attendances = Attendance.objects.filter(club=club, attendance_date__date=date)

        # 출석한 사용자 목록 생성
        attendance_list = [
            {
            # 'user_id': attendance.user.id, 
            'club_id': club_id,
            'username': attendance.user.username, 
            'date': attendance.attendance_date.strftime('%Y-%m-%d'),
            'status': 'Present' 
            }           
            for attendance in attendances
        ]

        return Response({'status': 'success', 'attendance_list': attendance_list})