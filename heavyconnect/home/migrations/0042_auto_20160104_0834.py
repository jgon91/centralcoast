# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_auto_20151229_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='last_task',
        ),
        migrations.AddField(
            model_name='task',
            name='attendance',
            field=models.ForeignKey(to='home.EmployeeAttendance', null=True),
        ),
    ]
