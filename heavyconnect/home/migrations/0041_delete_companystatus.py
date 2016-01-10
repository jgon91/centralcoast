# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_companystatus'),
    ]

    operations = [
        migrations.DeleteModel(
            name='companyStatus',
        ),
    ]
