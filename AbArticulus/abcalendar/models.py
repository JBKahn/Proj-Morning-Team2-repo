from django.db import models

from constants.py import TAG_CHOICES, VOTE_CHOICES
from authentication.models import CustomUser


class Event(models.Model):
    gevent_id = models.CharField(max_length=255)#Google event id
    tag = models.foreignKey(Tag)
    user = models.foreignKey(CustomUser)


class Tag(models.Model):
    number = models.integerField(default=1, min_value=0)
    tagType = models.CharField(max_length=25, choices=TAG_CHOICES)
    organization = models.foreignKey(Organization)


class Comment(models.Model):
    event = models.foreignKey(Event)
    user = models.foreignKey(CustomUser)
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    
    
class Vote(models.Model):
    user = models.foreignKey(CustomUser)
    event = models.foreignKey(Event)
    number = models.integerField(choices=VOTE_CHOICES)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    user = models.foreignKey(CustomUser)
    