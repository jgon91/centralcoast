# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_remove_employee_picfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='photoEmployee',
            field=models.ImageField(default=b'employee/no.jpg', upload_to=b'employee'),
        ),
    ]
