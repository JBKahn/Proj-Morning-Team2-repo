from django.conf.urls import patterns, url, include
from django.contrib import admin

from home.views import HomeView, TodoList, TodoDetail, AuthComplete, LoginError


urlpatterns = patterns(
    '',
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'^login-error/$', LoginError.as_view()),
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^todos/$', TodoList.as_view(), name="todos_list"),
    url(r'^todos/(?P<pk>[0-9]+)/$', TodoDetail.as_view(), name="todos_update"),
)
