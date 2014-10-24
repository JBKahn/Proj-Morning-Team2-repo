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
        # TODO: Signup flow
        if not self.request.user.is_authenticated():
            return redirect('home:home_page')
        return redirect('time_table:home')

    def get_context_data(self, **kwargs):
        context = super(LoggedInView, self).get_context_data(**kwargs)
        return context


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
