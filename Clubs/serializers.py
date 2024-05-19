from rest_framework import serializers
from .models import Club

class ClubSerializer(serializers.ModelSerializer):
    remaining_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = Club
        fields = ['club_id', 'club_name', 'club_time', 'club_introduction', 'club_details', 'club_contact', 'club_open', 'club_open_start', 'club_open_end', 'remaining_days']
