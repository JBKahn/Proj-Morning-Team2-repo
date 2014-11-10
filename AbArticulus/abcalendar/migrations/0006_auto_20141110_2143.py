# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcalendar', '0005_auto_20141109_0638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='calendar',
        ),
        migrations.AddField(
            model_name='googleevent',
            name='calendar',
            field=models.ForeignKey(default=1, to='abcalendar.Calendar'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googleevent',
            name='tag',
            field=models.ForeignKey(default=1, to='abcalendar.Tag'),
            preserve_default=False,
        ),
    ]
