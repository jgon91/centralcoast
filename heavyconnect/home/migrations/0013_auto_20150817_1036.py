# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20150730_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='home.TaskCategory')),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.AddField(
            model_name='break',
            name='break_num',
            field=models.IntegerField(default=1, choices=[(1, b'0'), (2, b'1'), (3, b'2'), (4, b'3'), (5, b'4'), (6, b'5')]),
        ),
        migrations.AddField(
            model_name='task',
            name='code',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='field',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='hours_prediction',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='passes',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(default=1, null=True, choices=[(1, b'Pending'), (2, b'Approved'), (3, b'Denied'), (4, b'Ongoing'), (5, b'Paused'), (6, b'Finished')]),
        ),
    ]
