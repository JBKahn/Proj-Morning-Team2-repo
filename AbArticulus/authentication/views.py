import requests
from social.apps.django_app.views import complete

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.utils.decorators import method_decorator

class LoggedInView(TemplateView):
    template_name = 'logged_in.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoggedInView, self).get_context_data(**kwargs)
	user = self.request.user
	social = user.social_auth.get(provider='google-oauth2')
	response = requests.get(
	    'https://www.googleapis.com/plus/v1/people/me/people/visible',
	    params={'access_token': social.extra_data['access_token']}
	)
	friends = response.json()['items']
	context.update({
	    'friends': friends,
	})
        return context


class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        return complete(request, backend, *args, **kwargs)


class LoginError(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=401)
