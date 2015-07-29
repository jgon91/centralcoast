# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_employee_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='implementchecklist',
            old_name='qrCode',
            new_name='qr_code',
        ),
        migrations.RenameField(
            model_name='machinechecklist',
            old_name='qrCode',
            new_name='qr_code',
        ),
        migrations.AddField(
            model_name='implement',
            name='note',
            field=models.CharField(max_length=250, blank=True),
        ),
        migrations.AddField(
            model_name='machine',
            name='note',
            field=models.CharField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='notes',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
