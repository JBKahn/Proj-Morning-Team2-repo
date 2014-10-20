from django.conf.urls import patterns, url
from authentication.views import AuthComplete, LoginError


urlpatterns = patterns(
    '',
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'^login-error/$', LoginError.as_view()),
)
