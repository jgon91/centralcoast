# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_remove_employee_picfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='picFile',
            field=models.ImageField(default=b'pic_employee/None/no-img.jpg', upload_to=b'pic_employee/'),
        ),
    ]
