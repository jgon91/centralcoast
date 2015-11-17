# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_employee_photoemployee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='photo',
        ),
    ]
