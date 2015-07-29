# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20150728_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslatedQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=250)),
                ('idiom', models.IntegerField(default=1, choices=[(1, b'es'), (2, b'pt-br')])),
                ('question', models.ForeignKey(to='home.Question')),
            ],
        ),
    ]
