# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_translatedquestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.IntegerField(choices=[(1, b'Before Lunch Break'), (2, b'Post Lunch Pre Start'), (3, b'Post Lunch Start'), (4, b'End of Day Inspection'), (5, b'Default')]),
        ),
    ]
