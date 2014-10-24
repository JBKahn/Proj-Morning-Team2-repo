from django.db import models

from constants.py import TAG_CHOICES, VOTE_CHOICES
from authentication.models import CustomUser


class Event(models.Model):
    gevent_id = models.CharField(max_length=255)#Google event id
    tag = models.ForeignKey(Tag)
    user = models.ForeignKey(CustomUser)


class Tag(models.Model):
    number = models.IntegerField(default=1, min_value=0)
    tag_type = models.CharField(max_length=25, choices=TAG_CHOICES)
    organization = models.ForeignKey(Organization)


class Comment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(CustomUser)
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    
    
class Vote(models.Model):
    user = models.ForeignKey(CustomUser)
    event = models.ForeignKey(Event)
    number = models.IntegerField(choices=VOTE_CHOICES)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser)
    