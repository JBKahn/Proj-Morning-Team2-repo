from api.interfaces.google_api_interface import GoogleApiInterface
from api.interfaces.helpers import is_all_day_event, json_to_dict
import datetime as dt

from rest_framework import status

class ApiInterface(object):
    @classmethod
    def get_calendars_from_user(cls, user):
        response = GoogleApiInterface.get_calendars_from_user(user)
        if response.status_code != status.HTTP_200_OK:
            raise Exception(response.status_code)
        return response.json()

    @classmethod
    def get_events_from_calendar(cls, user, calendar_id):
        response = GoogleApiInterface.get_events_from_calendar(user, calendar_id)
        if response.status_code != status.HTTP_200_OK:
            raise Exception(response.status_code)
        formated_events = []
        for item in response.json().get('items'):
            formated_events.append(json_to_dict(item))
        return formated_events

    @classmethod
    def get_event_from_calendar(cls, user, calendar_id, event_id):
        response = GoogleApiInterface.get_event_from_calendar(user, calendar_id, event_id)
        if response.status_code != status.HTTP_200_OK:
            raise Exception(response.status_code)
        event = json_to_dict(response.json())
        return event

    @classmethod
    def delete_event_from_calendar(cls, user, calendar_id, event_id):
        response = GoogleApiInterface.delete_event_from_calendar(user, calendar_id, event_id)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            raise Exception(response.status_code)

    @classmethod
    def post_event_to_calendar(cls, user, calendar_id, event):
        '''event is a JSON request body, can be populated via create_event_json()'''
        response = GoogleApiInterface.post_event_to_calendar(user, calendar_id, event)
        if response.status_code != status.HTTP_200_OK:
            raise Exception(response.status_code)
        event = json_to_dict(response.json())
        return event

    @classmethod
    def put_event_to_calendar(cls, user, calendar_id, event_id, event):
        '''event is a JSON request body, can be populated via create_event_json()'''
        response = GoogleApiInterface.put_event_to_calendar(user, calendar_id, event_id, event)
        if response.status_code != status.HTTP_200_OK:
            raise Exception(response.status_code)
        event = json_to_dict(response.json())
        return event

    @classmethod
    def create_google_json(cls, title, start, end, all_day=False, description=None, location=None, recur_until=None):
        '''creates JSON formatted event data to send to Google to create a Google Calendar event times should be datetime objects'''
        if not (isinstance(start, dt.datetime) and isinstance(end, dt.datetime)):
            raise ValueError("Times must be instances of datetime.datetime")
        body = {}
        body['summary'] = title
        body['end'] = {}
        body['start'] = {}
        if recur_until is not None:
            if not isinstance(recur_until, dt.datetime):
                raise ValueError("Times must be instances of datetime.datetime")
            if start.tzinfo is None:
                raise ValueError("datetimes need tzinfo (timezones) defined for recurring events")
            body["recurrence"] = ["RRULE:FREQ=WEEKLY;UNTIL={}".format(recur_until.strftime("%Y%m%dT%H%M%SZ"))]
        if all_day:
            body['start']['date'] = start.strftime("%Y-%m-%d")
            body['end']['date'] = end.strftime("%Y-%m-%d")
        else:
            body['start']['dateTime'] = start.strftime("%Y-%m-%dT%H:%M:%S%z")
            body['end']['dateTime'] = end.strftime("%Y-%m-%dT%H:%M:%S%z")
        body['end']['timeZone'] = str(start.tzinfo)
        body['start']['timeZone'] = str(start.tzinfo)

        if description is not None:
            body['description'] = description
        if location is not None:
            body['location'] = location
        return body


    @classmethod
    def create_event_from_request(cls, request):
        return ApiInterface.create_event_json(
            title=request.POST.get('title'), 
            start=request.POST.get('start'), 
            end=request.POST.get('end'), 
            all_day=request.POST.get('all_day'), 
            description=request.POST.get('description'), 
            location=request.POST.get('location'),
            recur_until=request.POST.get('recur_until')
        )