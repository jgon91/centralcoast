# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20151113_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='picFile',
        ),
    ]
