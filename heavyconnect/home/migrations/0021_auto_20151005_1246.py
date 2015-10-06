# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20150918_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='implementchecklist',
            name='photo',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='machinechecklist',
            name='photo',
            field=models.TextField(blank=True),
        ),
    ]
