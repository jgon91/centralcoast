# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0055_auto_20160218_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeattendance',
            name='managerRejected',
            field=models.BooleanField(default=False),
        ),
    ]
