# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_break_lunch'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='manager',
            field=models.ForeignKey(blank=True, to='home.Employee', null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='company_id',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='contact_number',
            field=models.CharField(max_length=14, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hour_cost',
            field=models.FloatField(null=True, blank=True),
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
