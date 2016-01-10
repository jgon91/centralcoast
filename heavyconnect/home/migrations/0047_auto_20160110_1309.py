# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0046_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='break',
            name='break_num',
        ),
        migrations.AddField(
            model_name='taskcode',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='taskcode',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='break',
            name='lunch',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='language',
            field=models.IntegerField(default=3, choices=[(1, b'pt-br'), (2, b'es'), (3, b'en-us')]),
        ),
    ]
