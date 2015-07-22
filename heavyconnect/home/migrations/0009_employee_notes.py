# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20150721_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='notes',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
