'''
	@andreemenezes
	06/10/2015
	menezescode@gmail.com
'''

from django import forms
from django.contrib.auth.models import User
from home.models import * 

class loginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

### Structure for Manufacturer Form ###
class manufacturerForm(forms.Form):
	name = forms.CharField(max_length = 20)

class manufacturerModelForm(forms.Form):
	model = forms.CharField(max_length = 20)
	manufacturer = forms.ModelChoiceField(queryset = Manufacturer.objects.all())
### End ###

### Structure for Repair Shop Form ###
class repairShopForm(forms.Form):
	contact_name = forms.CharField(max_length = 20)
	contact_number =  forms.CharField(max_length = 14)
	contact_address = forms.CharField(max_length = 150)
### End ###

### Structure for Shop Form ###
class shopForm(forms.Form):
	contact_name = forms.CharField()
	contact_number = forms.CharField()
	contact_address = forms.CharField()
### End ###

### Structure for Machine Form ###
class machineForm(forms.Form):
	HITCH_CHOICES = (
		(1, u'1'),
		(2, u'2'),
		(3, u'3'),
		(4, u'4N'),
		(5, u'4'),
		(6, u'5'),
	)
	DRAWBAR_CHOICES = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '4WS'),
		(6, '5'),
		(7, '5WS'),
	)
	manufacturer_model_id = forms.ModelChoiceField(queryset = ManufacturerModel.objects.all())
	repair_shop_id = forms.ModelChoiceField(queryset = RepairShop.objects.all())
	shop_id = forms.ModelChoiceField(queryset = Shop.objects.all())
	qr_code = forms.CharField(max_length = 10)
	asset_number = forms.CharField(max_length = 15)
	serial_number = forms.CharField(max_length = 25, required = True)
	horsepower = forms.IntegerField()
	hitch_capacity = forms.IntegerField()
	hitch_category = forms.ChoiceField(choices = HITCH_CHOICES)
	drawbar_category = forms.ChoiceField(choices = DRAWBAR_CHOICES)
	speed_range_min = forms.FloatField()
	speed_range_max = forms.FloatField()
	year_purchased = forms.IntegerField()
	engine_hours = forms.IntegerField()
	service_interval = forms.IntegerField()
	base_cost = forms.FloatField()
	m_type = forms.ChoiceField(choices = (('T', 'Track'), ('W', 'Wheels')), required = True)
	front_tires = forms.CharField(max_length = 20)														
	rear_tires = forms.CharField(max_length = 20)
	steering = forms.ChoiceField(choices = (('M', 'Manual'), ('G', 'GPS')), required = True)
	operator_station =  forms.ChoiceField(choices = (('C', 'Cab'), ('O', 'Open')), required = True)
	status = forms.ChoiceField(choices = ((1, 'Ok'), (2, 'Attention'), (3, 'Broken'), (4, 'Quarantine')), required = True)
	hour_cost = forms.FloatField()
	photo = forms.URLField(max_length=200)
