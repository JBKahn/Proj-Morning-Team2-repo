# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20141105_0326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='organizations',
        ),
    ]
