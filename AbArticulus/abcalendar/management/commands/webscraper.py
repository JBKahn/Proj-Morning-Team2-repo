import pytz
import re
from datetime import datetime, timedelta
from string import ascii_letters

from django.core.management.base import BaseCommand

from abcalendar.time_table_parser import University_of_Toronto_Timetable, get_lecture_info
from api.interfaces.api_interface import ApiInterface
from authentication.models import CustomUser


class Command(BaseCommand):
    help = 'Adds a course in the timetable database.'

    def handle(self, *args, **options):
        calendar_id = 'primary'
        if CustomUser.objects.filter(is_staff=True).exists():
            user = CustomUser.objects.filter(is_staff=True)[0]
        else:
            print "This command requires a staff account to exist. Please create one and try again"
            return
        timetable_info = self.timetable_information()
        for course, course_info in timetable_info.iteritems():
            # for each course, create a tag object
            for lecture in course_info:

                # returns course_desc, course_section, course_time, course_loc, course_instructor
                # Michelle: this doesn't always work.
                course_desc, course_sec, course_time, course_loc, instructor = get_lecture_info(lecture)
                course_title = course + " : " + course_desc
                lecture_times = self.convert_lecture_time_codes(course_time)

                print lecture
                # Hard coding Y till I figure out where you put it.
                for weekday, start_time, duration in lecture_times:
                    event_start, event_end, recur_until = self.get_reccuring_time_until('Y', weekday, start_time, duration)
                    print weekday, start_time, duration
#                    try:
#                        event = ApiInterface.create_google_json(title=course_title, start=event_start, end=event_end, all_day=False, description=None, location=None, recur_until=recur_until)
#                        ApiInterface.post_event_to_calendar(user=user, calendar_id=calendar_id, event=event, tag="LECTURE", org=course)
#                    except Exception:
#                        print "failed to add course: {}".format(course_title)
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
        # TODO: FIX
        if time_code_string == 'Cancel' or len(time_code_string) == 1:
            #TODO: Michelle, cancelled courses can get in.
            return lecture_times
        if time_code_string in ['TBA', 'See Details']:
            return lecture_times
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

    def timetable_information(self):
        ''' Returns a dictionary containing course offerings in UofT. '''
        return University_of_Toronto_Timetable()
