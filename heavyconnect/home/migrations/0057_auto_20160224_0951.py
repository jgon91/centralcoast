# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0056_employeeattendance_managerrejected'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeattendance',
            old_name='managerApproved',
            new_name='manager_approved',
        ),
        migrations.RenameField(
            model_name='employeeattendance',
            old_name='managerRejected',
            new_name='manager_rejected',
        ),
    ]
