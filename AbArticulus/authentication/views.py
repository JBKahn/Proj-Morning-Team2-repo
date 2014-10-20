from social_auth.views import complete

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.base import View


class LoggedInView(TemplateView):
    template_name = 'logged_in.html'

    def get_context_data(self, **kwargs):
        context = super(LoggedInView, self).get_context_data(**kwargs)
        return context


class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        return complete(request, backend, *args, **kwargs)


class LoginError(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=401)
