import pytz
from datetime import datetime, timedelta
from abcalendar.time_table_parser import University_of_Toronto_Timetable, get_lecture_info
from django.core.management.base import BaseCommand
from string import ascii_letters
from abcalendar.models import Tag, Organization, Event
from authentication.models import CustomUser
# from api.interfaces.api_interface import create_event_json, post_event_to_calendar, get_calendars_from_user


class Command(BaseCommand):
    help = 'Adds a course in the timetable database.'

    index = 0
    customUser = CustomUser.objects.create(uoft_email='mitch.data@mail.utoronto.ca')

    def handle(self, *args, **options):
        timetable_info = self.timetable_information()
        for course, course_info in timetable_info.iteritems():
            # creates each class as an organization object
            #class_org = Organization.objects.get_or_create(name=course, user=customUser)

            # for each course, create a tag object
            for lecture in course_info:

                # returns course_desc, course_section, course_time, course_loc, course_instructor
                course_desc, course_sec, course_time, course_loc, instructor = get_lecture_info(lecture)
                # course_title = course + " : " + course_desc

                # creates a tag object for each classes created
                # lecture_tags = Tag.objects.get_or_create(tag_type='LECTURE', class_section=course_sec, number=0)

                lecture_times = self.convert_lecture_time_codes(course_time)

                # Hard coding Y till I figure out where you put it.
                for weekday, start_time, duration in lecture_times:
                    event_start, event_end, recur_until = self.get_reccuring_time_until('Y', weekday, start_time, duration)
                    # how to work on start, end day?
                    # json_create_eve = create_event_json(title=course_title, start=start_time, end=end_time, all_day=False, description=course_desc, location=course_loc)

                    # cal_info = post_event_to_calendar(user=customUser, calendar_id='primary', event=json_create_eve)

                    # if cal_info['id'] != '':
                    #  time_table_event = Event.objects.create(gevent_id=cal_info['id'],tag=lecture_tags,user=customUser)
                    # else:
                    #  raise ValueError("Failed to retrieve gevent_id.")

    def get_reccuring_time_until(self, time_period, day_of_week, hour_start, duration):
        if hour_start < 9:
            hour_start += 12
        local = pytz.timezone("America/Toronto")
        if time_period == "F":
            # A monday
            start_date = datetime(year=2014, month=9, day=8, hour=0, minute=0, second=0)
            end_date = datetime(year=2014, month=12, day=3, hour=0, minute=0, second=0)
        elif time_period == "S":
            # a monday
            start_date = datetime(year=2015, month=1, day=5, hour=0, minute=0, second=0)
            end_date = datetime(year=2015, month=4, day=2, hour=0, minute=0, second=0)
        elif time_period == 'Y':
            start_date = datetime(year=2014, month=9, day=8, hour=0, minute=0, second=0)
            end_date = datetime(year=2015, month=4, day=2, hour=0, minute=0, second=0)

        if day_of_week == 'M':
            day_diff = 0
        elif day_of_week == 'T':
            day_diff = 1
        elif day_of_week == 'W':
            day_diff = 3
        elif day_of_week == 'R':
            day_diff = 4
        elif day_of_week == 'F':
            day_diff = 5

        event_start = local.localize(start_date + timedelta(days=day_diff, hours=hour_start))
        event_end = local.localize(event_start + timedelta(hours=duration))
        until = local.localize(end_date)

        return event_start, event_end, until

    def convert_lecture_time_codes(self, time_code_string):
        backwards_timecode = time_code_string[::-1]
        current_time = ''
        lecture_times = []
        reset_time = False
        for char in backwards_timecode:
            if char not in ascii_letters:
                if reset_time:
                    current_time = ''
                    reset_time = False
                current_time = char + current_time
            else:
                split_times = current_time.split('-')
                if int(split_times[0]) < 9:
                    split_times[0] = int(split_times[0]) + 12
                start = split_times[0]

                if len(split_times) == 1:
                    duration = 1
                else:
                    if int(split_times[1]) < 9:
                        split_times[1] = int(split_times[1]) + 12
                    duration = int(split_times[1]) - int(split_times[0])

                lecture_times.append((char, start, duration))
                reset_time = True
        return lecture_times

    def timetable_information(self):
        ''' Returns a dictionary containing course offerings in UofT. '''
        return University_of_Toronto_Timetable()
