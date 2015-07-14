# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appendix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('a_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AppendixTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('brand', models.CharField(max_length=20)),
                ('appendix', models.ForeignKey(to='home.Appendix')),
            ],
        ),
        migrations.CreateModel(
            name='Break',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.TimeField()),
                ('end', models.TimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField()),
                ('company_id', models.CharField(max_length=10)),
                ('language', models.IntegerField(choices=[(1, b'pt-br'), (2, b'es'), (3, b'en')])),
                ('qr_code', models.CharField(max_length=10)),
                ('start_date', models.DateField()),
                ('hour_cost', models.FloatField()),
                ('contact_number', models.CharField(max_length=14)),
                ('permission_level', models.IntegerField(choices=[(1, b'Driver'), (2, b'Manager')])),
                ('photo', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('hour_started', models.TimeField()),
                ('hour_ended', models.TimeField(null=True, blank=True)),
                ('employee', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeCertifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('certification', models.ForeignKey(to='home.Certification')),
                ('employee', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLocalization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('e_time', models.DateTimeField()),
                ('employee', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeQualifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(choices=[(1, b'Low'), (2, b'Medium'), (3, b'High')])),
                ('employee', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_init', models.DateTimeField(null=True, blank=True)),
                ('hours_spent', models.FloatField(default=0)),
                ('substitution', models.BooleanField()),
                ('employee', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeWithdrawn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('employee', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('category', models.ForeignKey(to='home.EquipmentCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('organic', models.BooleanField()),
                ('size', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FieldLocalization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.ForeignKey(to='home.Field')),
            ],
        ),
        migrations.CreateModel(
            name='GPS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Implement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=20)),
                ('qr_code', models.CharField(max_length=10)),
                ('asset_number', models.CharField(max_length=15)),
                ('serial_number', models.CharField(max_length=25)),
                ('horse_power_req', models.IntegerField()),
                ('hitch_capacity_req', models.IntegerField(null=True, blank=True)),
                ('hitch_category', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4N'), (5, b'4'), (6, b'5')])),
                ('drawbar_category', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'4WS'), (6, b'5'), (7, b'5WS')])),
                ('speed_range_min', models.FloatField()),
                ('speed_range_max', models.FloatField()),
                ('year_purchased', models.IntegerField()),
                ('implement_hours', models.IntegerField()),
                ('service_interval', models.IntegerField()),
                ('base_cost', models.FloatField()),
                ('hour_cost', models.FloatField()),
                ('status', models.IntegerField(choices=[(1, b'Ok'), (2, b'Attention'), (3, b'Broken'), (4, b'Quarantine')])),
                ('photo', models.URLField(blank=True)),
                ('photo1', models.URLField(blank=True)),
                ('photo2', models.URLField(blank=True)),
                ('equipment_type', models.ForeignKey(to='home.EquipmentType')),
            ],
        ),
        migrations.CreateModel(
            name='ImplementCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('certification', models.ForeignKey(to='home.Certification')),
                ('implement', models.ForeignKey(to='home.Implement')),
            ],
        ),
        migrations.CreateModel(
            name='ImplementChecklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.BooleanField()),
                ('note', models.CharField(max_length=200, blank=True)),
                ('date', models.DateTimeField()),
                ('photo', models.URLField(blank=True)),
                ('qrCode', models.ForeignKey(to='home.Implement')),
            ],
        ),
        migrations.CreateModel(
            name='ImplementQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qualification_required', models.IntegerField(choices=[(1, b'Low'), (2, b'Medium'), (3, b'High')])),
                ('implement', models.ForeignKey(to='home.Implement')),
            ],
        ),
        migrations.CreateModel(
            name='ImplementService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('assigned_date', models.DateTimeField()),
                ('expected_date', models.DateTimeField()),
                ('accomplished_date', models.DateTimeField(null=True, blank=True)),
                ('price', models.FloatField()),
                ('implement', models.ForeignKey(to='home.Implement')),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=20)),
                ('qr_code', models.CharField(max_length=10)),
                ('asset_number', models.CharField(max_length=15)),
                ('serial_number', models.CharField(max_length=25, null=True)),
                ('horsepower', models.IntegerField()),
                ('hitch_capacity', models.IntegerField()),
                ('hitch_category', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4N'), (5, b'4'), (6, b'5')])),
                ('drawbar_category', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'4WS'), (6, b'5'), (7, b'5WS')])),
                ('speed_range_min', models.FloatField()),
                ('speed_range_max', models.FloatField()),
                ('year_purchased', models.IntegerField()),
                ('engine_hours', models.IntegerField()),
                ('service_interval', models.IntegerField()),
                ('base_cost', models.FloatField(default=0)),
                ('m_type', models.CharField(max_length=1, choices=[(b'T', b'Track'), (b'W', b'Wheels')])),
                ('front_tires', models.CharField(max_length=20)),
                ('rear_tires', models.CharField(max_length=20)),
                ('steering', models.CharField(max_length=1, choices=[(b'M', b'Manual'), (b'G', b'GPS')])),
                ('operator_station', models.CharField(max_length=1, choices=[(b'a', b'Cab'), (b'b', b'Open'), (b'c', b'Canopy')])),
                ('status', models.IntegerField(null=True, choices=[(1, b'Ok'), (2, b'Attention'), (3, b'Broken'), (4, b'Quarantine')])),
                ('hour_cost', models.FloatField()),
                ('photo', models.URLField(blank=True)),
                ('photo1', models.URLField(blank=True)),
                ('photo2', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MachineCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('certification', models.ForeignKey(to='home.Certification')),
                ('machine', models.ForeignKey(to='home.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='MachineChecklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.BooleanField()),
                ('note', models.CharField(max_length=200, blank=True)),
                ('date', models.DateTimeField()),
                ('photo', models.URLField(blank=True)),
                ('qrCode', models.ForeignKey(to='home.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='MachineQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qualification_required', models.IntegerField(choices=[(1, b'Low'), (2, b'Medium'), (3, b'High')])),
                ('machine', models.ForeignKey(to='home.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='MachineService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('assigned_date', models.DateTimeField()),
                ('expected_date', models.DateTimeField()),
                ('accomplished_date', models.DateTimeField(null=True, blank=True)),
                ('price', models.FloatField()),
                ('machine', models.ForeignKey(to='home.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ManufacturerModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.CharField(max_length=30)),
                ('manufacturer', models.ForeignKey(to='home.Manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=250)),
                ('category', models.IntegerField(choices=[(1, b'Before Lunch Break'), (2, b'Post Lunch Pre Start'), (3, b'Post Lunch Start'), (4, b'End of Day Inspection')])),
                ('refers', models.IntegerField(choices=[(1, b'Machine'), (2, b'Implement')])),
            ],
        ),
        migrations.CreateModel(
            name='RepairShop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('number', models.CharField(max_length=14)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_category', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('number', models.CharField(max_length=14)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate_cost', models.FloatField(default=0, null=True)),
                ('hours_spent', models.FloatField(default=0, null=True)),
                ('hours_prediction', models.FloatField()),
                ('description', models.CharField(max_length=500)),
                ('passes', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('accomplished', models.BooleanField(default=False)),
                ('approval', models.IntegerField(default=4, choices=[(1, b'Approved'), (2, b'Denied'), (3, b'Pending'), (4, b'Setup')])),
            ],
        ),
        migrations.CreateModel(
            name='TaskCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TaskImplementMachine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('implement', models.ForeignKey(to='home.Implement')),
                ('machine', models.ForeignKey(to='home.Machine')),
                ('task', models.ForeignKey(to='home.Task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.ForeignKey(to='home.TaskCategory'),
        ),
        migrations.AddField(
            model_name='task',
            name='field',
            field=models.ForeignKey(to='home.Field'),
        ),
        migrations.AddField(
            model_name='machineservice',
            name='service',
            field=models.ForeignKey(to='home.ServiceCategory'),
        ),
        migrations.AddField(
            model_name='machinequalification',
            name='qualification',
            field=models.ForeignKey(to='home.Qualification'),
        ),
        migrations.AddField(
            model_name='machinechecklist',
            name='question',
            field=models.ForeignKey(to='home.Question'),
        ),
        migrations.AddField(
            model_name='machine',
            name='manufacturer_model',
            field=models.ForeignKey(to='home.ManufacturerModel'),
        ),
        migrations.AddField(
            model_name='machine',
            name='repair_shop',
            field=models.ForeignKey(to='home.RepairShop'),
        ),
        migrations.AddField(
            model_name='machine',
            name='shop',
            field=models.ForeignKey(to='home.Shop'),
        ),
        migrations.AddField(
            model_name='implementservice',
            name='service',
            field=models.ForeignKey(to='home.ServiceCategory'),
        ),
        migrations.AddField(
            model_name='implementqualification',
            name='qualification',
            field=models.ForeignKey(to='home.Qualification'),
        ),
        migrations.AddField(
            model_name='implementchecklist',
            name='question',
            field=models.ForeignKey(to='home.Question'),
        ),
        migrations.AddField(
            model_name='implement',
            name='manufacturer_model',
            field=models.ForeignKey(to='home.ManufacturerModel'),
        ),
        migrations.AddField(
            model_name='implement',
            name='repair_shop',
            field=models.ForeignKey(to='home.RepairShop'),
        ),
        migrations.AddField(
            model_name='implement',
            name='shop',
            field=models.ForeignKey(to='home.Shop'),
        ),
        migrations.AddField(
            model_name='fieldlocalization',
            name='gps',
            field=models.ForeignKey(to='home.GPS'),
        ),
        migrations.AddField(
            model_name='employeetask',
            name='task',
            field=models.ForeignKey(to='home.Task'),
        ),
        migrations.AddField(
            model_name='employeequalifications',
            name='qualification',
            field=models.ForeignKey(to='home.Qualification'),
        ),
        migrations.AddField(
            model_name='employee',
            name='last_task',
            field=models.ForeignKey(blank=True, to='home.Task', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='break',
            name='attendance',
            field=models.ForeignKey(to='home.EmployeeAttendance'),
        ),
        migrations.AddField(
            model_name='appendixtask',
            name='task',
            field=models.ForeignKey(to='home.Task'),
        ),
    ]
