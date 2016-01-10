# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20151027_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='break',
            name='edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
