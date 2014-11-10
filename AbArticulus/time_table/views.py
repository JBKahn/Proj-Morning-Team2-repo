from rest_framework.views import APIView
from rest_framework.response import Response

from abcalendar.constants import TAG_CHOICES
from api.interfaces.api_interface import ApiInterface
from time_table.serializers import SimpleEventSerializer, SimpleEventUpdateSerializer, SimpleTagSerializer

from django.views.generic import TemplateView


class TimeTableHomeView(TemplateView):
    template_name = 'time_table_home.html'

    def get_context_data(self, **kwargs):
        context = super(TimeTableHomeView, self).get_context_data(**kwargs)
        context['tag_types'] = [choice[0].capitalize() for choice in TAG_CHOICES]
        return context


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
        event_serializer = SimpleEventSerializer(data=request.DATA)
        tag_serializer = SimpleTagSerializer(data=request.DATA)
        if event_serializer.is_valid() and tag_serializer.is_valid():
            new_event_data = ApiInterface.add_user_event(user=request.user, calendar_id=request.DATA.get('calendar'), event_data=event_serializer.data, tag_data=tag_serializer.data)
            new_event_data['calendar_id'] = request.DATA.get('calendar')
            return Response(new_event_data)


class EventAccessView(APIView):
    calendar_id = "primary"

    def get(self, request, event_id, format='JSON', *args, **kwargs):
        return Response(ApiInterface.get_event_from_calendar(user=request.user, calendar_id=self.calendar_id, event_id=event_id))

    def put(self, request, event_id, format='JSON', *args, **kwargs):
        event_serializer = SimpleEventUpdateSerializer(data=request.DATA)
        if event_serializer.is_valid():
            json_event = ApiInterface.create_event_from_dict(dict(event_serializer.data))
            event_data = ApiInterface.user_update_event(user=request.user, calendar_id=request.DATA.get('calendar'), gevent_id=event_serializer.data.get('id'), event_data=json_event, revision=request.DATA.get('sequence'))
            event_data['calendar_id'] = request.DATA.get('calendar')
            return Response(event_data)

    def delete(self, request, event_id, format='JSON', *args, **kwargs):
        return Response(ApiInterface.get_event_from_calendar(user=request.user, calendar_id=self.calendar_id, event_id=event_id))
