from datetime import datetime

from rest_framework import status

from django.db.models import Sum

from abcalendar.models import Tag, Calendar, Event, GoogleEvent, Vote
from abcalendar.serializers import GoogleEventSerializer, EventSerializer, VoteSerializer
from api.interfaces.google_api_interface import GoogleApiInterface
from api.interfaces.helpers import json_to_dict


class ApiInterface(object):
    @classmethod
    def get_calendars_from_user(cls, user):
        response = GoogleApiInterface.get_calendars_from_user(user)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        return response.json()

    @classmethod
    def get_events_from_calendar(cls, user, calendar_id):
        response = GoogleApiInterface.get_events_from_calendar(user, calendar_id)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        formated_events = []
        for item in response.json().get('items'):
            formated_events.append(json_to_dict(item))
        return formated_events

    @classmethod
    def get_event_from_calendar(cls, user, calendar_id, event_id):
        response = GoogleApiInterface.get_event_from_calendar(user, calendar_id, event_id)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        event = json_to_dict(response.json())
        return event

    @classmethod
    def delete_event_from_calendar(cls, user, calendar_id, event_id):
        response = GoogleApiInterface.delete_event_from_calendar(user, calendar_id, event_id)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            raise UnexpectedResponseError(response.status_code)

    @classmethod
    def post_event_to_calendar(cls, user, calendar_id, event_data):
        '''event is a JSON request body, can be populated via create_event_json()'''
        response = GoogleApiInterface.post_event_to_calendar(user, calendar_id, event_data)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        # we save the Google Event with the google id. Then we save the other models.
        event = json_to_dict(response.json())
        return event

    @classmethod
    def put_event_to_calendar(cls, user, calendar_id, gevent_id, event_data, revision):
        '''event is a JSON request body, can be populated via create_event_json()'''
        event_data['sequence'] = revision
        response = GoogleApiInterface.put_event_to_calendar(user, calendar_id, gevent_id, event_data)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        event = json_to_dict(response.json())
        return event

    @classmethod
    def add_user_event(cls, user, calendar_id, event_data, tag_data):
        # If the calendar isn't one of ours, we don't care about this.
        if Calendar.objects.filter(gid=calendar_id).exists():
            calendar_object = Calendar.objects.get(gid=calendar_id)
            tag_object, _ = Tag.objects.get_or_create(calendar=calendar_object, **tag_data)

            if Event.objects.filter(tag=tag_object, **event_data).exists():
                event_object = Event.objects.get(tag=tag_object, **event_data)
                gevent = event_object.gevent
            else:
                event_object = Event(tag=tag_object, **event_data)
                gevent = None

            vote_object = None
            if not Vote.objects.filter(user=user, event=event_object).exists():
                vote_object = Vote(user=user, event=event_object)

            if gevent is None:
                gevent = GoogleEvent(revision=0)
                description = GoogleEventSerializer(gevent).data
                description['events'].append(EventSerializer(event_object).data)
                description['events'][0]['votes'].append(VoteSerializer(vote_object).data)
                response = cls.post_event_to_calendar(user=user, calendar_id=calendar_id, event_data=event_data)
                if response.status_code == status.HTTP_200_OK:
                    gid = response.json().get('id')
                    gevent.gid = gid
                    gevent.save()
                    event_object.gevent = gevent
                    event_object.save()
                    vote_object.save()
                    return response
            else:
                event_object.save()
                vote_object.save()
                events = gevent.event_set.all().selected_related('vote').annotate(num_votes=Sum('vote__number'))
                most_upvoted_event = max(events, key=lambda e: e.num_votes)
                vote_count = most_upvoted_event.num_votes
                if vote_count >= 0:
                    event_data = {
                        'start': most_upvoted_event.start,
                        'end': most_upvoted_event.end,
                        'recur_until': most_upvoted_event.reccur_until,
                        'description': GoogleEventSerializer(gevent)
                    }
                    response = cls.put_event_to_calendar(user=user, calendar_id=calendar_id, gevent_id=gevent.gid, event_data=event_data, revision=gevent.revision + 1)
                    if response.status_code == status.HTTP_200_OK:
                        gevent.revision = gevent.revision + 1
                        gevent.save()
                        return response
                else:
                    return cls.delete_event_from_calendar(user=user, calendar_id=calendar_id, event_id=gevent.gid)
            raise UnexpectedResponseError('Could not add event')
        else:
            return cls.post_event_to_calendar(user=user, calendar_id=calendar_id, event_data=event_data)

    @classmethod
    def create_google_json(cls, title, start, end, all_day=False, description=None, location=None, recur_until=None, sequence=None):
        '''creates JSON formatted event data to send to Google to create a Google Calendar event times should be datetime objects'''
        if not (isinstance(start, datetime) and isinstance(end, datetime)):
            raise ValueError("Times must be instances of datetime.datetime")

        if all_day:
            time_format = "%Y-%m-%d"
            time_key = 'date'
        else:
            time_format = "%Y-%m-%dT%H:%M:%S%z"
            time_key = 'dateTime'

        body = {
            'summary': title,
            'start': {
                time_key: start.strftime(time_format),
                'timeZone': str(start.tzinfo)
            },
            'end': {
                time_key: end.strftime(time_format),
                'timeZone': str(start.tzinfo)
            },
        }

        if sequence is not None:
            body['sequence'] = sequence

        if recur_until is not None:
            if not isinstance(recur_until, datetime):
                raise ValueError("Times must be instances of datetime.datetime")
            if start.tzinfo is None:
                raise ValueError("datetimes need tzinfo (timezones) defined for recurring events")
            body["recurrence"] = ["RRULE:FREQ=WEEKLY;UNTIL={}".format(recur_until.strftime("%Y%m%dT%H%M%SZ"))]
        if description is not None:
            body['description'] = description
        if location is not None:
            body['location'] = location
        return body

    @classmethod
    def create_event_from_dict(cls, info):
        return ApiInterface.create_google_json(
            title=info.get('title'),
            start=info.get('start'),
            end=info.get('end'),
            all_day=info.get('all_day'),
            description=info.get('description'),
            location=info.get('location'),
            recur_until=info.get('recur_until'),
            sequence=info.get('sequence')
        )


class UnexpectedResponseError(Exception):
    pass
