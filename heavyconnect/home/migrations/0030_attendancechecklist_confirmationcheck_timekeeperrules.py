# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_auto_20151105_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceChecklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.IntegerField(choices=[(1, b'Always'), (2, b'Less lunch than Expected'), (3, b'Less Breaks than Expected')])),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmationCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.BooleanField()),
                ('note', models.CharField(max_length=200, blank=True)),
                ('attendance', models.ForeignKey(to='home.EmployeeAttendance')),
                ('question', models.ForeignKey(to='home.AttendanceChecklist')),
            ],
        ),
        migrations.CreateModel(
            name='TimeKeeperRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hour', models.FloatField()),
                ('breaks', models.IntegerField()),
                ('lunchs', models.IntegerField()),
                ('lunchBool', models.BooleanField()),
            ],
        ),
    ]
