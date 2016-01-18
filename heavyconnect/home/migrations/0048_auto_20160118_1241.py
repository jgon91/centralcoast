# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_auto_20160110_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='permission_level',
            field=models.IntegerField(default=1, choices=[(1, b'Driver'), (2, b'Manager'), (3, b'Shop')]),
        ),
    ]
