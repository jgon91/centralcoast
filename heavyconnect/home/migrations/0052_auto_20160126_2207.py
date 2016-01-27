# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0051_employeeattendance_declined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancechecklist',
            name='description',
            field=models.CharField(max_length=2000),
        ),
    ]
