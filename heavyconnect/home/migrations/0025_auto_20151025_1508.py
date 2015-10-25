# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_employee_teammanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, blank=True)),
                ('data', models.DateField()),
                ('permanent', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='GrupParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(to='home.Group')),
                ('participant', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='group',
            field=models.ForeignKey(blank=True, to='home.Group', null=True),
        ),
    ]
