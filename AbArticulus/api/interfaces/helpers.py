import json
from dateutil.parser import parse
from abcalendar.models import Event, Tag, Organization
from django.core.exceptions import ObjectDoesNotExist
import requests


def get_google_api_endpoint_url(api_name, **kwargs):
    if api_name == 'calendarList':
        return 'https://www.googleapis.com/calendar/v3/users/me/calendarList'
    if api_name == 'events':
        if kwargs.get('calendar_id') is None:
            raise ValueError('Calendar id was not passed in.')
        if kwargs.get('event_id'):
            event_info = '/' + kwargs.get('event_id')
        else:
            event_info = ''
        return 'https://www.googleapis.com/calendar/v3/calendars/{}/events{}'.format(kwargs.get('calendar_id'), event_info)
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
    else:
        raise ValueError("Only GET, DELETE, POST, and PUT are supported.")
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

def handle_models_for_event_creation(organization_name, tag_type, gevent_id, user):
    if not Organization.objects.filter(name=organization_name).exists():
        organization = Organization.objects.create(name=organization_name, user=user)
    else:
        organization = Organization.objects.get(name=organization_name)

    tag, _ = Tag.objects.get_or_create(tag_type=tag_type, organization=organization)
    Event.objects.create(gevent_id=gevent_id, tag=tag, user=user)

def handle_models_for_event_delete(gevent_id):
    Event.objects.get(gevent_id=gevent_id).delete()