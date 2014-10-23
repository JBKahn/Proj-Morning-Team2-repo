from django.db import models
from constants.py import TAG_CHOICES 

class Event(models.Model):
    gevent_id = models.CharField(max_length=255)#Google event id
    eventDetail = foreignKey(EventDetail)
    
class EventDetail(models.Model):
    tag = foreignKey(Tag)
    votes = models.foreignKey(Vote)
    comment = models.foreignKey(Comment)

class Tag(models.Model):
    event = models.foreignKey(Event)
    number = intergerFeild
    tagType = models.CharField(max_length=25, choices=TAG_CHOICES, default='Homework')

class Comment(models.Model):
    event = foreignKey(Event)
    user = models.foreignKey(User)
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    
class Vote(models.Model):
    user = foreginKey(User)
    event = foreignKey(Event)

class Orginization(models.Model):
    name = models.CharFeild(max_length=255)
    