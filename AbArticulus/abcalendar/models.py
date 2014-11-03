from django.db import models

from constants import TAG_CHOICES, VOTE_CHOICES


class Organization(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('authentication.CustomUser')


class Tag(models.Model):
    tag_type = models.CharField(max_length=25, choices=TAG_CHOICES)
    organization = models.ForeignKey(Organization)
    number = models.IntegerField(default=1)
    class_section = models.CharField(max_length=25)

    def save(self, *args, **kwargs):
        if self.number < 0:
            raise ValueError("number must be greater than -1")
        super(Tag, self).save(*args, **kwargs)

    def add_course_info(self, section_code):
        ''' Adds course section information to the Tag object. '''
        if self.tag_type == 'LECTURE':
            self.class_section = section_code



class Event(models.Model):
    gevent_id = models.CharField(max_length=255)  # Google event id
    tag = models.ForeignKey(Tag)
    user = models.ForeignKey('authentication.CustomUser')

    def add_event_info(self,tag):

      if tag.tag_type == 'LECTURE':

    # if tag_choices=lecture, need to add lecture info
    # (i.e SC, title, section, time, loc, instructor)


class Comment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey('authentication.CustomUser')
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    user = models.ForeignKey('authentication.CustomUser')
    event = models.ForeignKey(Event)
    number = models.IntegerField(choices=VOTE_CHOICES)
