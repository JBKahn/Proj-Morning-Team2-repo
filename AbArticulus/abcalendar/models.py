from django.conf import settings
from django.db import models

from constants import TAG_CHOICES, VOTE_CHOICES


class Calendar(models.Model):
    name = models.CharField(max_length=255, unique=True)  # e.g. `CSC301H1S-L0101`
    gid = models.CharField(max_length=255, unique=True)


class Tag(models.Model):
    tag_type = models.CharField(max_length=25, choices=TAG_CHOICES)
    number = models.IntegerField(default=1, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.number < 0:
            raise ValueError("number must be greater than -1")
        super(Tag, self).save(*args, **kwargs)


class GoogleEvent(models.Model):
    tag = models.ForeignKey(Tag)
    calendar = models.ForeignKey(Calendar)
    gid = models.CharField(max_length=255, unique=True)
    revision = models.IntegerField()


class Event(models.Model):
    gevent = models.ForeignKey(GoogleEvent, related_name='events')
    start = models.DateTimeField()
    end = models.DateTimeField()
    reccur_until = models.DateTimeField(blank=True, null=True)
    all_day = models.BooleanField(default=False)


class Comment(models.Model):
    gevent = models.ForeignKey(GoogleEvent, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    event = models.ForeignKey(Event, related_name='votes')
    number = models.IntegerField(choices=VOTE_CHOICES)
