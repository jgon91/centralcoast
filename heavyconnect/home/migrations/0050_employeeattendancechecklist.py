# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_auto_20160124_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAttendanceChecklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=200, blank=True)),
                ('attendance', models.ForeignKey(to='home.EmployeeAttendance')),
                ('question', models.ForeignKey(to='home.Question')),
            ],
        ),
    ]
