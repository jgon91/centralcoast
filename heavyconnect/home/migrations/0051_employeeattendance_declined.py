# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0050_employeeattendancechecklist'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeattendance',
            name='declined',
            field=models.BooleanField(default=False),
        ),
    ]
