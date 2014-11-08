# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_remove_customuser_organizations'),
        ('abcalendar', '0002_auto_20141105_0326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GoogleEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gid', models.CharField(unique=True, max_length=255)),
                ('revision', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='organization',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='gevent_id',
        ),
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='organization',
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
        migrations.AddField(
            model_name='event',
            name='all_day',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='end',
            field=models.DateTimeField(default=datetime.date(2014, 11, 8)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='gevent',
            field=models.ForeignKey(default=1, to='abcalendar.GoogleEvent'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='reccur_until',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='start',
            field=models.DateTimeField(default=datetime.date(2014, 11, 8)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='calendar',
            field=models.ForeignKey(default=1, to='abcalendar.Calendar'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(to='abcalendar.GoogleEvent'),
        ),
        migrations.AlterField(
            model_name='event',
            name='tag',
            field=models.ForeignKey(to='abcalendar.Tag'),
        ),
    ]
