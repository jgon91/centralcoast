# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20150911_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='manager',
            field=models.ForeignKey(blank=True, to='home.Employee', null=True),
        ),
    ]
