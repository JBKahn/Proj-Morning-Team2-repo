from django.conf.urls import patterns, url

from time_table.views import TimeTableHomeView


urlpatterns = patterns(
    '',
    url(r'^event/([^/]+)/?$', 'time_table.views.access_event'),
    url(r'^$', TimeTableHomeView.as_view(), name='home')
)
