# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20150904_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='horsepower',
            field=models.IntegerField(null=True),
        ),
    ]
