from django.views.generic import TemplateView
from abcalendar.models import Event, Tag
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from api.interfaces.api_interface import ApiInterface
from rest_framework.response import Response

class TimeTableHomeView(TemplateView):
    template_name = 'time_table_home.html'



def access_event(request, event_id):
    """Manipulates Events"""
    if request.method == 'POST':
        tag = request.POST.get('tag')
        if tag is not None:
            tag = Tag.objects.get(tag_type=tag.get("name"), organization=tag.get("organization"))

        #temporary, until we support more calendars
        calendar_id = "primary"
        json_event = ApiInterface.create_event_from_request(request)
        
        if event_id is None or trim(event_id) == "":
            event = ApiInterface.post_event_to_calendar(user=request.user, calendar_id=calendar_id, event=json_event)
        else:
            event = ApiInterface.put_event_to_calendar(user=request.user, calendar_id=calendar_id, event=json_event, event_id=event_id)
        time_table_event = Event.objects.create(gevent_id=event['id'], tag=tag, user=request.user)
    if request.method == 'DELETE':
        ApiInterface.delete_event_from_calendar(user=request.user, calendar_id=calendar_id, event_id=event_id)
        time_table_event = Event.objects.delete(gevent_id=event_id)
    return redirect('time_table:home')
