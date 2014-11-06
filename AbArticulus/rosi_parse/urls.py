from django.conf.urls import patterns, url
from rosi_parse.views import RosiParseAPIView, SimpleRosiFormView

urlpatterns = patterns(
    '',
    url(r'^courses/', RosiParseAPIView.as_view(), name='get_courses'),
    url(r'^login/', SimpleRosiFormView.as_view(), name='rosi_login_example')
)
