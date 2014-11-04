from django.db import models
from abcalendar.time_table_parser import University_of_Toronto_Timetable, get_lecture_info
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
            classes.save()

            # creates a tag object for each classes created
            lecture_tags = classes.tag_set.create(tag_type='LECTURE')

            # for each course, create a tag object
            for lecture in course_info:

               # returns course_desc, course_section, course_time, course_loc, course_instructor
                course_sec, course_desc, course_sec, course_time, course_loc, instructor = get_lecture_info(lecture)
                course_title = course + " : " + course_desc
                lecture_tags.add_course_info(course_sec)

                # how to work on start, end day?
                json_create_eve = create_event_json(title=course_title, start=start, end=end, all_day=False, description=course_desc, location=course_loc)

                cal_info = post_event_to_calendar(user=customUser, calendar_id='primary', event=json_create_eve)

                # create event object
                time_table_event = Event.objects.create(gevent_id=cal_info['id'],tag=lecture_tags,user=customUser)



    def timetable_information(self):
      ''' Returns a dictionary containing course offerings in UofT. '''
        return University_of_Toronto_Timetable()


# Questions
# 1) How should I retrieve the user. Right now its default to mine.

# Comments
# classes are organization, courses are events, lecture times are tags
