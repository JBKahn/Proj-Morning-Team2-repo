from rest_framework.views import APIView
from rest_framework.response import Response

from api.interfaces.api_interface import ApiInterface
from time_table.serializers import SimpleEventSerializer, SimpleEventUpdateSerializer

from django.views.generic import TemplateView


class TimeTableHomeView(TemplateView):
    template_name = 'time_table_home.html'


class EventCreateView(APIView):
    calendar_id = "primary"

    def get(self, request, format='JSON', *args, **kwargs):
        calendars = ApiInterface.get_calendars_from_user(user=request.user)
        event_sources = {}
        for item in calendars.get('items'):
            # hack till I figure out why that doesn't work.
            if u"group.v.calendar.google.com" not in item.get('id'):
                event_sources[item.get('summary')] = {
                    'events': ApiInterface.get_events_from_calendar(user=request.user, calendar_id=item.get('id')),
                    'id': item.get('id'),
                    'role': item.get('accessRole')
                }
        return Response(event_sources)

    def post(self, request, format='JSON', *args, **kwargs):
        serializer = SimpleEventSerializer(data=request.DATA)
        if serializer.is_valid():
            json_event = ApiInterface.create_event_from_dict(dict(serializer.data))
            new_event_data = ApiInterface.add_user_event(user=request.user, calendar_id=request.DATA.get('calendar'), event_data=json_event, tag_data='')
            new_event_data['calendar_id'] = request.DATA.get('calendar')
            return Response(new_event_data)


class EventAccessView(APIView):
    calendar_id = "primary"

    def get(self, request, event_id, format='JSON', *args, **kwargs):
        return Response(ApiInterface.get_event_from_calendar(user=request.user, calendar_id=self.calendar_id, event_id=event_id))

    def put(self, request, event_id, format='JSON', *args, **kwargs):
        serializer = SimpleEventUpdateSerializer(data=request.DATA)
        if serializer.is_valid():
            json_event = ApiInterface.create_event_from_dict(dict(serializer.data))
            return Response(ApiInterface.user_update_event(user=request.user, calendar_id=request.DATA.get('calendar'), gevent_id=serializer.data.get('id'), event_data=json_event, revision=request.DATA.get('sequence')))

    def delete(self, request, event_id, format='JSON', *args, **kwargs):
        return Response(ApiInterface.get_event_from_calendar(user=request.user, calendar_id=self.calendar_id, event_id=event_id))
