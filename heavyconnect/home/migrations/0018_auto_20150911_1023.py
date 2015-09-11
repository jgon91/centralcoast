# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20150904_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='drawbar_category',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'4WS'), (6, b'5'), (7, b'5WS')]),
        ),
        migrations.AlterField(
            model_name='machine',
            name='engine_hours',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='hitch_capacity',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='hitch_category',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4N'), (5, b'4'), (6, b'5')]),
        ),
        migrations.AlterField(
            model_name='machine',
            name='horsepower',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='repair_shop',
            field=models.ForeignKey(blank=True, to='home.RepairShop', null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='serial_number',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='service_interval',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='shop',
            field=models.ForeignKey(blank=True, to='home.Shop', null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='year_purchased',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
