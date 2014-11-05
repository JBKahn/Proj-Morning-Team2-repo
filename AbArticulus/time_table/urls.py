from django.conf.urls import patterns, url

from time_table.views import TimeTableHomeView, EventCreateView, EventAccessView


urlpatterns = patterns(
    '',
    url(r'^event(/)?$', EventCreateView.as_view(), name='event_create'),
    url(r'^event/([^/]+)(/)?$', EventAccessView.as_view(), name='event_access'),
    url(r'^$', TimeTableHomeView.as_view(), name='home')
)
