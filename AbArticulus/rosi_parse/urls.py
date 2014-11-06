from django.conf.urls import patterns, url 
from rosi_parse.views import RosiParseAPIView

urlpatterns = patterns(
    '',
    url(r'^input/', 'rosi_parse.views.input')

) 
