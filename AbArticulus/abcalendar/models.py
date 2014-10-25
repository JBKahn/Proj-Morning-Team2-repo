from django.db import models

from constants import TAG_CHOICES, VOTE_CHOICES


class Organization(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('authentication.CustomUser')


class Tag(models.Model):
    tag_type = models.CharField(max_length=25, choices=TAG_CHOICES)
    organization = models.ForeignKey(Organization)
    number = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.number < 0:
            raise ValueError("number must be greater than -1")
        super(Tag, self).save(*args, **kwargs)


class Event(models.Model):
    gevent_id = models.CharField(max_length=255)  # Google event id
    tag = models.ForeignKey(Tag)
    user = models.ForeignKey('authentication.CustomUser')


class Comment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey('authentication.CustomUser')
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    user = models.ForeignKey('authentication.CustomUser')
    event = models.ForeignKey(Event)
    number = models.IntegerField(choices=VOTE_CHOICES)
