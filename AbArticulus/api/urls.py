from django.conf.urls import patterns, url

from api.views import EventAPIView


urlpatterns = patterns(
    '',
    url(r'^events/$', EventAPIView.as_view(), name="events"),
)
