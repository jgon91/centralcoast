# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20150827_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='company_id',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hour_cost',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='qr_code',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
