# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0048_auto_20160118_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.IntegerField(choices=[(1, b'Default'), (2, b'Before Lunch Break'), (3, b'Post Lunch Pre Start'), (4, b'Post Lunch Start'), (5, b'End of Day Inspection'), (6, b'End of shift')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='refers',
            field=models.IntegerField(choices=[(1, b'Machine'), (2, b'Implement'), (3, b'Employee')]),
        ),
    ]
