from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from abcalendar.constants import TAG_CHOICES
from abcalendar.models import Calendar
from api.interfaces.api_interface import ApiInterface
from time_table.serializers import SimpleEventSerializer, SimpleEventUpdateSerializer, SimpleTagSerializer, SimpleCalendarSerializer, SimpleDatabaseCalendarSerializer

from django.conf import settings
from django.views.generic import TemplateView


class TimeTableHomeView(TemplateView):
    template_name = 'time_table_home.html'

    def get_context_data(self, **kwargs):
        context = super(TimeTableHomeView, self).get_context_data(**kwargs)
        context['tag_types'] = [choice[0].capitalize() for choice in TAG_CHOICES]
        return context


class EventCreateView(APIView):
    def get(self, request, format='JSON', *args, **kwargs):
        calendars = ApiInterface.get_calendars_from_user(user=request.user)
        event_sources = {}
        for item in calendars.get('items'):
            # hack till I figure out why that doesn't work.
            if u"group.v.calendar.google.com" not in item.get('id'):
                event_sources[item.get('summary')] = {
                    'events': ApiInterface.get_events_from_calendar(user=request.user, calendar_id=item.get('id')),
                    'id': item.get('id'),
                    'canCreateEvents': item.get('accessRole') in [u'writer', u'owner'],
                    'isAppCalendar': Calendar.objects.filter(gid=item.get('id')).exists() or item.get('id') == settings.EMAIL_OF_USER_WITH_CALENDARS
                }
        return Response(event_sources)

    def post(self, request, format='JSON', *args, **kwargs):
        event_serializer = SimpleEventSerializer(data=request.DATA)
        tag_serializer = SimpleTagSerializer(data=request.DATA)
        if event_serializer.is_valid() and (not Calendar.objects.filter(gid=request.DATA.get('calendar')).exists() or tag_serializer.is_valid()):
            new_event_data = ApiInterface.add_user_event(user=request.user, calendar_id=request.DATA.get('calendar'), event_data=event_serializer.data, tag_data=tag_serializer.data)
            new_event_data['calendar_id'] = request.DATA.get('calendar')
            return Response(new_event_data)
        errors = {}
        errors.update(event_serializer.errors)
        errors.update(tag_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id, format='JSON', *args, **kwargs):
        return Response(ApiInterface.get_event_from_calendar(user=request.user, calendar_id=self.calendar_id, event_id=event_id))


class CalendarListCreateView(APIView):
    def get(self, request, format='JSON', *args, **kwargs):
        calendars = SimpleDatabaseCalendarSerializer(Calendar.objects.exclude(name=settings.EMAIL_OF_USER_WITH_CALENDARS), many=True)
        return Response(calendars.data)

    def post(self, request, format='JSON', *args, **kwargs):
        calendar_serializer = SimpleCalendarSerializer(data=request.DATA)
        if calendar_serializer.is_valid():
            new_calendar_data = ApiInterface.user_add_calendar(user=request.user, title=calendar_serializer.data.get('title'))
            return Response(new_calendar_data)
        return Response(calendar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
