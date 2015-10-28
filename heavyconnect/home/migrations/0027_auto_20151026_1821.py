# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20151025_1514'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='data',
            new_name='date',
        ),
    ]
