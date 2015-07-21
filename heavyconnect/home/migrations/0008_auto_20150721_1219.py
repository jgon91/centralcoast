# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20150717_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beacon_serial', models.CharField(max_length=10, null=True)),
                ('refers', models.IntegerField(choices=[(1, b'Machine'), (2, b'Implement')])),
            ],
        ),
        migrations.CreateModel(
            name='BeaconGPS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('beacon', models.ForeignKey(to='home.Beacon')),
                ('gps', models.ForeignKey(to='home.GPS')),
            ],
        ),
        migrations.AddField(
            model_name='implement',
            name='beacon',
            field=models.ForeignKey(blank=True, to='home.Beacon', null=True),
        ),
        migrations.AddField(
            model_name='machine',
            name='beacon',
            field=models.ForeignKey(blank=True, to='home.Beacon', null=True),
        ),
    ]
