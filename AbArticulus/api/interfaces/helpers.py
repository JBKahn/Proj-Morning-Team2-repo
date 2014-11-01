import requests
from dateutil.parser import parse


def get_google_api_endpoint_url(api_name, **kwargs):
    if api_name == 'calendarList':
        return 'https://www.googleapis.com/calendar/v3/users/me/calendarList'
    if api_name == 'events':
        if kwargs.get('calendar_id') is None:
            raise ValueError('Calendar id was not passing in `id_num`.')
        return 'https://www.googleapis.com/calendar/v3/calendars/{}/events'.format(kwargs.get('calendar_id'))
    raise ValueError('request api endpoint not defined.')


def make_request(user, url, params=None):
    # Default params will pass other params if we need more.
    if params is None:
        social = user.social_auth.get(provider='google-oauth2')
        params = {'access_token': social.extra_data['access_token']}
    response = requests.get(
        url=url,
        params=params
    )
    return response


def is_all_day_event(end):
    parsed_time = end and end.get('dateTime') and parse(end.get('dateTime'))
    hour = parsed_time and parsed_time.hour
    minute = parsed_time and parsed_time.minute
    return hour == minute == 0