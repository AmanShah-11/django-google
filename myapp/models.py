from django.db import models
from django.utils.timezone import now
# Create your models here.


class ScheduleUsers(models.Model):
    def __str__(self):
        return self.firstname

    def get_location(self):
        return str(self.city + ", " + "ON")

    def print_city(self):
        return self.city

    def print_name(self):
        return self.firstname

    CHOICES = (
        ('AB', 'Alberta'),
        ('BC', 'British Columbia'),
        ('MN', 'Manitoba'),
        ('NB', 'New Brunswick'),
        ('NL', 'Newfoundland and Labrador'),
        ('NWT', 'Northwest Terrorities'),
        ('NS', 'Nova Scotia'),
        ('NV', 'Nunavut'),
        ('ON', 'Ontario'),
        ('PEI', 'Prince Edward Island'),
        ('QB', 'Quebec'),
        ('SAS', 'Saskatchewan'),
        ('YUK', 'Yukon'),
    )
    firstname = models.CharField(max_length=150, default="")
    lastname = models.CharField(max_length=150, default="")
    email = models.CharField(max_length=150, default="")
    city = models.CharField(max_length=150, default="")
    province = models.CharField(max_length=150, choices=CHOICES, default="ON")
    address = models.CharField(max_length=150, default="")


class Schedule(models.Model):
    time_start = models.TimeField(max_length=50, default="09:00")
    time_end = models.TimeField(max_length=50, default="12:00")
    date = models.DateField(max_length=50, default=now())
    activity = models.CharField(max_length=50, default="Korean Food")
    user_invite = models.ForeignKey(ScheduleUsers, on_delete=models.CASCADE, max_length=50, default="none")
