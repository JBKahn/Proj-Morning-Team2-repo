from django.conf.urls import patterns, url

from time_table.views import TimeTableHomeView, EventCreateView, EventAccessView, CalendarListCreateView, VoteCreateView, CommentCreateView


urlpatterns = patterns(
    '',
    url(r'^event/$', EventCreateView.as_view(), name='event_create'),
    url(r'^event/(?P<event_id>\w+)/', EventAccessView.as_view(), name='event_access'),
    url(r'^calendar/$', CalendarListCreateView.as_view(), name='calendar_list_create'),
    url(r'^vote/$', VoteCreateView.as_view(), name='vote_create'),
    url(r'^comment/$', CommentCreateView.as_view(), name='comment_create'),
    url(r'^$', TimeTableHomeView.as_view(), name='home')
)
