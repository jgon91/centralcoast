# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_auto_20151216_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='language',
            field=models.IntegerField(default=3, choices=[(1, b'pt-br'), (2, b'es'), (3, b'en-us')]),
        ),
    ]
