# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_break_lunch'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='teamManager',
            field=models.BooleanField(default=False),
        ),
    ]
