# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20150717_1351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='implementtask',
            old_name='machine',
            new_name='machine_task',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'Pending'), (2, b'Approved'), (3, b'Denied'), (4, b'Ongoing'), (5, b'Paused'), (6, b'Finished')]),
        ),
    ]
