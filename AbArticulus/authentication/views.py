import json
import requests
from dateutil.parser import parse
from social.apps.django_app.views import complete

from django.contrib.auth import logout as auth_logout
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.shortcuts import redirect


class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        return complete(request, backend, *args, **kwargs)


class LoggedInView(TemplateView):
    template_name = 'logged_in.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect('home:home_page')
        return super(LoggedInView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoggedInView, self).get_context_data(**kwargs)
        user = self.request.user
        social = user.social_auth.get(provider='google-oauth2')
        response = requests.get(
            'https://www.googleapis.com/calendar/v3/users/me/calendarList',
            params={'access_token': social.extra_data['access_token']}
        )
        friends = response.json()['items']
        context.update({
            'friends': friends,
        })
        id = friends[1].get('id')
        response = requests.get(url='https://www.googleapis.com/calendar/v3/calendars/{}/events'.format(id),params={'access_token': social.extra_data['access_token']})
        events = []
        for item in response.json().get('items'):
            events.append({
                'end': item.get('end') and item.get('end').get('dateTime'),
                'start': item.get('start') and item.get('start').get('dateTime'),
                'allDay': item.get('end') and item.get('end').get('dateTime') and parse(item.get('end').get('dateTime')) and parse(item.get('end').get('dateTime')).hour == item.get('end') and item.get('end').get('dateTime') and parse(item.get('end').get('dateTime')) and parse(item.get('end').get('dateTime')).minute == 0,
                'title': item.get('summary'),
                'id': item.get('id'),
            })
        return {"events": json.dumps(events)}


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


class RequireEmailView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(RequireEmailView, self).get_context_data(**kwargs)
        backend = self.request.session['partial_pipeline']['backend']
        context.update({
            'email_required': True,
            'backend': backend
        })
        return context


class ValidationCodeSentView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(ValidationCodeSentView, self).get_context_data(**kwargs)
        context.update({
            'validation_sent': True,
            'email': self.request.session.get('email_validation_address')
        })
        return context
