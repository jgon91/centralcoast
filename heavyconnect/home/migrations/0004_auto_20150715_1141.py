# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20150714_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='implementchecklist',
            name='employee',
            field=models.ForeignKey(blank=True, to='home.Employee', null=True),
        ),
        migrations.AddField(
            model_name='machinechecklist',
            name='employee',
            field=models.ForeignKey(blank=True, to='home.Employee', null=True),
        ),
    ]
