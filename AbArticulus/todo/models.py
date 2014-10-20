from django.db import models


class Todo(models.Model):
    item = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
