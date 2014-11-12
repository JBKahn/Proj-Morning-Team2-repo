from django.conf.urls import patterns, url
from authentication.views import AuthComplete, LoggedInView, RequireEmailView, ValidationCodeSentView
from home.views import HomeView

urlpatterns = patterns(
    '',
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'^logged-in/$', LoggedInView.as_view()),
    url(r'^login/$', HomeView.as_view()),
    url(r'^logout/$', 'authentication.views.logout'),
    url(r'^email/$', RequireEmailView.as_view(), name='require_email'),
    url(r'^email-sent/', ValidationCodeSentView.as_view()),
)
