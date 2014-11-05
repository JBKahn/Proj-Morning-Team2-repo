from rest_framework.views import APIView
from rest_framework.response import Response
import pytz
import datetime as dt

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
        local = pytz.timezone("America/Toronto")
        start = dt.datetime(2014, 11, 6, 12, 0)
        end = dt.datetime(2014, 11, 6, 13, 0)
        recur_until = dt.datetime(2014, 11, 14, 13, 0)
        start = local.localize(start)
        end = local.localize(end)
        recur_until = local.localize(recur_until)


        event = ApiInterface.create_google_json(title="fweuifhqewfiu", start=start, end=end, all_day=False, description=None, location=None, recur_until=recur_until)
        #return Response(ApiInterface.put_event_to_calendar(user=request.user, calendar_id=calendar_id, event=event, event_id="5su69nirj9n317s1nadchmq4mk"))
        return Response(ApiInterface.post_event_to_calendar(user=request.user, calendar_id=calendar_id, event=event))
        #return Response(ApiInterface.delete_event_from_calendar(user=request.user, calendar_id=calendar_id, event_id="rgpp3uibv8m3ks6namrdave7no"))