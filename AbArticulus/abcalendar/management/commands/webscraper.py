from django.db import models
from abcalendar.time_table_parser import University_of_Toronto_Timetable, get_lecture_info
from django.core.management.base import BaseCommand
from abcalendar.models import Tag, Organization, Event


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
            for (lec in course_info):
                lecture_tags.add_course_info(lec_section)

                # Returns information on course schedule (i.e title, time)
                course_title, time, location, instructor = get_lecture_info(lec)

                # Retrieves gevent_id that will be used to create Event objects
                google_event_id = retrieve_gevent_id()
                course_events = Event.objects.create(gevent_id=google_event_id,tag=lecture_tags,user=customUser)


    def timetable_information(self):
      ''' Returns a dictionary containing course offerings in UofT. '''
        return University_of_Toronto_Timetable()




# Questions
# 1) How should I retrieve the user. Right now its default to mine.
# 2) For tag number, should it differ for every course created? I'm unsure how this works.

# Comments
# classes are organization, courses are events, lecture times are tags
