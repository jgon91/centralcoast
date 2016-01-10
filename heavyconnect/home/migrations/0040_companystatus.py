# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0039_auto_20151208_0833'),
    ]

    operations = [
        migrations.CreateModel(
            name='companyStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('employ_limit', models.IntegerField(default=10)),
            ],
        ),
    ]
