# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_remove_timekeeperrules_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='timekeeperrules',
            name='hour',
            field=models.TimeField(default=datetime.datetime(2015, 11, 8, 17, 33, 31, 136577)),
            preserve_default=False,
        ),
    ]
