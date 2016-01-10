# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_delete_companystatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('employ_limit', models.IntegerField(default=10)),
            ],
        ),
    ]
