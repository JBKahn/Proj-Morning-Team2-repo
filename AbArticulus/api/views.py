from rest_framework.views import APIView
from rest_framework.response import Response

from api.interfaces.api_interface import ApiInterface


class EventAPIView(APIView):
    """
    Retreives all events (only supports list).
    """

    def get(self, request, format='JSON', *args, **kwargs):
        calendars = ApiInterface.get_calendars_from_user(request.user).get('items')
        if not calendars:
            return Response()
        # temp till we define the calendar the users want.
        calendar_id = calendars[-1].get('id')
        return Response(ApiInterface.get_events_from_calendar(user=request.user, calendar_id=calendar_id))
