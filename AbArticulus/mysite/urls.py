from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', include('home.urls', namespace="home")),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^ngtodo/', include('todo.urls', namespace="ngtodo")),
    url(r'^auth/', include('authentication.urls', namespace="authentication")),
    url(r'^timetable/', include('time_table.urls', namespace="time_table")),
    url(r'^api/', include('api.urls', namespace="api")),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rosi_parse/', include('rosi_parse.urls', namespace='rosi')),
)
