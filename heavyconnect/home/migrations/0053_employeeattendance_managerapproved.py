# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0052_auto_20160126_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeattendance',
            name='managerApproved',
            field=models.BooleanField(default=False),
        ),
    ]
