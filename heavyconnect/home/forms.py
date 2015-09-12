'''
	@menezescode
	06/10/2015
	menezescode@gmail.com

	notes: All the BooleanField are (required = False). This is hapening because if we don't
	use the required false the form will only work when the checkbox is marked.
'''

from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget

import datetime
import json

from home.models import *

class loginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

### Structure for manufacturerForm ###
class manufacturerForm(forms.Form):
	name = forms.CharField(max_length = 20)
### End ###

### Structure for manufacturerModelForm ###
class manufacturerModelForm(forms.Form):
	model = forms.CharField(max_length = 20)
	manufacturer = forms.ModelChoiceField(queryset = Manufacturer.objects.all())
### End ###

### Structure for repairShopForm ###
class repairShopForm(forms.Form):
	name = forms.CharField(max_length = 20)
	number =  forms.CharField(max_length = 14)
	address = forms.CharField(max_length = 150)
### End ###

### Structure for shopForm ###
class shopForm(forms.Form):
	name = forms.CharField(max_length = 20)
	number = forms.CharField(max_length = 14)
	address = forms.CharField(max_length = 150)
### End ###

### Structure for EquipmentCategoryForm ###
class equipmentCategoryForm(forms.Form):
	name = forms.CharField(max_length = 25)
### End ###

### Structure for EquipmentTypeForm ###
class equipmentTypeForm(forms.Form):
	category = forms.ModelChoiceField(queryset = EquipmentCategory.objects.all())
	name = forms.CharField(max_length = 25)
### End ###


### Structure for MachineUpdateForm ###
class machineUpdateForm(forms.Form):
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
	MTYPE_CHOICES = (
		('T', 'Track'),
		('W', 'Wheels'),
	)
	STEERING_CHOICES = (
		('M', 'Manual'),
		('G', 'GPS')
	)
	OPERATORSTATION_CHOICES = (
		('C', 'Cab'),
		('O', 'Open'),
	)
	STATUS_CHOICES = (
		(1, 'Ok'),
		(2, 'Attention'),
		(3, 'Broken'),
		(4, 'Quarantine'),
	)
	machine_id = forms.IntegerField()
	manufacturer_model = forms.ModelChoiceField(queryset = ManufacturerModel.objects.all())
	nickname = forms.CharField(max_length = 20)
	asset_number = forms.CharField(max_length = 15)
	serial_number = forms.CharField(max_length = 25)
	repair_shop = forms.ModelChoiceField(queryset = RepairShop.objects.all(), required = False)
	shop = forms.ModelChoiceField(queryset = Shop.objects.all(), required = False)
	#equipment_type = forms.ModelChoiceField(queryset = EquipmentType.objects.all(), required = False)
	qr_code = forms.CharField(max_length = 10, required = False)
	horsepower = forms.IntegerField(required = False)
	hitch_capacity = forms.IntegerField(required = False)
	hitch_category = forms.ChoiceField(choices = HITCH_CHOICES, required = False)
	drawbar_category = forms.ChoiceField(choices = DRAWBAR_CHOICES, required = False)
	speed_range_min = forms.FloatField(required = False)
	speed_range_max = forms.FloatField(required = False)
	year_purchased = forms.IntegerField(required = False)
	engine_hours = forms.IntegerField(required = False)
	service_interval = forms.IntegerField(required = False)
	base_cost = forms.FloatField(required = False)
	m_type = forms.ChoiceField(choices = MTYPE_CHOICES, required = False)
	front_tires = forms.CharField(max_length = 20, required = False)
	rear_tires = forms.CharField(max_length = 20, required = False)
	steering = forms.ChoiceField(choices = STEERING_CHOICES, required = False)
	operator_station = forms.ChoiceField(choices = OPERATORSTATION_CHOICES, required = False)
	status = forms.ChoiceField(choices = STATUS_CHOICES, required = False)
	hour_cost = forms.FloatField(required = False)
	beacon = forms.ModelChoiceField(queryset = Beacon.objects.all(), required = False)
	note = forms.CharField(max_length = 250, required = False)
	photo = forms.URLField(max_length = 200, required = False)
	photo1 = forms.URLField(max_length = 200, required = False)
	photo2 = forms.URLField(max_length = 200, required = False)
