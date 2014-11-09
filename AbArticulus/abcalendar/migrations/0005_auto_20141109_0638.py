# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcalendar', '0004_auto_20141108_0301'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='gid',
            field=models.CharField(default=1, unique=True, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='gevent',
            field=models.ForeignKey(related_name=b'comments', to='abcalendar.GoogleEvent'),
        ),
        migrations.AlterField(
            model_name='event',
            name='gevent',
            field=models.ForeignKey(related_name=b'events', to='abcalendar.GoogleEvent'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='event',
            field=models.ForeignKey(related_name=b'votes', to='abcalendar.Event'),
        ),
    ]
