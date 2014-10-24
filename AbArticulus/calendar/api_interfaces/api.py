from calendar.api_interfaces.gapi import GoogleApiInterface
from calendar.api_interfaces.helpers import is_all_day_event


class ApiInterface(object):
    @classmethod
    def get_calendars_from_user(cls, user):
        response = GoogleApiInterface.get_calendars_from_user(user)
        return response.json()

    @classmethod
    def get_events_from_calendar(cls, user, calendar_id):
        response = GoogleApiInterface.get_events_from_calendar(user, calendar_id)

        formated_events = []
        for item in response.json().get('items'):
            formated_events.append({
                'end': item.get('end') and item.get('end').get('dateTime'),
                'start': item.get('start') and item.get('start').get('dateTime'),
                'allDay': is_all_day_event(item.get('end')),
                'title': item.get('summary'),
                'id': item.get('id'),
            })
        return formated_events
