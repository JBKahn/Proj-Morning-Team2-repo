# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcalendar', '0003_auto_20141108_0258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='event',
            new_name='gevent',
        ),
    ]
