# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20151025_1508'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GrupParticipant',
            new_name='GroupParticipant',
        ),
    ]
