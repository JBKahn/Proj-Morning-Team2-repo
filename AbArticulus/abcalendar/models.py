from django.db import models

from constants import TAG_CHOICES, VOTE_CHOICES


class Calendar(models.Model):
    name = models.CharField(max_length=255, unique=True)  # e.g. `CSC301H1S-L0101`
    gid = models.CharField(max_length=255, unique=True)


class Tag(models.Model):
    calendar = models.ForeignKey(Calendar)
    tag_type = models.CharField(max_length=25, choices=TAG_CHOICES)
    number = models.IntegerField(default=1, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.number < 0:
            raise ValueError("number must be greater than -1")
        super(Tag, self).save(*args, **kwargs)


class GoogleEvent(models.Model):
    gid = models.CharField(max_length=255, unique=True)
    revision = models.IntegerField()


class Event(models.Model):
    tag = models.ForeignKey(Tag)
    gevent = models.ForeignKey(GoogleEvent, related_name='events')
    start = models.DateTimeField()
    end = models.DateTimeField()
    reccur_until = models.DateTimeField(blank=True, null=True)
    all_day = models.BooleanField(default=False)


class Comment(models.Model):
    gevent = models.ForeignKey(GoogleEvent, related_name='comments')
    user = models.ForeignKey('authentication.CustomUser')
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    user = models.ForeignKey('authentication.CustomUser')
    event = models.ForeignKey(Event, related_name='votes')
    number = models.IntegerField(choices=VOTE_CHOICES)
