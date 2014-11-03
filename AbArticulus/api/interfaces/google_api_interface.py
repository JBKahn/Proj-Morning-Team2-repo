from api.interfaces.helpers import get_google_api_endpoint_url, make_request


class GoogleApiInterface(object):
    @classmethod
    def get_calendars_from_user(cls, user):
        url = get_google_api_endpoint_url(api_name="calendarList")
        return make_request(user=user, url=url, params=None)

    @classmethod
    def get_events_from_calendar(cls, user, calendar_id):
        url = get_google_api_endpoint_url(api_name="events", calendar_id=calendar_id)
        return make_request(user=user, url=url, params=None)

    @classmethod
    def get_event_from_calendar(cls, user, calendar_id, event_id):
        url = get_google_api_endpoint_url(api_name="events", calendar_id=calendar_id, event_id=event_id)
        return make_request(user=user, url=url, params=None)

    @classmethod
    def delete_event_from_calendar(cls, user, calendar_id, event_id):
        url = get_google_api_endpoint_url(api_name="events", calendar_id=calendar_id, event_id=event_id)
        return make_request(user=user, url=url, params=None, method="DELETE")

    @classmethod
    def post_event_to_calendar(cls, user, calendar_id, event):
        url = get_google_api_endpoint_url(api_name="events", calendar_id=calendar_id)
        return make_request(user=user, url=url, data=event, method="POST")

    @classmethod
    def put_event_to_calendar(cls, user, calendar_id, event_id, event):
        url = get_google_api_endpoint_url(api_name="events", calendar_id=calendar_id, event_id=event_id)
        return make_request(user=user, url=url, data=event, method="PUT")