### End ###


### End ###

### Structure for machineForm ###
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
	MTYPE_CHOICES = (
		('T', 'Track'),
		('W', 'Wheels'),
	)
	STEERING_CHOICES = (
		('M', 'Manual'),
		('G', 'GPS')
	)
	OPERATORSTATION_CHOICES = (
		('C', 'Cab'),
		('O', 'Open'),
	)
	STATUS_CHOICES = (
		(1, 'Ok'),
		(2, 'Attention'),
		(3, 'Broken'),
		(4, 'Quarantine'),
	)
	manufacturer_model = forms.ModelChoiceField(queryset = ManufacturerModel.objects.all())
	nickname = forms.CharField(max_length = 20)
	asset_number = forms.CharField(max_length = 15)
	serial_number = forms.CharField(max_length = 25)
	repair_shop = forms.ModelChoiceField(queryset = RepairShop.objects.all(), required = False)
	shop = forms.ModelChoiceField(queryset = Shop.objects.all(), required = False)
	#equipment_type = forms.ModelChoiceField(queryset = EquipmentType.objects.all(), required = False)
	qr_code = forms.CharField(max_length = 10, required = False)
	horsepower = forms.IntegerField(required = False)
	hitch_capacity = forms.IntegerField(required = False)
	hitch_category = forms.ChoiceField(choices = HITCH_CHOICES, required = False)
	drawbar_category = forms.ChoiceField(choices = DRAWBAR_CHOICES, required = False)
	speed_range_min = forms.FloatField(required = False)
	speed_range_max = forms.FloatField(required = False)
	year_purchased = forms.IntegerField(required = False)
	engine_hours = forms.IntegerField(required = False)
	service_interval = forms.IntegerField(required = False)
	base_cost = forms.FloatField(required = False)
	m_type = forms.ChoiceField(choices = MTYPE_CHOICES, required = False)
	front_tires = forms.CharField(max_length = 20, required = False)
	rear_tires = forms.CharField(max_length = 20, required = False)
	steering = forms.ChoiceField(choices = STEERING_CHOICES, required = False)
	operator_station = forms.ChoiceField(choices = OPERATORSTATION_CHOICES, required = False)
	status = forms.ChoiceField(choices = STATUS_CHOICES, required = False)
	hour_cost = forms.FloatField(required = False)
	beacon = forms.ModelChoiceField(queryset = Beacon.objects.all(), required = False)
	note = forms.CharField(max_length = 250, required = False)
	photo = forms.URLField(max_length = 200, required = False)
	photo1 = forms.URLField(max_length = 200, required = False)
	photo2 = forms.URLField(max_length = 200, required = False)
### End ###

### Structure for implementForm ###
class implementForm(forms.Form):
	manufacturer_model = forms.ModelChoiceField(queryset = ManufacturerModel.objects.all())
	repair_shop = forms.ModelChoiceField(queryset = RepairShop.objects.all())
	shop = forms.ModelChoiceField(queryset = Shop.objects.all())
	equipment_type = forms.ModelChoiceField(queryset = EquipmentType.objects.all())
	nickname = forms.CharField(max_length = 20)
	qr_code = forms.CharField()
	asset_number = forms.CharField()
	serial_number = forms.CharField()
	horse_power_req = forms.IntegerField()
	hitch_capacity_req = forms.IntegerField()
	hitch_category = forms.ChoiceField(choices = Machine.HITCH_CHOICES)
	drawbar_category = forms.ChoiceField(choices = Machine.DRAWBAR_CHOICES)
	speed_range_min = forms.FloatField()
	speed_range_max = forms.FloatField()
	year_purchased = forms.IntegerField()
	implement_hours = forms.IntegerField()
	service_interval = forms.IntegerField()
	base_cost = forms.FloatField()
	hour_cost = forms.FloatField()
	status = forms.ChoiceField(choices = Machine.STATUS_CHOICES)
	photo = forms.URLField()
### End ###


### Structure for userForm ####
class UserForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)
	first_name = forms.CharField()
	last_name = forms.CharField()

### End ###

