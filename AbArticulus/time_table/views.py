from rest_framework.views import APIView
from rest_framework.response import Response

from api.interfaces.api_interface import ApiInterface
from time_table.serializers import SimpleEventSerializer

from django.views.generic import TemplateView


class TimeTableHomeView(TemplateView):
    template_name = 'time_table_home.html'


class EventCreateView(APIView):
    calendar_id = "primary"

    def get(self, request, format='JSON', *args, **kwargs):
        return Response(ApiInterface.get_events_from_calendar(user=request.user, calendar_id=self.calendar_id))

    def post(self, request, format='JSON', *args, **kwargs):
        serializer = SimpleEventSerializer(data=request.DATA)
        if serializer.is_valid():
            json_event = ApiInterface.create_event_from_dict(dict(serializer.data))
            return Response(ApiInterface.post_event_to_calendar(user=request.user, calendar_id=self.calendar_id, event=json_event, tag="ASSIGNMENT", org="Best Org"))


class EventAccessView(APIView):
    calendar_id = "primary"

    def get(self, request, event_id, format='JSON', *args, **kwargs):
        return Response(ApiInterface.get_event_from_calendar(user=request.user, calendar_id=self.calendar_id, event_id=event_id))

    def put(self, request, event_id, format='JSON', *args, **kwargs):
        json_event = ApiInterface.create_event_from_dict(request.DATA)
        return Response(ApiInterface.put_event_to_calendar(user=request.user, calendar_id=self.calendar_id, event=json_event, event_id=event_id, tag=request.get("tag"), org=request.get("org")))

    def delete(self, request, event_id, format='JSON', *args, **kwargs):
        return Response(ApiInterface.get_event_from_calendar(user=request.user, calendar_id=self.calendar_id, event_id=event_id))
