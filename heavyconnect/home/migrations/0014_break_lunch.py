# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20150817_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='break',
            name='lunch',
            field=models.BooleanField(default=False),
        ),
    ]
