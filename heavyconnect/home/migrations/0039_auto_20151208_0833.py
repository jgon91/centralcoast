# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_remove_employee_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='language',
            field=models.IntegerField(default=3, choices=[(1, b'pt-br'), (2, b'es'), (3, b'en-us')]),
        ),
    ]
