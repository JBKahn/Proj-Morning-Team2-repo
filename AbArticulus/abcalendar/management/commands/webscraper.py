import pytz
import re
from datetime import datetime, timedelta
from string import ascii_letters

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from abcalendar.time_table_parser import University_of_Toronto_Timetable
from api.interfaces.api_interface import ApiInterface


class Command(BaseCommand):
    help = 'Adds a course in the timetable database.'

    def handle(self, *args, **options):

        if not get_user_model().objects.filter(email=settings.EMAIL_OF_USER_WITH_CALENDARS).exists():
            print "This command requires you authenticate or login with {}.".format(settings.EMAIL_OF_USER_WITH_CALENDARS)
            return

        calendar_user = get_user_model().objects.get(email=settings.EMAIL_OF_USER_WITH_CALENDARS)
        timetable_info = University_of_Toronto_Timetable()
        for course, course_info in timetable_info.iteritems():
            for lecture in course_info:
                # TODO: unsure if you looked into this, but Michelle: this didn't always work.
                sec_code, course_desc, meeting_sec, course_time, course_loc, instructor = lecture
                course_title = course + " : " + course_desc
                lecture_times = self.convert_lecture_time_codes(course_time)

                course_name = course + " : " + course_desc  # Must be the same format accepted by the frontend
                #
                #
                # DO NOT UNCOMMENT UNTIL THIS IS READY FOR FINAL TESTING AND NOT WITHOUT TALKING TO ME FIRST
                # clander_info = ApiInterface.add_calendar(course_name)


                # TODO: Michelle hook this up to wherever you get it from
                season = 'Y'
                for weekday, start_time, duration in lecture_times:
                    # TODO: Fix am/pm in this function and ensure it works using the print statement
                    event_start, event_end, recur_until = self.get_reccuring_time_until(season, weekday, start_time, duration)
                    print weekday, start_time, duration

                    event_data = {
                        'title': '',  # e.g. `CSC301 Lecture 01`
                        'start': event_start,
                        'end': event_end,
                        'all_day': False,
                        'reccur_until': recur_until
                    }

                    tag_data = {
                        'number': 1,
                        'tag_type': 'LECTURE'
                    }

                    #
                    #
                    #
                    # TODO: Uncomment when ready for testing. DO NOT TEST THIS PART WITHOUT TALKING TO ME FIRST.
                    #
                    #
                    #try:
                    #    ApiInterface.add_user_event(calendar_user, calendar_info.get('id'), event_data, tag_data)
                    #except Exception as e:
                    #    print e
                    #    print "failed to add course: {}".format(course_title)
        return

    def get_reccuring_time_until(self, time_period, day_of_week, hour_start, duration):
        if hour_start < 9:
            hour_start += 12
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

        local = pytz.timezone("America/Toronto")
        event_start = local.localize(start_date + timedelta(days=day_diff, hours=int(hour_start)))
        event_end = local.localize(start_date + timedelta(days=day_diff, hours=int(hour_start) + int(duration)))
        until = local.localize(end_date)

        return event_start, event_end, until

    def convert_lecture_time_codes(self, time_code_string):
        # TODO: Michelle, empty courses can get in.
        if not time_code_string:
            return []
        time_code_string = filter(lambda p: not p.strip().startswith('(Note') and p.strip(), time_code_string.split(','))[0]
        time_code_string = re.sub(r'\([^])]*\)', '', time_code_string).strip().replace('am', '').replace('pm', '')
        backwards_timecode = time_code_string[::-1]
        current_time = ''
        lecture_times = []
        reset_time = False
        # TODO: FIX, this shouldn't get in here.
        if time_code_string == 'Cancel' or len(time_code_string) == 1:
            # TODO: Michelle, cancelled courses can get in.
            return lecture_times
        # TODO: Michelle find a way to fix these. I still
        # want you to add the TBA courses to the list of courses you return just not the times with TBA in them.
        if time_code_string in ['TBA', 'See Details']:
            return lecture_times

        # TODO: Michelle fix The lines with `+ 12` are the original demo am vs pm stuff. Not good eoungh.
        for char in backwards_timecode:
            if char not in ascii_letters:
                if reset_time:
                    current_time = ''
                    reset_time = False
                current_time = char + current_time
            else:
                split_times = current_time.split('-')

                if split_times[0].endswith(':15'):
                    split_times[0] = int(split_times[0][:-3]) + .25
                elif split_times[0].endswith(':30'):
                    split_times[0] = int(split_times[0][:-3]) + .5
                elif split_times[0].endswith(':45'):
                    split_times[0] = int(split_times[0][:-3]) + .75

                if float(split_times[0]) < 9:
                    split_times[0] = float(split_times[0]) + 12
                start = split_times[0]
                if len(split_times) == 1:
                    duration = 1
                else:

                    if split_times[1].endswith(':15'):
                        split_times[1] = int(split_times[1][:-3]) + .25
                    elif split_times[1].endswith(':30'):
                        split_times[1] = int(split_times[1][:-3]) + .5
                    elif split_times[1].endswith(':45'):
                        split_times[1] = int(split_times[1][:-3]) + .75

                    if int(split_times[1]) < 9:
                        split_times[1] = float(split_times[1]) + 12
                    duration = float(split_times[1]) - float(split_times[0])
                lecture_times.append((char, start, duration))
                reset_time = True
        return lecture_times
