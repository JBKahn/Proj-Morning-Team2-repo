from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from abcalendar.models import Tag, Calendar, Event, GoogleEvent
from api.interfaces.api_interface import ApiInterface


class Command(BaseCommand):
    help = 'adds existing calendars from the calendar user to the DB'

    def handle(self, *args, **options):
        if not get_user_model().objects.filter(email=settings.EMAIL_OF_USER_WITH_CALENDARS).exists():
            print "You have yet to authenicate the user with calendars. Authenticate the {} email.".format(settings.EMAIL_OF_USER_WITH_CALENDARS)
            return
        calendar_user = get_user_model().objects.get(email=settings.EMAIL_OF_USER_WITH_CALENDARS)
        calendars = ApiInterface.get_calendars_from_user(user=calendar_user)

        for calendar in calendars.get('items'):
            if u"group.v.calendar.google.com" not in calendar.get('id') and calendar.get('id') != settings.EMAIL_OF_USER_WITH_CALENDARS:
                calendar_object = Calendar.objects.get_or_create(name=calendar.get('summary'), gid=calendar.get('id'))

                events = ApiInterface.get_events_from_calendar(user=calendar_user, calendar_id=calendar.get('id'))
                break
                for event in events:
                    description = event.get('description')
                    tag_object, _ = Tag.objects.get_or_create(**description.get('tag'))
                    google_event_object = GoogleEvent.objects.get_or_create(tag=tag_object, calendar=calendar_object, gid=calendar_object.gid, revision=calendar.get('revision'))
                    for abarticulus_event in description.get('events'):
                        # Event.objects.get_or_create(start=abarticulus_event.get('start'), end=abarticulus_event.get('end'), reccur_until=abarticulus_event.get('reccur_until'), all_day=abarticulus_event.get('all_day'), gid=google_event_object.gid)
                        print abarticulus_event
