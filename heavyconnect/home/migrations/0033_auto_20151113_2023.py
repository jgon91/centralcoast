# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_timekeeperrules_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='picFile',
            field=models.FileField(null=True, upload_to=b'employee_images'),
        ),
        migrations.AlterField(
            model_name='attendancechecklist',
            name='category',
            field=models.IntegerField(choices=[(1, b'Always'), (2, b'Less lunch than Expected'), (3, b'Less Breaks than Expected'), (4, b'Optional Lunch')]),
        ),
    ]
