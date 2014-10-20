from django.conf.urls import patterns, url
from authentication.views import AuthComplete, LoginError, LoggedInView


urlpatterns = patterns(
    '',
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'^logged-in/$', LoggedInView.as_view()),
    url(r'^login-error/$', LoginError.as_view()),
)
