from django.db import models

class Event(models.Model):
    eventID = models.CharField(max_length=255)#Google event id goes here
    tagID = foreignKey(Tag)
    eventDetail = foreignKey(EventDetail)
    
class EventDetail(models.Model):
    tagID = foreignKey(Tag)
    eventType = foreignKey(Tag, to_field=tagType) #Unsure
    votes = models.foreignKey(Vote) #how does this get all tags associated with User

class Tag(models.Model):
    eventID = models.CharField(max_length=255)
    tagID = models.CharField(max_length=255)
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
    eventID = foreignKey(Event)
    userID = models.foreignKey(User)
    comment = models.CharField(max_length=255) #length too small?
    time = models.DateTimeField(auto_now_add=True)
    
class User(models.Model):
    userID = models.CharField(max_length=255) #this line necessary?
    tags = models.foreignKey(tag) #how does this get all tags associated with User
    
class Vote(models.Model):
    user = foreginKey(User)
    event = foreignKey(Event)