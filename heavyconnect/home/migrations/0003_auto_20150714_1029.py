# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_certification_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeattendance',
            name='signature',
            field=models.CharField(max_length=5000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='certification',
            name='year',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
