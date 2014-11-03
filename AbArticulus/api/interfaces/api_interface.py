from api.interfaces.google_api_interface import GoogleApiInterface
from api.interfaces.helpers import is_all_day_event, json_to_dict
from requests import codes

class ApiInterface(object):
    @classmethod
    def get_calendars_from_user(cls, user):
        response = GoogleApiInterface.get_calendars_from_user(user)
        assert response.status_code == requests.codes.ok
        return response.json()

    @classmethod
    def get_events_from_calendar(cls, user, calendar_id):
        response = GoogleApiInterface.get_events_from_calendar(user, calendar_id)
        assert response.status_code == requests.codes.ok
        formated_events = []
        for item in response.json().get('items'):
            formated_events.append(json_to_dict(item))
        return formated_events

    @classmethod
    def get_event_from_calendar(cls, user, calendar_id, event_id):
        response = GoogleApiInterface.get_event_from_calendar(user, calendar_id, event_id)
        assert response.status_code == requests.codes.ok
        event = json_to_dict(response.json())
        return event

    @classmethod
    def delete_event_from_calendar(cls, user, calendar_id, event_id):
        response = GoogleApiInterface.delete_event_from_calendar(user, calendar_id, event_id)
        assert response.status_code == requests.codes.no_content

    @classmethod
    def post_event_to_calendar(cls, user, calendar_id, event):
        '''event is a JSON request body, can be populated via create_event_json()'''
        response = GoogleApiInterface.post_event_to_calendar(user, calendar_id, event)
        assert response.status_code == requests.codes.created
        event = json_to_dict(response.json())
        return event

    @classmethod
    def put_event_to_calendar(cls, user, calendar_id, event_id, event):
        '''event is a JSON request body, can be populated via create_event_json()'''
        response = GoogleApiInterface.put_event_to_calendar(user, calendar_id, event_id, event)
        event = json_to_dict(response.json())
        return event

    @classmethod
    def create_event_json(cls, title, start, end, all_day=False, description=None, location=None):
        '''supply start and end times in YYYY-MM-DDThh:mm:dd+00:00 format'''
        body = {}
        body['summary'] = title
        body['end'] = {}
        body['start'] = {}
        if all_day:
            body['start']['date'] = start[0:10]
            body['end']['date'] = end[0:10]
        else:
            body['start']['dateTime'] = start
            body['end']['dateTime'] = end
        if description is not None:
            body['description'] = description
        if location is not None:
            body['location'] = location
        return body


    def create_event_from_request(request):
        event = ApiInterface.create_event_json(
            title=request.POST.get('title'), 
            start=request.POST.get('start'), 
            end=request.POST.get('end'), 
            all_day=request.POST.get('all_day'), 
            description=request.POST.get('description'), 
            location=request.POST.get('location')
            )
        return event