import pytz
from django.db import models
import datetime as dt
from abcalendar.time_table_parser import University_of_Toronto_Timetable, get_lecture_info, time_schedule
from django.core.management.base import BaseCommand
from abcalendar.models import Tag, Organization, Event
from api.interfaces.api_interface import create_event_json, post_event_to_calendar, get_calendars_from_user


class Command(BaseCommand):
    help = 'Adds a course in the timetable database.'

    index = 0
    customUser = CustomUser.objects.create(uoft_email='mitch.data@mail.utoronto.ca')

    def handle(self, *args, **options):

        for (course, course_info) in self.timetable_information():
            # creates each class as an organization object
            class_org = Organization.objects.create(name=course,user=customUser)

            # for each course, create a tag object
            for lecture in course_info:

               # returns course_desc, course_section, course_time, course_loc, course_instructor
                course_sec, course_desc, course_sec, course_time, course_loc, instructor = get_lecture_info(lecture)
                course_title = course + " : " + course_desc

                # creates a tag object for each classes created
                lecture_tags = Tag.classes.create(tag_type='LECTURE', class_section=course_sec)

                # only handles format ex. M1-2
                start_time, end_time = time_schedule(course_time)

                # how to work on start, end day?
                json_create_eve = create_event_json(title=course_title, start=start_time, end=end_time, all_day=False, description=course_desc, location=course_loc)

                cal_info = post_event_to_calendar(user=customUser, calendar_id='primary', event=json_create_eve)

                if cal_info['id'] != '':
                  time_table_event = Event.objects.create(gevent_id=cal_info['id'],tag=lecture_tags,user=customUser)
                else:
                  raise ValueError("Failed to retrieve gevent_id.")


    def convert_date_time(start,end):
      ''' Returns start and end time as datetime format'''
        year='2014'

        local = pytz.timezone("America/Toronto")
        start_time = dt.datetime(year, 7, 7, start, 0)
        end_time = dt.datetime(year, 11, 6, end, 0)
        recur_until = dt.datetime(year, 12, 1, 12, 0)

        #Convert to appropriate timezone setting
        start = local.localize(start_time)
        end = local.localize(end_time)
        recur_until = local.localize(recur_until)

        return start, end


    def timetable_information(self):
      ''' Returns a dictionary containing course offerings in UofT. '''
        return University_of_Toronto_Timetable()
