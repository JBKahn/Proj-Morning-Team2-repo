from datetime import datetime

from api.interfaces.google_api_interface import GoogleApiInterface
from api.interfaces.helpers import json_to_dict

from rest_framework import status


class ApiInterface(object):
    @classmethod
    def get_calendars_from_user(cls, user):
        response = GoogleApiInterface.get_calendars_from_user(user)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        return response.json()

    @classmethod
    def get_events_from_calendar(cls, user, calendar_id):
        response = GoogleApiInterface.get_events_from_calendar(user, calendar_id)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        formated_events = []
        for item in response.json().get('items'):
            formated_events.append(json_to_dict(item))
        return formated_events

    @classmethod
    def get_event_from_calendar(cls, user, calendar_id, event_id):
        response = GoogleApiInterface.get_event_from_calendar(user, calendar_id, event_id)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        event = json_to_dict(response.json())
        return event

    @classmethod
    def delete_event_from_calendar(cls, user, calendar_id, event_id):
        response = GoogleApiInterface.delete_event_from_calendar(user, calendar_id, event_id)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            raise UnexpectedResponseError(response.status_code)

    @classmethod
    def post_event_to_calendar(cls, user, calendar_id, event, tag, org):
        '''event is a JSON request body, can be populated via create_event_json()'''
        # We need to instantiate a new google event object after creating the Tag, Vote and Event on our side.
        # None of these models are saved.
        # By doing that, we can attach the serialized version of our event, using the model serializer and
        # save ourselves any work, onto the description field the first time.

        # Check if the Tag exsists for our Calendar. If it does then check if an event with the same event info exists.
        # If it does, respond with such a message. Otherwise Continue.
        response = GoogleApiInterface.post_event_to_calendar(user, calendar_id, event)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        # we save the Google Event with the google id. Then we save the other models.
        event = json_to_dict(response.json())
        return event

    @classmethod
    def put_event_to_calendar(cls, user, calendar_id, event_id, event):
        '''event is a JSON request body, can be populated via create_event_json()'''
        # get the GoogleEvent model and use the serializer to generate the description.
        response = GoogleApiInterface.put_event_to_calendar(user, calendar_id, event_id, event)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        event = json_to_dict(response.json())
        return event

    @classmethod
    def add_user_event(cls, user, calendar_id, event, tag, org):
        # If an event with the same info already exists:
        #   Add my vote.
        # otherwise:
        #   Add another event to our DB along with a vote. Create the Tag if it does not exists.
        # If it is for a new tag:
        #   post_event_to_calendar.
        # Otherwise:
        #   Take the most unvoted thing
        #   if it has 0 or more votes:
        #       if the second place has les than 0 votes we need to get the old GoogleEvent and update the gevent_id.
        #       put_event_to_calendar with that info
        #   else:
        #       delete_event_from_calendar
        pass

    @classmethod
    def create_google_json(cls, title, start, end, all_day=False, description=None, location=None, recur_until=None):
        '''creates JSON formatted event data to send to Google to create a Google Calendar event times should be datetime objects'''
        if not (isinstance(start, datetime) and isinstance(end, datetime)):
            raise ValueError("Times must be instances of datetime.datetime")

        if all_day:
            time_format = "%Y-%m-%d"
        else:
            time_format = "%Y-%m-%dT%H:%M:%S%z"

        body = {
            'summary': title,
            'start': {
                'dateTime': start.strftime(time_format),
                'timeZone': str(start.tzinfo)
            },
            'end': {
                'dateTime': end.strftime(time_format),
                'timeZone': str(start.tzinfo)
            },
        }

        if recur_until is not None:
            if not isinstance(recur_until, datetime):
                raise ValueError("Times must be instances of datetime.datetime")
            if start.tzinfo is None:
                raise ValueError("datetimes need tzinfo (timezones) defined for recurring events")
            body["recurrence"] = ["RRULE:FREQ=WEEKLY;UNTIL={}".format(recur_until.strftime("%Y%m%dT%H%M%SZ"))]
        if description is not None:
            body['description'] = description
        if location is not None:
            body['location'] = location
        return body

    @classmethod
    def create_event_from_dict(cls, info):
        return ApiInterface.create_google_json(
            title=info.get('title'),
            start=info.get('start'),
            end=info.get('end'),
            all_day=info.get('all_day'),
            description=info.get('description'),
            location=info.get('location'),
            recur_until=info.get('recur_until')
        )


class UnexpectedResponseError(Exception):
    pass
