from django.conf.urls import patterns, url

from time_table.views import TimeTableHomeView


urlpatterns = patterns(
    '',
    url(r'^event/([^/]+)?/?$', EventView.as_view(), name='event'),
    url(r'^$', TimeTableHomeView.as_view(), name='home')
)
