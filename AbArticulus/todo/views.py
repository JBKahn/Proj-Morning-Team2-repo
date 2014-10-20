from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser

from django.views.generic import TemplateView

from todo.models import Todo
from todo.serializers import TodoSerializer


class TodoView(TemplateView):
    template_name = 'todo.html'


class TodoMixin(object):
    queryset = Todo.objects.all().order_by('-id')
    serializer_class = TodoSerializer
    parser_classes = (JSONParser,)


class TodoList(TodoMixin, ListCreateAPIView):
    """Return a list of all the todos, or create new ones."""
    pass


class TodoDetail(TodoMixin, RetrieveUpdateDestroyAPIView):
    """Return a specific todo, update it, or delete it."""
    pass
