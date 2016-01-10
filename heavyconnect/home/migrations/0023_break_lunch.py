# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20151008_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='break',
            name='lunch',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