### Structor for user password update ###
class UserFormUpdate(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
### End ###

### Structor for employee ###
class employeePasswordForm(forms.Form):
	# password = forms.CharField(widget = forms.PasswordInput)
	password1 = forms.CharField(widget = forms.PasswordInput)
	password2 = forms.CharField(widget = forms.PasswordInput)
### End ###


### Structor for employee###
class employeeForm(forms.Form):
	PERMISSION_LEVEL_CHOICES = (
		(1, 'Driver'),
		(2, 'Manager'),
	)
	LANGUAGE_CHOICES = (
		(3, 'en'),
		(2, 'es'),
		(1, 'pt-br'),
	)
	last_task = forms.ModelChoiceField(queryset = Task.objects.all(), required = False)
	user = forms.ModelChoiceField(queryset = User.objects.all(), required = False)
	active = forms.BooleanField(required = False)
	company_id = forms.CharField(required = False)
	language = forms.ChoiceField(choices = LANGUAGE_CHOICES)
	qr_code = forms.CharField(required = False)
	start_date = forms.DateField(widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")), required = False)
	hour_cost = forms.FloatField(required = False)
	contact_number = forms.CharField(required = False)
	permission_level = forms.ChoiceField(choices = PERMISSION_LEVEL_CHOICES)
	photo = forms.URLField(required = False)
	notes = forms.CharField(max_length = 250, required = False)
	manager = forms.ModelChoiceField(queryset = Employee.objects.filter(permission_level = '1'))
### End ###


### Structor for employee Update###
class employeeUpdateForm(forms.Form):
	PERMISSION_LEVEL_CHOICES = (
		(1, 'Driver'),
		(2, 'Manager'),
	)
	LANGUAGE_CHOICES = (
		(3, 'en'),
		(2, 'es'),
		(1, 'pt-br'),
	)
	last_task = forms.ModelChoiceField(queryset = Task.objects.all(), required = False)
	user = forms.IntegerField(required = False)
	active = forms.BooleanField(required = False)
	company_id = forms.CharField(required = False)
	language = forms.ChoiceField(choices = LANGUAGE_CHOICES)
	qr_code = forms.CharField(required = False)
	start_date = forms.DateField(widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")), required = False)
	hour_cost = forms.FloatField(required = False)
	contact_number = forms.CharField(required = False)
	permission_level = forms.ChoiceField(choices = PERMISSION_LEVEL_CHOICES)
	photo = forms.URLField(required = False)
	notes = forms.CharField(max_length = 250, required = False)
### End ###

### Structure for employeeAttendanceForm ###
class employeeAttendanceForm(forms.Form):
	employee = forms.ModelChoiceField(queryset = Employee.objects.all())
	date = forms.DateField()
	hour_started = forms.TimeField()
	hour_ended = forms.TimeField()
### End ###

### Structure for qualificationForm ###
class qualificationForm(forms.Form):
	description = forms.CharField()
### End ###

### Structure for certificationForm ###
class certificationForm(forms.Form):
	category = forms.IntegerField()
	description = forms.CharField()
### End ###

### Structure for employeeQualificationForm ###
class employeeQualificationsForm(forms.Form):
	LEVEL_CHOICES = (
		(1, 'Low'),
		(2, 'Medium'),
		(3, 'High'),
	)
	employee = forms.ModelChoiceField(queryset = Employee.objects.all())
	qualification = forms.ModelChoiceField(queryset = Qualification.objects.all())
	level = forms.ChoiceField(choices = LEVEL_CHOICES)
### End ###

### Structure for machineQualificationForm ###
class machineQualificationForm(forms.Form):
	QUALIFICATIONREQUIRED_CHOICES = (
		(1, 'Low'),
		(2, 'Medium'),
		(3, 'High'),
	)
	machine = forms.ModelChoiceField(queryset = Machine.objects.all())
	qualification = forms.ModelChoiceField(queryset = Qualification.objects.all())
	qualification_required = forms.ChoiceField(choices = QUALIFICATIONREQUIRED_CHOICES)
### End ###

### Structure for implementQualificationForm ###
class implementQualificationForm(forms.Form):
	implement = forms.ModelChoiceField(queryset = Implement.objects.all())
	qualification = forms.ModelChoiceField(queryset = Qualification.objects.all())
	qualification_required = forms.ChoiceField(choices = machineQualificationForm.QUALIFICATIONREQUIRED_CHOICES)
### End ###

### Structure for fieldForm ###
class fieldForm(forms.Form):
	name = forms.CharField()
	organic = forms.BooleanField(required = False)
	size =  forms.FloatField()
### End ###

### Structure for gpsForm ###
class gpsForm(forms.Form):
	latitude = forms.CharField()
	longitude = forms.CharField()
### End ###

### Structure for employeeLocalizationForm ###
class employeeLocalizationForm(forms.Form):
	employee = forms.ModelChoiceField(queryset = Employee.objects.all())
	gps = forms.ModelChoiceField(queryset = GPS.objects.all())
	e_time = forms.DateTimeField()
### End ###

### taskForm ###
class taskForm(forms.Form):
	STATUS_CHOICES = (
		(1, 'Pending'),
		(2, 'Approved'),
		(3, 'Denied'),
		(4, 'Ongoing'),
		(5, 'Paused'),
		(6, 'Finished'),
	)
	field = forms.ModelChoiceField(queryset = Field.objects.all())
	category = forms.ModelChoiceField(queryset = TaskCategory.objects.all())
	date = forms.DateTimeField(required = True)
	time = forms.TimeField(required = True)
	hours_prediction = forms.FloatField()
	description = forms.CharField()
	passes = forms.IntegerField()
	machine = forms.CharField(max_length=10)
	implement = forms.CharField(max_length=10)
	implement2 = forms.CharField(max_length=10, required = False)

	#@bss3
	def clean_implement(self):
		qr_code = self.cleaned_data['implement']
		if qr_code is None:
			return None
		else:
			try:
				return Implement.objects.get(qr_code = qr_code)
			except Implement.DoesNotExist:
				raise forms.ValidationError("This QR code do not belong do any implement!")
	
	#@bss3
	def clean_machine(self):
		qr_code = self.cleaned_data['machine']
		if qr_code is None:
			return None
		else:
			try:
				return Machine.objects.get(qr_code = qr_code)
			except Machine.DoesNotExist:
				raise forms.ValidationError("This QR code do not belong do any machine!")

	#@bss3
	def clean_implement2(self):
		qr_code = self.cleaned_data['implement2']
		if len(qr_code) == 0:
			return None
		else:
			try:
				implement2 = Implement.objects.get(qr_code = qr_code)
				if implement2 is not self.cleaned_data['implement']:
					return implement2
				else:
					raise forms.ValidationError("The second implement cannot be the same as the first!")
			except Implement.DoesNotExist:
				raise forms.ValidationError("This QR code do not belong do any implement!")
### End ###

### Structure for taskCategoryForm ###
class taskCategoryForm(forms.Form):
	description = forms.CharField()
### End ###

### Structure for employeeTaskForm ###
class employeeTaskForm(forms.Form):
	employee = forms.ModelChoiceField(queryset = Employee.objects.all())
	task = forms.ModelChoiceField(queryset = Task.objects.all())
	hours_spent = forms.FloatField()
	start_time = forms.DateTimeField(required = True)
	end_time = forms.DateTimeField(required = True)
### End ###

### Structure for appendixForm ###
class appendixForm(forms.Form):
	a_type = forms.CharField()
### End ###

### Structure for appendixTaskForm ###
class appendixTaskForm(forms.Form):
	appendix = forms.ModelChoiceField(queryset = Appendix.objects.all())
	task = forms.ModelChoiceField(queryset = Task.objects.all())
	quantity = forms.IntegerField()
	brand = forms.CharField()
### End ###

### Structure for serviceCategoryForm ###
class serviceCategoryForm(forms.Form):
	service_category = forms.CharField()
### End ###

### Structure for machineServiceForm ###
class machineServiceForm(forms.Form):
	machine = forms.ModelChoiceField(queryset = Machine.objects.all())
	service = forms.ModelChoiceField(queryset = ServiceCategory.objects.all())
	description = forms.CharField()
	done = forms.BooleanField(required = False)
	expected_date = forms.DateTimeField()
	price = forms.FloatField()
### End ###

### Structure for implementServiceForm ###
class implementServiceForm(forms.Form):
	implement = forms.ModelChoiceField(queryset = Implement.objects.all())
	service = forms.ModelChoiceField(queryset = ServiceCategory.objects.all())
	description = forms.CharField()
	expected_date = forms.DateTimeField()
	done = forms.BooleanField(required = False)
	price = forms.FloatField()
### End ###

### Structure for questionForm ###
class questionForm(forms.Form):
	description = forms.CharField(max_length = 250)
	category = forms.IntegerField()
	refers = forms.ChoiceField(choices = ((1, 'Machine'), (2, 'Implement')))
### End ###

### Structure for machineChecklistForm ###
class machineChecklistForm(forms.Form):
	question = forms.ModelChoiceField(queryset = Question.objects.all())
	qrCode = forms.ModelChoiceField(queryset = Machine.objects.all())
	employee = forms.ModelChoiceField(queryset = Employee.objects.all())
	answer = forms.BooleanField()
	note = forms.CharField(max_length = 200)
	date = forms.DateTimeField()
	photo = forms.URLField(max_length = 200)
### End ###

### Structure for implementChecklistForm ###
class implementChecklistForm(forms.Form):
	question = forms.ModelChoiceField(queryset = Question.objects.all())
	qrCode = forms.ModelChoiceField(queryset = Implement.objects.all())
	employee = forms.ModelChoiceField(queryset = Employee.objects.all())
	answer = forms.BooleanField()
	note = forms.CharField(max_length = 200)
	date = forms.DateTimeField()
	photo = forms.URLField(max_length = 200)
### End ###

### Structure for breakForm ###
class breakForm(forms.Form):
	attendance = forms.ModelChoiceField(queryset = EmployeeAttendance.objects.all())
	start = forms.TimeField()
	end = forms.TimeField(required = False)
### End ###

### Structire for beaconForm ###
class beaconForm(forms.Form):
	beacon = forms.CharField(max_length = 10)
	longitude = forms.FloatField()
	latitude = forms.FloatField()
	timestamp = forms.DateTimeField()

	def clean_beacon(self):
		serial = self.cleaned_data['beacon']

		if serial is None or serial == '':
			return None
		else:
			try:
				return Beacon.objects.get(beacon_serial = serial)
			except Beacon.DoesNotExist:
				raise forms.ValidationError("This serial do not belong do any registered bluetooth beacon.")
### End ###


def getMachineOrImplement(self):
	try:
		return Machine.objects.get(qr_code = self.cleaned_data['qr_code'])
	except Machine.DoesNotExist:
		try:
			return Implement.objects.get(qr_code = self.cleaned_data['qr_code'])
		except:
			raise forms.ValidationError('This QR code do not belong to any machine or implement')

### Structure for Checlist ###
class checkListForm(forms.Form):

	CATEGORIES = (
		(Question.CATDEFAULT, u'Default'),
	)

	category = forms.ChoiceField(choices = CATEGORIES, initial = Question.CATDEFAULT)
	qr_code = forms.CharField(max_length = 10)

	def clean_qr_code(self):
		return getMachineOrImplement(self)

class storeAnswersForm(forms.Form):
	qr_code = forms.CharField(max_length = 10)
	answers = forms.CharField(max_length = 1000)
	engine_hours = forms.IntegerField()

	def clean_qr_code(self):
		return getMachineOrImplement(self)

	def clean_answers(self):
		try:
			ans = json.loads(self.cleaned_data['answers'])
			equipment = self.cleaned_data['qr_code']
			now = datetime.datetime.now()
			ret = []

			if isinstance(equipment, Machine):
				for iten in  ans:
					awr = iten['answer']
					note = ''

					try:
						note = iten['note']
					except KeyError:
						pass

					ret.append(
						MachineChecklist(
							question = Question.objects.get(id = iten['id']),
							qr_code = equipment,
							answer = awr,
							note = note,
							date = now
						)
					)
				return ret
			elif isinstance(equipment, Implement):
				for iten in ans:
					awr = iten['answer']
					note = ''

					try:
						note = iten['note']
					except KeyError:
						pass

					ret.append(
						ImplementChecklist(
							question = Question.objects.get(id = iten['id']),
							qr_code = equipment,
							answer = awr,
							note = note,
							date = now
						)
					)
				return ret
			else:
				return None
		except ValueError:
			raise forms.ValidationError('The json with the answers are invalid')

