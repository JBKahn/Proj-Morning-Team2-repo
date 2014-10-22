from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class UoftEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@mail.utoronto.ca') and not validate_email(email):
            raise ValidationError("Email already exists")
        return email
