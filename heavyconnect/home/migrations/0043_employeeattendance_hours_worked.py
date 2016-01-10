# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_companystatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeattendance',
            name='hours_worked',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
