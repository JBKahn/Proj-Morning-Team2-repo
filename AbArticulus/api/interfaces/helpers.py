import json
from datetime import datetime

import requests
from rest_framework import status
from social.apps.django_app.utils import load_strategy

from django.conf import settings


def get_google_api_endpoint_url(api_name, **kwargs):
    if api_name == 'calendarList':
        return 'https://www.googleapis.com/calendar/v3/users/me/calendarList'
    if api_name == 'calendars':
        return 'https://www.googleapis.com/calendar/v3/calendars'
    if api_name == 'events':
        if kwargs.get('calendar_id') is None:
            raise ValueError('Calendar id was not passed in.')
        if kwargs.get('event_id'):
            event_info = '/' + kwargs.get('event_id')
        else:
            event_info = ''
        return 'https://www.googleapis.com/calendar/v3/calendars/{}/events{}'.format(kwargs.get('calendar_id'), event_info)
    if api_name == 'acl':
        if kwargs.get('calendar_id') is None:
            raise ValueError('Calendar id was not passed in.')
        return 'https://www.googleapis.com/calendar/v3/calendars/{}/acl'.format(kwargs.get('calendar_id'))
    raise ValueError('request api endpoint not defined.')


def make_request(user, url, params=None, method="GET", data=None):
    retries = 2
    response = None
    while retries > 0 and (response is None or response.status_code != 200):
        if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
            # Our access token is likely the issue. We can use the refrest token to reauthorize ourselves.
            social = user.social_auth.get(provider='google-oauth2')
            strategy = load_strategy(response)
            social.refresh_token(strategy=strategy)
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
        else:
            raise ValueError("Only GET, DELETE, POST, and PUT are supported.")
        retries = retries - 1

    return response


def json_to_dict(event):
    return {
        'end': event.get('end') and (event.get('end').get('dateTime') or (datetime.strptime(event.get('end').get('date'), "%Y-%m-%d").isoformat())),
        'start': event.get('start') and (event.get('start').get('dateTime') or (datetime.strptime(event.get('start').get('date'), "%Y-%m-%d").isoformat())),
        'allDay': ('end' in event and 'date' in event.get('end')) or ('start' in event and 'date' in event.get('start')),
        'title': event.get('summary'),
        'id': event.get('id'),
        'sequence': event.get('sequence'),
        'description': event.get('description'),
        'isAppEvent': event.get('creator', {}).get('email') == settings.EMAIL_OF_USER_WITH_CALENDARS
    }
