from django.conf.urls import patterns, url
from rosi_parse.views import RosiParseAPIView

urlpatterns = patterns(
    '',
    url(r'^courses/', RosiParseAPIView.asView(), name='get_courses')
)
