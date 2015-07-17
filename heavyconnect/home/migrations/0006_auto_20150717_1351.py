# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20150715_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='implementtask',
            name='machine',
            field=models.ForeignKey(to='home.MachineTask'),
        ),
    ]
