# Define a custom User class to work with django-social-auth
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    uoft_email = models.EmailField(max_length=70, blank=True)

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)
