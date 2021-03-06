from datetime import datetime

from rest_framework import status
from rest_framework.renderers import JSONRenderer

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone

from abcalendar.models import Tag, Calendar, Event, GoogleEvent, Vote, Comment
from abcalendar.serializers import GoogleEventSerializer, EventSerializer, VoteSerializer, TagSerializer
from api.interfaces.google_api_interface import GoogleApiInterface
from api.interfaces.helpers import json_to_dict


class ApiInterface(object):
    @classmethod
    def add_calendar(cls, title):
        calendar_user = get_user_model().objects.get(email=settings.EMAIL_OF_USER_WITH_CALENDARS)
        data = {
            'summary': title
        }
        response = GoogleApiInterface.add_calendar(calendar_user=calendar_user, data=data)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        return response.json()

    @classmethod
    def get_calendars_from_user(cls, user):
        response = GoogleApiInterface.get_calendars_from_user(user)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        return response.json()

    @classmethod
    def user_add_calendars(cls, user, titles):
        return [cls.user_add_calendar(user, title) for title in titles]

    @classmethod
    def user_add_calendar(cls, user, title):
        calendar_user = get_user_model().objects.get(email=settings.EMAIL_OF_USER_WITH_CALENDARS)
        calendars = cls.get_calendars_from_user(calendar_user)
        calendar = None
        for item in calendars.get('items'):
            if item.get('summary') == title:
                calendar = item
        if not calendar:
            calendar = cls.add_calendar(title)
        Calendar.objects.get_or_create(gid=calendar.get('id'), name=title)
        cls.share_calendar_with_user(user, calendar.get('id'))
        return calendar

    @classmethod
    def get_events_from_calendar(cls, user, calendar_id):
        response = GoogleApiInterface.get_events_from_calendar(user, calendar_id)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.json())
        formated_events = []
        for item in response.json().get('items'):
            if item.get('status') != u'cancelled':
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
            raise UnexpectedResponseError(response.json())
        event = json_to_dict(response.json())
        return event

    @classmethod
    def share_calendar_with_user(cls, user, calendar_id):
        '''event is a JSON request body, can be populated via create_event_json()'''
        data = {
            'scope': {
                'type': 'user',
                'value': user.email,
            },
            'role': 'reader'
        }

        calendar_user = get_user_model().objects.get(email=settings.EMAIL_OF_USER_WITH_CALENDARS)
        response = GoogleApiInterface.share_calendar(calendar_user, calendar_id, data)
        if response.status_code != status.HTTP_200_OK:
            raise UnexpectedResponseError(response.status_code)
        return json_to_dict(response.json())

    @classmethod
    def user_update_event(cls, user, calendar_id, gevent_id, event_data, revision):
        if Calendar.objects.filter(gid=calendar_id).exists():
            raise ValueError("You cannot update an event which belongs to the app user")
        return cls.put_event_to_calendar(
            user=user,
            calendar_id=calendar_id,
            gevent_id=gevent_id,
            event_data=event_data,
            revision=revision
        )

    @classmethod
    def add_comment_to_event(cls, user, calendar_id, tag_data, comment_data):
        if not Calendar.objects.filter(gid=calendar_id).exists():
            raise ValueError("You cannot vote for a non app event")
        calendar_object = Calendar.objects.get(gid=calendar_id)
        if not Tag.objects.filter(**tag_data).exists():
            raise ValueError("You cannot vote for a non existant event")
        tag_object = Tag.objects.get(**tag_data)

        if not GoogleEvent.objects.filter(tag=tag_object, calendar=calendar_object).exists():
            raise ValueError("The event you're trying to vote on does not exist")

        gevent = GoogleEvent.objects.get(tag=tag_object, calendar=calendar_object)
        if len(comment_data.get('comment')) < 1:
            raise ValueError("The comment length must be greater than 0")

        Comment.objects.create(gevent=gevent, user=user, comment=comment_data.get('comment'))

        events = gevent.events.annotate(num_votes=Sum('votes__number'))
        most_upvoted_event = max(events, key=lambda e: e.num_votes)
        vote_count = most_upvoted_event.num_votes

        if vote_count >= -1:
            gevent.revision = gevent.revision + 1
            gevent.save()

            event_data = {
                'start': timezone.localtime(most_upvoted_event.start),
                'end': timezone.localtime(most_upvoted_event.end),
                'recur_until': (most_upvoted_event.reccur_until and timezone.localtime(most_upvoted_event.reccur_until)) or most_upvoted_event.reccur_until,
                'description': JSONRenderer().render(GoogleEventSerializer(gevent).data)
            }
            event_data['title'] = '{}: {} {}'.format(calendar_object.name, tag_object.tag_type.capitalize(), tag_object.number)
            event_data = cls.create_event_from_dict(event_data)
            event_data['sequence'] = gevent.revision
            calendar_user = get_user_model().objects.get(email=settings.EMAIL_OF_USER_WITH_CALENDARS)
            # TODO: remove. for testing only as we won't share the primary calendar
            if calendar_id == settings.EMAIL_OF_USER_WITH_CALENDARS:
                calendar_id = 'primary'
            response = GoogleApiInterface.put_event_to_calendar(user=calendar_user, calendar_id=calendar_id, event_id=gevent.gid, event=event_data)
            if response.status_code == status.HTTP_200_OK:
                newEventData = json_to_dict(response.json())
                newEventData['existing'] = True
                return newEventData
            else:
                gevent.revision = gevent.revision - 1
                gevent.save()
        else:
            return cls.delete_event_from_calendar(user=user, calendar_id=calendar_id, event_id=gevent.gid)

    @classmethod
    def vote_for_user_event(cls, user, calendar_id, event_data, tag_data, vote_data):
        if not Calendar.objects.filter(gid=calendar_id).exists():
            raise ValueError("You cannot vote for a non app event")
        calendar_object = Calendar.objects.get(gid=calendar_id)
        if not Tag.objects.filter(**tag_data).exists():
            raise ValueError("You cannot vote for a non existant event")
        tag_object = Tag.objects.get(**tag_data)
        event_object_data = {
            'start': event_data.get('start'),
            'end': event_data.get('end'),
            'all_day': event_data.get('all_day'),
            'reccur_until': event_data.get('reccur_until'),
        }

        if not GoogleEvent.objects.filter(tag=tag_object, calendar=calendar_object).exists():
            raise ValueError("The event you're trying to vote on does not exist")

        gevent = GoogleEvent.objects.get(tag=tag_object, calendar=calendar_object)

        if not gevent.events.filter(**event_object_data).exists():
            raise ValueError("The event you're voting for does not have this alternative")
        event_object = gevent.events.get(**event_object_data)

        vote = vote_data.get('vote')
        if vote == 1:
            Vote.objects.filter(user=user, event__pk__in=gevent.events.values_list('pk', flat=True), number=1).delete()
            Vote.objects.filter(user=user, event=event_object).delete()
            Vote.objects.create(user=user, event=event_object, number=vote)
        elif vote == -1:
            Vote.objects.filter(user=user, event=event_object).delete()
            Vote.objects.create(user=user, event=event_object, number=vote)
        elif vote == 0:
            Vote.objects.filter(user=user, event=event_object).delete()
        else:
            raise ValueError("This is not a valid vote, must be 1, -1 or 0")

        events = gevent.events.annotate(num_votes=Sum('votes__number'))
        most_upvoted_event = max(events, key=lambda e: e.num_votes)
        vote_count = most_upvoted_event.num_votes

        if vote_count >= -1:
            gevent.revision = gevent.revision + 1
            gevent.save()

            event_data = {
                'start': timezone.localtime(most_upvoted_event.start),
                'end': timezone.localtime(most_upvoted_event.end),
                'recur_until': (most_upvoted_event.reccur_until and timezone.localtime(most_upvoted_event.reccur_until)) or most_upvoted_event.reccur_until,
                'description': JSONRenderer().render(GoogleEventSerializer(gevent).data)
            }
            event_data['title'] = '{}: {} {}'.format(calendar_object.name, tag_object.tag_type.capitalize(), tag_object.number)
            event_data = cls.create_event_from_dict(event_data)
            event_data['sequence'] = gevent.revision
            calendar_user = get_user_model().objects.get(email=settings.EMAIL_OF_USER_WITH_CALENDARS)
            # TODO: remove. for testing only as we won't share the primary calendar
            if calendar_id == settings.EMAIL_OF_USER_WITH_CALENDARS:
                calendar_id = 'primary'
            response = GoogleApiInterface.put_event_to_calendar(user=calendar_user, calendar_id=calendar_id, event_id=gevent.gid, event=event_data)
            if response.status_code == status.HTTP_200_OK:
                newEventData = json_to_dict(response.json())
                newEventData['existing'] = True
                return newEventData
            else:
                gevent.revision = gevent.revision - 1
                gevent.save()
        else:
            return cls.delete_event_from_calendar(user=user, calendar_id=calendar_id, event_id=gevent.gid)

    @classmethod
    def add_user_event(cls, user, calendar_id, event_data, tag_data):
        # If the calendar isn't one of ours, we don't care about this.
        if Calendar.objects.filter(gid=calendar_id).exists():
            calendar_object = Calendar.objects.get(gid=calendar_id)
            tag_object, _ = Tag.objects.get_or_create(**tag_data)

            # TODO: Should the title be combination of the tag info?
            event_object_data = {
                'start': event_data.get('start'),
                'end': event_data.get('end'),
                'all_day': event_data.get('all_day'),
                'reccur_until': event_data.get('reccur_until'),
            }

            if GoogleEvent.objects.filter(tag=tag_object, calendar=calendar_object).exists():
                gevent = GoogleEvent.objects.get(tag=tag_object, calendar=calendar_object)
                if gevent.events.filter(**event_object_data).exists():
                    event_object = gevent.events.get(**event_object_data)
                else:
                    event_object = Event(**event_object_data)
            else:
                gevent = None
                event_object = Event(**event_object_data)

            vote_object = None
            if not Vote.objects.filter(user=user, event=event_object).exists():
                vote_object = Vote(user=user, event=event_object, number=1)
            else:
                vote_object = Vote.objects.get(user=user, event=event_object)

            if gevent is None:
                gevent = GoogleEvent(revision=0, tag=tag_object, calendar=calendar_object)
                description = GoogleEventSerializer(gevent).data
                description['events'].append(EventSerializer(event_object).data)
                description['events'][0]['votes'].append(VoteSerializer(vote_object).data)
                description['tag'] = TagSerializer(tag_object).data
                event_data['title'] = '{}: {} {}'.format(calendar_object.name, tag_object.tag_type.capitalize(), tag_object.number)
                event_data = cls.create_event_from_dict(event_data)
                event_data['description'] = JSONRenderer().render(description)
                calendar_user = get_user_model().objects.get(email=settings.EMAIL_OF_USER_WITH_CALENDARS)

                response = GoogleApiInterface.post_event_to_calendar(user=calendar_user, calendar_id=calendar_id, event=event_data)

                if response.status_code == status.HTTP_200_OK:
                    gid = response.json().get('id')
                    gevent.gid = gid
                    gevent.save()
                    event_object.gevent = gevent
                    event_object.save()
                    vote_object.event_id = event_object.id
                    vote_object.save()
                    newEventData = json_to_dict(response.json())
                    newEventData['existing'] = False
                    return newEventData
            else:
                event_object.gevent = gevent
                event_object.save()
                for potentual_voted_on_event in gevent.events.all():
                    if potentual_voted_on_event.id == event_object.id:
                        continue
                    Vote.objects.filter(user=user, event=potentual_voted_on_event).delete()
                vote_object.event_id = event_object.id
                vote_object.save()
                events = gevent.events.annotate(num_votes=Sum('votes__number'))
                most_upvoted_event = max(events, key=lambda e: e.num_votes)
                vote_count = most_upvoted_event.num_votes
                if vote_count >= -1:
                    gevent.revision = gevent.revision + 1
                    gevent.save()

                    event_data = {
                        'start': timezone.localtime(most_upvoted_event.start),
                        'end': timezone.localtime(most_upvoted_event.end),
                        'recur_until': (most_upvoted_event.reccur_until and timezone.localtime(most_upvoted_event.reccur_until)) or most_upvoted_event.reccur_until,
                        'description': JSONRenderer().render(GoogleEventSerializer(gevent).data)
                    }
                    event_data['title'] = '{}: {} {}'.format(calendar_object.name, tag_object.tag_type.capitalize(), tag_object.number)
                    event_data = cls.create_event_from_dict(event_data)
                    event_data['sequence'] = gevent.revision
                    calendar_user = get_user_model().objects.get(email=settings.EMAIL_OF_USER_WITH_CALENDARS)
                    # TODO: remove. for testing only as we won't share the primary calendar
                    if calendar_id == settings.EMAIL_OF_USER_WITH_CALENDARS:
                        calendar_id = 'primary'
                    response = GoogleApiInterface.put_event_to_calendar(user=calendar_user, calendar_id=calendar_id, event_id=gevent.gid, event=event_data)
                    if response.status_code == status.HTTP_200_OK:
                        newEventData = json_to_dict(response.json())
                        newEventData['existing'] = True
                        return newEventData
                    else:
                        gevent.revision = gevent.revision - 1
                        gevent.save()
                else:
                    return cls.delete_event_from_calendar(user=user, calendar_id=calendar_id, event_id=gevent.gid)
            raise UnexpectedResponseError('Could not add event')
        else:
            event_data = cls.create_event_from_dict(event_data)
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
            },
            'end': {
                time_key: end.strftime(time_format),
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
