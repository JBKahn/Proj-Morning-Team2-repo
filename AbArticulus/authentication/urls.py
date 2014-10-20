from django.conf.urls import patterns, url, include
from authentication.views import AuthComplete, LoginError


urlpatterns = patterns(
    '',
    url(r'', include('social_auth.urls')),
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'^login-error/$', LoginError.as_view()),
)
