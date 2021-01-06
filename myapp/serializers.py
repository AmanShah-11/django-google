from rest_framework import serializers
from .models import Schedule
import datetime


class ScheduleSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    def get_completed(self, obj):
        time_difference = datetime.date.today() - obj.date
        if (time_difference.total_Seconds() >= 0):
            return True
        return False

    class Meta:
        model = Schedule
        fields = ("id", "time_start", "time_end", "date", "activity", "user_invite", "completed")