### End ###
'''
### Structure for Implement Form ###
class implementForm(forms.Form):
	manufacturer_model_id = forms.ForeignKey(ManufacturerForm)
	repair_shop_id = forms.ForeignKey(RepairShop)
	shop_id = forms.ForeignKey(Shop)
	qr_code = forms.CharField()
	asset_number = forms.CharField()
	serial_number = forms.CharField()
	horse_power_req = forms.IntegerField()
	hitch_capacity_req = forms.IntegerField()
	hitch_category = forms.IntegerField(choices = Machine.HITCH_CHOICES)
	drawbar_category = forms.IntegerField(choices = Machine.DRAWBAR_CHOICES)
	speed_range_min = forms.FloatField()
	speed_range_max = forms.FloatField()
	year_purchased = forms.IntegerField()
	implement_hours = forms.IntegerField()	
	service_interval = forms.IntegerField()
	base_cost = forms.FloatField()
	hour_cost = forms.FloatField()
	status = forms.IntegerField(choices = Machine.STATUS_CHOICES)
	photo = forms.URLField()
### End ###


class employeeForm(forms.Form):
	user = forms.OneToOneField(User)
	company_id = forms.CharField()
	qr_code = forms.CharField()
	start_date = forms.DateField()
	hour_cost = forms.FloatField()
	contact_number = forms.CharField()
	permission_level = forms.IntegerField(choices = ((1, 'Driver'), (2, 'Manager')))
	photo = forms.URLField()

class employeeAttendanceForm(forms.Form):
	employee_id = forms.ForeignKey(Employee)
	date = forms.DateField()
	hour_started = forms.TimeField()
	hour_ended = forms.TimeField()
	morning_break = forms.TimeField()
	morning_break_end = forms.TimeField()
	afternoon_break = forms.TimeField()
	afternoon_break_end = forms.TimeField()
	evening_break = forms.TimeField()
	evening_break_end = forms.TimeField()

class qualificationForm(forms.Form):
	description = forms.CharField()

class certificationForm(forms.Form):
	category = forms.IntegerField()
	description = forms.CharField()

class EmployeeQualificationsForm(forms.Form):
	employee_id =  forms.ForeignKey(Employee)
	qualification_id =  forms.ForeignKey(Qualification)
	level = forms.IntegerField(choices = ((1, 'Low'), (2, 'Medium'), (3, 'High')))

class MachineQualificationForm(forms.Form):
	machine_id = forms.ForeignKey(Machine)
	qualification_id = forms.ForeignKey(Qualification)
	qualification_required = forms.IntegerField(choices = ((1, 'Low'), (2, 'Medium'), (3, 'High')))

class ImplementQualificationForm(forms.Form):
	implement_id = forms.ForeignKey(Implement)
	qualification_id = forms.ForeignKey(Qualification)
	qualification_required = forms.IntegerField(choices = ((1, 'Low'), (2, 'Medium'), (3, 'High')))

class FieldForm(forms.Form):
	name = forms.CharField()
	organic = forms.BooleanField()
	size =  forms.FloatField()

class GPSForm(forms.Form):
	latitude = forms.CharField()
	longitude = forms.CharField()

class EmployeeLocalizationForm(forms.Form):
	employee_id = forms.ForeignKey(Employee)
	gps_id = forms.ForeignKey(GPS)
	e_time = forms.DateTimeField()

class TaskForm(forms.Form):
	field_id = forms.ForeignKey(Field)
	t_type = forms.CharField()
	rate_cost = forms.FloatField()
	hours_spent = forms.FloatField()
	hours_prediction = forms.FloatField()
	description =  forms.CharField()
	passes = forms.IntegerField()
	date = forms.DateTimeField()
	accomplished = forms.BooleanField()
	approval = forms.BooleanField()

class EmployeeTaskForm(forms.Form):
	employee_id = forms.ForeignKey(Employee)
	task_id = forms.ForeignKey(Task)
	task_init = forms.DateField()
	hours_spent = forms.FloatField()
	substitution = forms.BooleanField()

class TaskImplementMachineForm(forms.Form):
	task_id = forms.ForeignKey(Task)
	machine_id = forms.ForeignKey(Machine)
	implement_id = forms.ForeignKey(Implement)
	machine = forms.BooleanField()

class AppendixForm(forms.Form):
	a_type = forms.CharField()

class AppendixTaskForm(forms.Form):
	appendix_id = forms.ForeignKey(Appendix)
	task_id = forms.ForeignKey(Task)
	quantity = forms.IntegerField()
	brand = forms.CharField()

class ServiceCategoryForm(forms.Form):
	service_category = forms.CharField()

class ServiceForm(forms.Form):
	category_id = forms.ForeignKey(ServiceCategory)
	date = forms.DateTimeField()
	done = forms.BooleanField()

class MachineServiceForm(forms.Form):
	machine_id = forms.ForeignKey(Machine)
	service_id = forms.ForeignKey(Service)
	description = forms.CharField()
	done = forms.BooleanField()
	expected_date = forms.DateTimeField()
	price = forms.FloatField()

class ImplementServiceForm(forms.Form):
	implement_id = forms.ForeignKey(Implement)
	service_id = forms.ForeignKey(Service)
	description = forms.CharField()
	expected_date = forms.DateTimeField()
	done = forms.BooleanField()
	price = forms.FloatField()
'''