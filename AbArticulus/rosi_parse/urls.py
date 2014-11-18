from django.conf.urls import patterns, url
from rosi_parse.views import RosiParseAPIView

urlpatterns = patterns(
    '',
    url(r'^courses/', RosiParseAPIView.as_view(), name='get_courses'),
)
