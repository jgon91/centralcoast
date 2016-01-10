# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20151005_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinechecklist',
            name='photo',
            field=models.TextField(max_length=550000, blank=True),
        ),
    ]
