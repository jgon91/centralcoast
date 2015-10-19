# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20150715_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='TaskImplementMachine',
            new_name='ImplementTask',
        ),
        migrations.RenameField(
            model_name='employeetask',
            old_name='task_init',
            new_name='end_time',
        ),
        migrations.RemoveField(
            model_name='employeetask',
            name='substitution',
        ),
        migrations.RemoveField(
            model_name='task',
            name='accomplished',
        ),
        migrations.RemoveField(
            model_name='task',
            name='approval',
        ),
        migrations.RemoveField(
            model_name='task',
            name='date',
        ),
        migrations.AddField(
            model_name='employeetask',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='date_assigned',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='pause_end',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='pause_start',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='pause_total',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'Setup'), (2, b'Pending'), (3, b'Approved'), (4, b'Denied'), (5, b'Ongoing'), (6, b'Paused'), (7, b'Finished')]),
        ),
        migrations.AddField(
            model_name='task',
            name='task_end',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='task_init',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='machinetask',
            name='employee_task',
            field=models.ForeignKey(to='home.EmployeeTask'),
        ),
        migrations.AddField(
            model_name='machinetask',
            name='machine',
            field=models.ForeignKey(to='home.Machine'),
        ),
        migrations.AddField(
            model_name='machinetask',
            name='task',
            field=models.ForeignKey(to='home.Task'),
        ),
    ]
