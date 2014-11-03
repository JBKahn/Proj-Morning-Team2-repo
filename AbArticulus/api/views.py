from rest_framework.views import APIView
from rest_framework.response import Response

from api.interfaces.api_interface import ApiInterface


class EventAPIView(APIView):
    """
    Retreives all events (only supports list).
    """

    def get(self, request, format='JSON', *args, **kwargs):
        #calendars = ApiInterface.get_calendars_from_user(request.user).get('items')
        #if not calendars:
        #    return Response()
        # temp till we define the calendar the users want.
        #calendar_id = "primary" #calendars[-1].get('id')
        #return Response(ApiInterface.get_events_from_calendar(user=request.user, calendar_id=calendar_id))
        calendar_id = "primary"
        event = ApiInterface.create_event_json(title="Shit Works Even Better", start="2014-11-06T10:00:00-05:00", end="2014-11-06T12:00:00-05:00", all_day=False, description=None, location=None)
        return Response(ApiInterface.put_event_to_calendar(user=request.user, calendar_id=calendar_id, event=event, event_id="u3l4aq0opsqdqp00q8cb8llmq0"))