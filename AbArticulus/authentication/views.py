from social.apps.django_app.views import complete

from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView, TemplateView, View
from django.shortcuts import redirect


class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        return complete(request, backend, *args, **kwargs)


class LoggedInView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return reverse('home:home_page')
        # TODO: Signup flow
        return reverse('time_table:home')


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
