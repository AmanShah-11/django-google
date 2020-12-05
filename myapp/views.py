from __future__ import print_function

from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .forms import ScheduleForm, ScheduleUsersForm
import requests
from urllib.parse import urlencode
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .models import Schedule, ScheduleUsers

with open("secrets.txt", "r") as file:
    first_line = file.readline()

GOOGLE_API_KEY = first_line


class GoogleMapsClient(object):
    lat = None
    lng = None
    data_type = 'json'
    location_query = None
    api_key = None

    def __init__(self, api_key=None, address_or_postal_code=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if api_key == None:
            raise Exception("API Key is required")
        self.api_key = api_key
        self.location_query = address_or_postal_code
        if self.location_query != None:
            self.extract_lat_lng(self.location_query)

    def extract_lat_lng(self, location=None):
        loc_query = self.location_query
        if location != None:
            loc_query = location
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
        params = {"address": loc_query, "key": self.api_key}
        url_params = urlencode(params)
        print(url_params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
        if r.status_code not in range(200, 299):
            return {}
        latlng = {}
        try:
            latlng = r.json()["results"][0]['geometry']['location']
        except:
            pass
        lat, lng = latlng.get("lat"), latlng.get("lng")
        self.lat = lat
        self.lng = lng
        return lat, lng

    def search(self, keyword=None, radius=1000, location=None):
        lat, lng = self.lat, self.lng
        if location != None:
            lat, lng = self.extract_lat_lng(location=location)
        endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/{}".format(self.data_type)
        params = {
            "key": self.api_key,
            "location": f"{lat}, {lng}",
            "radius": radius,
            "language": "en",
            "keyword": keyword,
        }
        params_encoded = urlencode(params)
        places_url = f"{endpoint}?{params_encoded}"
        r = requests.get(places_url)
        print(r.text, places_url)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def roads(self, location=None):
        lat, lng = self.lat, self.lng
        if location != None:
            lat, lng = self.extract_lat_lng(location=location)
        detail_based_endpoint = "https://maps.googleapis.com/maps/api/streetview"
        detail_based_params = {
            "size": "300x300",
            "location": f"{lat}, {lng}",
            "key": self.api_key,
        }
        detail_params_encoded = urlencode(detail_based_params)
        detail_url = f"{detail_based_endpoint}?{detail_params_encoded}"
        print(detail_url)
        r = requests.get(detail_url)
        print(r.text, detail_url)
        if r.status_code not in range(200, 299):
            return {}
        return r

    def add_event(self, start_time, end_time, date, address_info, location_name, email):
        print(date)
        print(start_time)
        print(end_time)
        print(email)
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.abspath(r'C:\Users\Aman\PycharmProjects\djangogoogle\djangogoogle\myapp\credentials.json'),
                    ['https://www.googleapis.com/auth/calendar']
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        event = {
            'summary': location_name,
            'location': address_info,
            'description': 'An automated event made from Google Calendar API',
            'start': {
                'dateTime': f'{date}T{start_time}',
                'timeZone': 'GMT-5:00',
            },
            'end': {
                'dateTime': f'{date}T{end_time}',
                'timeZone': 'GMT-5:00',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'attendees': [
                {'email': email},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        service = build('calendar', 'v3', credentials=creds)
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return event


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


def events(request):
    # if request.method == "POST":
    #     pass
    model = Schedule.objects.all().values_list(
        "time_start",
        "time_end",
        "activity",
        "user_invite"
    )
    return render(
        request,
        'myapp/detail.html',
        {'model': model}
    )


def to_integer(dt):
    return int(10000 * dt.year + 100 * dt.month + dt.day)