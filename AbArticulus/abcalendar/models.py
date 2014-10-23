from django.db import models

class Event(models.Model):
    event = models.CharField(max_length=255)#Google event id goes here
    tag = foreignKey(Tag)
    eventDetail = foreignKey(EventDetail)
    
class EventDetail(models.Model):
    tag = foreignKey(Tag)
    votes = models.foreignKey(Vote) 

class Tag(models.Model):
    event = models.foreignKey(Event)
    
    TAG_CHOICES = (
        ('Test, Test'),
        ('Assignment, Assignment'),
        ('Homework', 'Homework'),
        ('Phase', 'Phase'),
        ('Meeting', 'Meeting'),
        ('Lecture', 'Lecture'),
    )
    tagType = models.CharField(max_length=25, choices=TAG_CHOICES, default='Homework')

class Comment(models.Model):
    event = foreignKey(Event)
    user = models.foreignKey(User)
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    
class Vote(models.Model):
    user = foreginKey(User)
    event = foreignKey(Event)

