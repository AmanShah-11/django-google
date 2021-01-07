from __future__ import print_function

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .forms import ScheduleForm, ScheduleUsersForm

from rest_framework import viewsets
from .models import Schedule, ScheduleUsers
from .serializers import ScheduleSerializer
from .myapi import GoogleMapsClient
from .myapi import GOOGLE_API_KEY


def schedule(request):
    client = GoogleMapsClient(api_key=GOOGLE_API_KEY)
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            form_instance = form.save(commit=False)

            new_object = ScheduleUsers.objects.filter(firstname=form_instance.user_invite)

            address_info_list = list(new_object.values_list('address', 'city', 'province'))
            address_info_tuple = address_info_list[0]
            address_info = ", ".join(address_info_tuple)

            email_info_list = list(new_object.values_list('email'))
            email_info = email_info_list[0]

            answer = client.search(form_instance.activity, location=address_info)

            results_list = (answer["results"])
            location_name = (results_list[0]["name"])
            location_lat_lng = (results_list[0]["geometry"]["location"])
            location_address = (results_list[0]["vicinity"])

            if answer != "":
                messages.success(request, 'The response is {}'.format("GOOD!"))
                messages.success(request, 'The name of the place is {}'.format(location_name))
                messages.success(request, "The lat/lng of the place is {}".format(location_lat_lng))
                messages.success(request, "The starting time for the event is {}".format(form_instance.time_start))
                messages.success(request, "The MAP URL! {}".format(client.roads(
                    address_info
                ).url))

                client.add_event(
                    form_instance.time_start,
                    form_instance.time_end,
                    form_instance.date,
                    address_info,
                    location_address,
                    email_info
                )
    form = ScheduleForm()

    return render(request, 'myapp/form.html', {'form': form})


def detail(request, question_id):
    question = get_object_or_404(Schedule, pk=question_id)
    return render(request, 'myapp/form.html', {'question': question})


def users(request):
    if request.method == "POST":
        form = ScheduleUsersForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ScheduleUsersForm()
    return render(request, 'myapp/form.html', {'form': form})


class EventsView(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()
