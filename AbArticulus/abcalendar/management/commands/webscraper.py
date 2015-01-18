from django.core.management.base import BaseCommand
from abcalendar.time_table_parser import *
from abcalendar.models import Tag, Organization, Event


class Command(BaseCommand):
    help = 'Adds courses in the timetable'
    index = 0

    def handle(self, *args, **options):

        for (course, course_info) in self.timetable_information():
            # classes are organization, courses are events, lecture times are tags
            classes = Organization.objects.create(name=course)
            classes.save()
            lecture_tags = classes.tag_set.create(tag_type='LECTURE',index)
            index+=1

            for (lec in course_info):
              # How to get gevent_id and user information?
              lecture_info = Event.objects.create(gevent_id='',tag=lecture_tags,user='')
              # this will create an event for each lecture schedule offered for a course
              # lecture_info.add_info(lect)


    def timetable_information(self):
      ''' Returns a dictionary containing course offerings in UofT. '''
        return University_of_Toronto_Timetable()
