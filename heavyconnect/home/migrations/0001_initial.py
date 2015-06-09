# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import home.models


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
                ('appendix_id', models.ForeignKey(to='home.Appendix')),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.IntegerField()),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_id', models.CharField(max_length=10)),
                ('qr_code', models.CharField(max_length=10)),
                ('start_date', models.DateField()),
                ('hour_cost', models.FloatField()),
                ('photo', models.URLField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('hour_started', models.TimeField()),
                ('hour_ended', models.TimeField()),
                ('morning_break', models.TimeField()),
                ('morning_break_end', models.TimeField()),
                ('afternoon_break', models.TimeField()),
                ('afternoon_break_end', models.TimeField()),
                ('evening_break', models.TimeField()),
                ('evening_break_end', models.TimeField()),
                ('employee_id', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeCertifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('certification_id', models.ForeignKey(to='home.Certification')),
                ('employee_id', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLocalization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('e_time', models.DateTimeField()),
                ('employee_id', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeQualifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('employee_id', models.ForeignKey(to='home.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_init', models.DateField()),
                ('hours_spent', models.FloatField()),
                ('substitution', models.BooleanField()),
                ('employee_id', models.ForeignKey(to='home.Employee')),
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
                ('field_id', models.ForeignKey(to='home.Field')),
            ],
        ),
        migrations.CreateModel(
            name='GPS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.CharField(max_length=15)),
                ('longitude', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Implement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qr_code', models.CharField(max_length=10)),
                ('asset_number', models.CharField(max_length=15)),
                ('serial_number', models.CharField(max_length=25)),
                ('horse_power_req', models.IntegerField()),
                ('hitch_capacity_req', models.IntegerField()),
                ('hitch_category', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4N'), (5, '4'), (6, '5')])),
                ('drawbar_category', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'4WS'), (6, b'5'), (7, b'5WS')])),
                ('speed_range_min', models.FloatField()),
                ('speed_range_max', models.FloatField()),
                ('year_purchased', models.IntegerField()),
                ('implement_hours', models.IntegerField()),
                ('service_interval', models.IntegerField()),
                ('base_cost', models.FloatField()),
                ('hour_cost', models.FloatField()),
                ('photo', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ImplementCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('certification_id', models.ForeignKey(to='home.Certification')),
                ('implement_id', models.ForeignKey(to='home.Implement')),
            ],
        ),
        migrations.CreateModel(
            name='ImplementQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('implement_id', models.ForeignKey(to='home.Implement')),
            ],
        ),
        migrations.CreateModel(
            name='ImplementService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('expected_date', models.DateTimeField()),
                ('done', models.BooleanField()),
                ('price', models.FloatField()),
                ('implement_id', models.ForeignKey(to='home.Implement')),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qr_code', models.CharField(max_length=10)),
                ('asset_number', models.CharField(max_length=15)),
                ('serial_number', models.CharField(max_length=25, null=True)),
                ('horsepower', models.IntegerField()),
                ('hitch_capacity', models.IntegerField()),
                ('hitch_category', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4N'), (5, '4'), (6, '5')])),
                ('drawbar_category', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'4WS'), (6, b'5'), (7, b'5WS')])),
                ('speed_range_min', models.FloatField()),
                ('speed_range_max', models.FloatField()),
                ('year_purchased', models.IntegerField()),
                ('engine_hours', models.IntegerField()),
                ('service_interval', models.IntegerField()),
                ('base_cost', models.FloatField()),
                ('front_tires', models.CharField(max_length=20)),
                ('rear_tires', models.CharField(max_length=20)),
                ('hour_cost', models.FloatField()),
                ('photo', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='MachineCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('certification_id', models.ForeignKey(to='home.Certification')),
                ('machine_id', models.ForeignKey(to='home.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='MachineQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('machine_id', models.ForeignKey(to='home.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='MachineService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('done', models.BooleanField()),
                ('expected_date', models.DateTimeField()),
                ('price', models.FloatField()),
                ('machine_id', models.ForeignKey(to='home.Machine')),
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
                ('model', models.ForeignKey(to='home.Manufacturer')),
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
            name='RepairShop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_name', models.CharField(max_length=20)),
                ('contact_number', models.IntegerField()),
                ('contact_address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_id', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('done', models.BooleanField()),
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
                ('contact_name', models.CharField(max_length=20)),
                ('contact_number', models.IntegerField()),
                ('contact_address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('t_type', models.CharField(max_length=100)),
                ('rate_cost', models.FloatField()),
                ('hours_spent', models.FloatField()),
                ('hours_prediction', models.FloatField()),
                ('description', models.CharField(max_length=500)),
                ('passes', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('accomplished', models.BooleanField()),
                ('approval', models.BooleanField()),
                ('field_id', models.ForeignKey(to='home.Field')),
            ],
        ),
        migrations.CreateModel(
            name='TaskImplementMachine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('implement_id', models.IntegerField(verbose_name=home.models.Implement)),
                ('machine', models.BooleanField()),
                ('machine_id', models.ForeignKey(to='home.Machine')),
                ('task_id', models.ForeignKey(to='home.Task')),
            ],
        ),
        migrations.AddField(
            model_name='machineservice',
            name='service_id',
            field=models.ForeignKey(to='home.Service'),
        ),
        migrations.AddField(
            model_name='machinequalification',
            name='qualification_id',
            field=models.ForeignKey(to='home.Qualification'),
        ),
        migrations.AddField(
            model_name='machine',
            name='manufacturer_model_id',
            field=models.ForeignKey(to='home.ManufacturerModel'),
        ),
        migrations.AddField(
            model_name='machine',
            name='repair_shop_id',
            field=models.ForeignKey(to='home.RepairShop'),
        ),
        migrations.AddField(
            model_name='machine',
            name='shop_id',
            field=models.ForeignKey(to='home.Shop'),
        ),
        migrations.AddField(
            model_name='implementservice',
            name='service_id',
            field=models.ForeignKey(to='home.Service'),
        ),
        migrations.AddField(
            model_name='implementqualification',
            name='qualification_id',
            field=models.ForeignKey(to='home.Qualification'),
        ),
        migrations.AddField(
            model_name='implement',
            name='manufacturer_model_id',
            field=models.ForeignKey(to='home.ManufacturerModel'),
        ),
        migrations.AddField(
            model_name='implement',
            name='repair_shop_id',
            field=models.ForeignKey(to='home.RepairShop'),
        ),
        migrations.AddField(
            model_name='implement',
            name='shop_id',
            field=models.ForeignKey(to='home.Shop'),
        ),
        migrations.AddField(
            model_name='fieldlocalization',
            name='gps_id',
            field=models.ForeignKey(to='home.GPS'),
        ),
        migrations.AddField(
            model_name='employeetask',
            name='task_id',
            field=models.ForeignKey(to='home.Task'),
        ),
        migrations.AddField(
            model_name='employeequalifications',
            name='qualification_id',
            field=models.ForeignKey(to='home.Qualification'),
        ),
        migrations.AddField(
            model_name='employeelocalization',
            name='gps_id',
            field=models.ForeignKey(to='home.GPS'),
        ),
        migrations.AddField(
            model_name='appendixtask',
            name='task_id',
            field=models.ForeignKey(to='home.Task'),
        ),
    ]
