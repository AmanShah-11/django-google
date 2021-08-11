from __future__ import print_function

import requests
from urllib.parse import urlencode
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

with open("myapp/secrets.txt", "r") as file:
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
        # print(url_params)
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
        # print(r.text, places_url)
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
        # print(detail_url)
        r = requests.get(detail_url)
        # print(r.text, detail_url)
        if r.status_code not in range(200, 299):
            return {}
        return r

    def add_event(self, start_time, end_time, date, address_info, location_name, email):
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
            # if creds and creds.expired and creds.refresh_token:
            #     creds.refresh(Request())
            # else:
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