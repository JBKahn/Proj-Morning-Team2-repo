import requests
from dateutil.parser import parse
import json

def get_google_api_endpoint_url(api_name, **kwargs):
    if api_name == 'calendarList':
        return 'https://www.googleapis.com/calendar/v3/users/me/calendarList'
    if api_name == 'events':
        if kwargs.get('calendar_id') is None:
            raise ValueError('Calendar id was not passing in `id_num`.')
        if kwargs.get('event_id') is None:
            return 'https://www.googleapis.com/calendar/v3/calendars/{}/events'.format(kwargs.get('calendar_id'))
        return 'https://www.googleapis.com/calendar/v3/calendars/{}/events/{}'.format(kwargs.get('calendar_id'), kwargs.get('event_id'))
    raise ValueError('request api endpoint not defined.')


def make_request(user, url, params=None, method="GET", data=None):
    # Default params will pass other params if we need more.
    if params is None:
        social = user.social_auth.get(provider='google-oauth2')
        params = {'access_token': social.extra_data['access_token']}
    if method == "GET":
        response = requests.get(
            url=url,
            params=params
        )
    elif method == "DELETE":
        response = requests.delete(
            url=url,
            params=params
        )
    elif method == "POST":
        response = requests.post(
            url=url,
            data=json.dumps(data),
            params=params,
            headers={"Content-Type": "application/json"}
        )
    elif method == "PUT":
        response = requests.put(
            url=url,
            data=json.dumps(data),
            params=params,
            headers={"Content-Type": "application/json"}
        )
    return response


def is_all_day_event(end):
    parsed_time = end and end.get('dateTime') and parse(end.get('dateTime'))
    hour = parsed_time and parsed_time.hour
    minute = parsed_time and parsed_time.minute
    return hour == minute == 0

def json_to_dict(event):
    return {
            'end': event.get('end') and event.get('end').get('dateTime'),
            'start': event.get('start') and event.get('start').get('dateTime'),
            'allDay': is_all_day_event(event.get('end')),
            'title': event.get('summary'),
            'id': event.get('id'),
        }
