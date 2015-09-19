# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_employee_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='implement',
            name='equipment_type',
        ),
        migrations.AlterField(
            model_name='implement',
            name='base_cost',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='drawbar_category',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'4WS'), (6, b'5'), (7, b'5WS')]),
        ),
        migrations.AlterField(
            model_name='implement',
            name='hitch_category',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4N'), (5, b'4'), (6, b'5')]),
        ),
        migrations.AlterField(
            model_name='implement',
            name='horse_power_req',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='hour_cost',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='implement_hours',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='note',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='photo',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='photo1',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='photo2',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='qr_code',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='repair_shop',
            field=models.ForeignKey(blank=True, to='home.RepairShop', null=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='service_interval',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='shop',
            field=models.ForeignKey(blank=True, to='home.Shop', null=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='speed_range_max',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='speed_range_min',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='implement',
            name='year_purchased',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
