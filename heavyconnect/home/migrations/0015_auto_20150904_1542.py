# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20150830_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='base_cost',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='drawbar_category',
            field=models.IntegerField(default=1, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'4WS'), (6, b'5'), (7, b'5WS')]),
        ),
        migrations.AlterField(
            model_name='machine',
            name='engine_hours',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='machine',
            name='front_tires',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='hitch_capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='machine',
            name='hitch_category',
            field=models.IntegerField(default=0, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4N'), (5, b'4'), (6, b'5')]),
        ),
        migrations.AlterField(
            model_name='machine',
            name='horsepower',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='machine',
            name='hour_cost',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='m_type',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'T', b'Track'), (b'W', b'Wheels')]),
        ),
        migrations.AlterField(
            model_name='machine',
            name='note',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='operator_station',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'a', b'Cab'), (b'b', b'Open'), (b'c', b'Canopy')]),
        ),
        migrations.AlterField(
            model_name='machine',
            name='photo',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='photo1',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='photo2',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='qr_code',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='rear_tires',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='repair_shop',
            field=models.ForeignKey(to='home.RepairShop', null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='service_interval',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='machine',
            name='shop',
            field=models.ForeignKey(to='home.Shop', null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='speed_range_max',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='speed_range_min',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'Ok'), (2, b'Attention'), (3, b'Broken'), (4, b'Quarantine')]),
        ),
        migrations.AlterField(
            model_name='machine',
            name='steering',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'Manual'), (b'G', b'GPS')]),
        ),
        migrations.AlterField(
            model_name='machine',
            name='year_purchased',
            field=models.IntegerField(default=0),
        ),
    ]
