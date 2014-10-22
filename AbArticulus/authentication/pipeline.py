from social.pipeline.partial import partial
from social.exceptions import InvalidEmail

from django.shortcuts import redirect

from authentication.forms import UoftEmailForm


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.uoft_email:
        return
    elif is_new and not details.get('uoft_email'):
        uoft_email = strategy.request_data().get('uoft_email')
        form = UoftEmailForm({'email': uoft_email})

        if uoft_email and form.is_valid():
            details['uoft_email'] = uoft_email
        else:
            return redirect('authentication:require_email')


@partial
def uoft_email_validation(backend, details, is_new=False, *args, **kwargs):
    if details.get('uoft_email') and is_new:
        data = backend.strategy.request_data()
        if 'verification_code' in data:
            backend.strategy.session_pop('email_validation_address')
            if not backend.strategy.validate_email(details['uoft_email'], data['verification_code']):
                raise InvalidEmail(backend)
        else:
            backend.strategy.send_email_validation(backend, details['uoft_email'])
            backend.strategy.session_set('email_validation_address', details['uoft_email'])
            return backend.strategy.redirect(
                backend.strategy.setting('EMAIL_VALIDATION_URL')
            )
