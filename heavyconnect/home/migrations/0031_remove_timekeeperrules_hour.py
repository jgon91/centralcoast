# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_attendancechecklist_confirmationcheck_timekeeperrules'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timekeeperrules',
            name='hour',
        ),
    ]
