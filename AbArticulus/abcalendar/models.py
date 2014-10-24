from django.db import models
from constants.py import TAG_CHOICES
from constants.py import VOTE_CHOICES ##from constants.py import * ??

class Event(models.Model):
    gevent_id = models.CharField(max_length=255)#Google event id
    eventDetail = foreignKey(EventDetail)
    tag = foreignKey(Tag)
    organizer = foreignKey(Organization)

class Tag(models.Model):
    number = intergerFeild(default=1, min_value=0)
    tagType = models.CharField(max_length=25, choices=TAG_CHOICES, default='Homework')

class Comment(models.Model):
    event = foreignKey(Event)
    user = models.foreignKey(User)
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    
class Vote(models.Model):
    user = foreginKey(User)
    event = foreignKey(Event)
    number = intergerFeild(choices=VOTE_CHOICES)

class Organization(models.Model):
    name = models.CharFeild(max_length=255)
    