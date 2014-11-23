from datetime import timedelta

from mock import patch
from rest_framework.renderers import JSONRenderer

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from abcalendar.models import Vote, Comment, Tag, Event, GoogleEvent, Calendar
from abcalendar.serializers import GoogleEventSerializer
from api.interfaces.api_interface import ApiInterface


class FakeGoogleApiResponse():
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            'id': 123,
            'key': 'value',
        }


class AddNewEventTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', first_name='test', last_name='user')
        self.calendar_user = get_user_model().objects.create(email=settings.EMAIL_OF_USER_WITH_CALENDARS, username='caluser')
        self.event_info = {
            'title': u'test title',
            'start': timezone.localtime(timezone.now()),
            'end': timezone.localtime(timezone.now()) + timedelta(hours=2),
            'all_day': False,
            'description': 1,
            'location': 1,
            'reccur_until': None,
            'sequence': 1
        }
        self.tag_data = {
            'number': 1,
            'tag_type': u'ASSIGNMENT'
        }
        self.original_google_event_count = GoogleEvent.objects.count()
        self.original_event_count = Event.objects.count()
        self.original_tag_count = Tag.objects.count()
        self.original_vote_count = Vote.objects.count()
        self.original_comment_count = Comment.objects.count()

    def test_non_app_event_calls_post_event_to_calendar_no_db_changes(self):
        with patch('api.interfaces.api_interface.ApiInterface.post_event_to_calendar') as post_event_mock:
            post_event_mock.return_value = ''
            ApiInterface.add_user_event(user=self.user, calendar_id=1, event_data=self.event_info, tag_data=self.tag_data)
            self.assertTrue(post_event_mock.called)
            post_event_mock.assert_called_once_with(
                calendar_id=1,
                event_data=ApiInterface.create_event_from_dict(self.event_info),
                user=self.user
            )

        # No events are created
        self.assertEqual(self.original_google_event_count, GoogleEvent.objects.count())
        self.assertEqual(self.original_event_count, Event.objects.count())
        self.assertEqual(self.original_tag_count, Tag.objects.count())
        self.assertEqual(self.original_vote_count, Vote.objects.count())
        self.assertEqual(self.original_comment_count, Comment.objects.count())

    @patch('api.interfaces.api_interface.GoogleApiInterface.post_event_to_calendar')
    def test_app_event_with_new_tag(self, google_post_event_mock):
        calendar = Calendar.objects.create(name='test cal', gid=456)
        google_post_event_mock.return_value = FakeGoogleApiResponse()
        ApiInterface.add_user_event(user=self.user, calendar_id=calendar.gid, event_data=self.event_info, tag_data=self.tag_data)
        self.assertTrue(google_post_event_mock.called)

        event_data = ApiInterface.create_event_from_dict(self.event_info)
        event_data.update({
            'description': JSONRenderer().render(GoogleEventSerializer(GoogleEvent.objects.get(gid=123)).data)
        })

        google_post_event_mock.assert_called_once_with(
            calendar_id=calendar.gid,
            event=event_data,
            user=self.calendar_user
        )

        self.assertEqual(self.original_google_event_count + 1, GoogleEvent.objects.count())
        self.assertEqual(self.original_event_count + 1, Event.objects.count())
        self.assertEqual(self.original_tag_count + 1, Tag.objects.count())
        self.assertEqual(self.original_vote_count + 1, Vote.objects.count())
        self.assertEqual(self.original_comment_count, Comment.objects.count())

    @patch('api.interfaces.api_interface.GoogleApiInterface.post_event_to_calendar')
    @patch('api.interfaces.api_interface.GoogleApiInterface.put_event_to_calendar')
    def test_app_event_with_same_tag_same_user(self, google_put_event_mock, google_post_event_mock):
        calendar = Calendar.objects.create(name='test cal', gid=456)
        google_post_event_mock.return_value = FakeGoogleApiResponse()
        google_put_event_mock.return_value = FakeGoogleApiResponse()
        ApiInterface.add_user_event(user=self.user, calendar_id=calendar.gid, event_data=self.event_info, tag_data=self.tag_data)

        # change end date
        event_info = {}
        event_info.update(self.event_info)
        event_info['end'] = timezone.localtime(timezone.now()) + timedelta(hours=1)

        ApiInterface.add_user_event(user=self.user, calendar_id=calendar.gid, event_data=event_info, tag_data=self.tag_data)
        self.assertTrue(google_post_event_mock.called)

        google_event_info = {
            'end': event_info.get('end'),
            'start': event_info.get('start'),
            'reccur_until': event_info.get('reccur_until'),
            'all_day': event_info.get('all_day'),
            'sequence': 1
        }

        event_data = ApiInterface.create_event_from_dict(google_event_info)
        event_data['description'] = JSONRenderer().render(GoogleEventSerializer(GoogleEvent.objects.get(gid=123)).data)

        google_put_event_mock.assert_called_once_with(
            event_id=u'123',
            calendar_id=calendar.gid,
            event=event_data,
            user=self.calendar_user
        )

        self.assertEqual(self.original_google_event_count + 1, GoogleEvent.objects.count())
        self.assertEqual(self.original_event_count + 2, Event.objects.count())
        self.assertEqual(self.original_tag_count + 1, Tag.objects.count())
        self.assertEqual(self.original_vote_count + 1, Vote.objects.count())
        self.assertEqual(self.original_comment_count, Comment.objects.count())
