# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20150730_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='company_id',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='contact_number',
            field=models.CharField(max_length=14, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hour_cost',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='language',
            field=models.IntegerField(default=3, choices=[(1, b'pt-br'), (2, b'es'), (3, b'en')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='permission_level',
            field=models.IntegerField(default=1, choices=[(1, b'Driver'), (2, b'Manager')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='qr_code',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='start_date',
            field=models.DateField(blank=True),
        ),
    ]
