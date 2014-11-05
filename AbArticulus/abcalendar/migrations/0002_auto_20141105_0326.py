# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcalendar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tag',
            field=models.ForeignKey(default=None, to='abcalendar.Tag'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='tag',
            name='number',
            field=models.IntegerField(default=1, null=True, blank=True),
        ),
    ]
