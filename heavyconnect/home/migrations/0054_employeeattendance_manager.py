# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0053_employeeattendance_managerapproved'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeattendance',
            name='manager',
            field=models.CharField(default=b'', max_length=5000),
        ),
    ]
