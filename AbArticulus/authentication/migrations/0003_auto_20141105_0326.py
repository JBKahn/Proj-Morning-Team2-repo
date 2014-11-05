# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcalendar', '0002_auto_20141105_0326'),
        ('authentication', '0002_customuser_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='tags',
        ),
        migrations.AddField(
            model_name='customuser',
            name='organizations',
            field=models.ManyToManyField(to='abcalendar.Organization'),
            preserve_default=True,
        ),
    ]
