# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeattendance',
            old_name='break_tome',
            new_name='afternoon_break',
        ),
        migrations.RenameField(
            model_name='employeeattendance',
            old_name='e_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='machinecertification',
            old_name='Machine_id',
            new_name='machine_id',
        ),
        migrations.RenameField(
            model_name='machinequalification',
            old_name='Machine_id',
            new_name='machine_id',
        ),
        migrations.RenameField(
            model_name='machineservice',
            old_name='Machine_id',
            new_name='machine_id',
        ),
        migrations.RenameField(
            model_name='manufacturer',
            old_name='man_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='s_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='appendix',
            name='a_id',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='permission_level',
        ),
        migrations.RemoveField(
            model_name='employeequalifications',
            name='q_level',
        ),
        migrations.RemoveField(
            model_name='task',
            name='t_date',
        ),
        migrations.RemoveField(
            model_name='taskimplementmachine',
            name='Machine_id',
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='afternoon_break_end',
            field=models.TimeField(default=datetime.datetime(2015, 6, 9, 21, 12, 50, 619346, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='evening_break',
            field=models.TimeField(default=datetime.datetime(2015, 6, 9, 21, 12, 55, 927567, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='evening_break_end',
            field=models.TimeField(default=datetime.datetime(2015, 6, 9, 21, 13, 3, 701840, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='morning_break',
            field=models.TimeField(default=datetime.datetime(2015, 6, 9, 21, 13, 11, 638042, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='morning_break_end',
            field=models.TimeField(default=datetime.datetime(2015, 6, 9, 21, 13, 19, 190755, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeetask',
            name='substitution',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 9, 21, 13, 45, 763782, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskimplementmachine',
            name='machine',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskimplementmachine',
            name='machine_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='implement',
            name='serial_number',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='implement',
            name='year_purchased',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='machine',
            name='year_purchased',
            field=models.IntegerField(),
        ),
    ]
