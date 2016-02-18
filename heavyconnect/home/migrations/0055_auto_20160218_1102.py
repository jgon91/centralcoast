# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0054_employeeattendance_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeattendance',
            name='manager',
            field=models.CharField(default=b'', max_length=5000, null=True, blank=True),
        ),
    ]
