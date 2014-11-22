import re

from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from authentication.models import CustomUser


course_matcher = re.compile(u'^[A-Za-z]{3}[0-9]{3}(H1 S|H1 F|Y1 Y) (LEC|TUT|PRA)-[0-9]{4}$')


class UoftEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@mail.utoronto.ca') or validate_email(email) or CustomUser.objects.filter(uoft_email=email).exists():
            raise ValidationError("Email already exists")
        return email


class UoftCourseForm(forms.Form):
    courses = forms.CharField()

    def clean_courses(self):
        courses = self.cleaned_data['courses'].split(',')
        for course in courses:
            # Expects courses of the form `CSC301H1 S LEC-0101`
            course_match = course_matcher.match(course)
            if not course_match:
                raise ValidationError("course code is not valid")
        return courses
