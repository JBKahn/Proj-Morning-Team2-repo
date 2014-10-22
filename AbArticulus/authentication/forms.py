from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from authentication.models import CustomUser


class UoftEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@mail.utoronto.ca') or validate_email(email) or CustomUser.objects.filter(uoft_email=email).exists():
            raise ValidationError("Email already exists")
        return email
