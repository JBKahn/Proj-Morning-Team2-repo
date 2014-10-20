from django.conf.urls import patterns, url

from todo.views import TodoView, TodoList, TodoDetail


urlpatterns = patterns(
    '',
    url(r'^$', TodoView.as_view(), name='todo_home'),
    url(r'^todos/$', TodoList.as_view(), name="todos_list"),
    url(r'^todos/(?P<pk>[0-9]+)/$', TodoDetail.as_view(), name="todos_update"),
)
