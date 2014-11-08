# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcalendar', '0003_auto_20141108_0258'),
        ('authentication', '0004_remove_customuser_organizations'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='calendars',
            field=models.ManyToManyField(to='abcalendar.Calendar'),
            preserve_default=True,
        ),
    ]
