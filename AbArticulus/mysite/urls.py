from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', include('home.urls', namespace="home")),
    url(r'^ngtodo/', include('todo.urls', namespace="ngtodo")),
    url(r'^auth/', include('authentication.urls', namespace="auth")),
    url(r'^admin/', include(admin.site.urls)),
)
