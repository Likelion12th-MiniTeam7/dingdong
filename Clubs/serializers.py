from rest_framework import serializers
from .models import Club
from rest_framework_simplejwt.authentication import JWTAuthentication

class ClubSerializer(serializers.ModelSerializer):
    remaining_days = serializers.IntegerField(read_only=True)
    created_by = serializers.CharField(read_only=True)  # username을 저장하기 위해 CharField로 변경

    class Meta:
        model = Club
        fields = ['club_id', 'club_name', 'club_time', 'club_introduction', 
                    'club_details', 'club_contact', 'club_open', 
                    'club_open_start', 'club_open_end', 'club_code', 'club_pic', 'remaining_days', 
                    'created_by', 'qr_code']

    def create(self, validated_data):
        # 현재 요청을 보낸 사용자의 정보를 가져옴
        user = self.context['request'].user
        # 사용자 객체를 created_by 필드에 할당
        validated_data['created_by'] = user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # created_by 필드는 수정할 수 없도록 설정
        validated_data.pop('created_by', None)
        return super().update(instance, validated_data)
        
class ClubMemberInfoSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ['members', 'member_count']

    def get_members(self, obj):
        members = obj.members.all()
        member_data = {member.id: member.username for member in members}
        return member_data

    def get_member_count(self, obj):
        return obj.members.count()
    
class ClubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['club_id', 'club_name', 'club_introduction', 
                    'club_open', 'club_pic', 'remaining_days']
