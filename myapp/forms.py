from django import forms

from .models import Schedule,ScheduleUsers


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ["user"]


class ScheduleUsersForm(forms.ModelForm):
    class Meta:
        model = ScheduleUsers
        exclude = ["user"]

