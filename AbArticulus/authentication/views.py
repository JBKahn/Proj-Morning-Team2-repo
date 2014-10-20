from django.http import HttpResponse
from django.views.generic.base import View
from social_auth.views import complete


class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        return complete(request, backend, *args, **kwargs)


class LoginError(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=401)
