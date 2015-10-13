from django.db import models
from django.contrib.auth.models import User


class Manufacturer(models.Model):
	name = models.CharField(max_length = 20)

	def __unicode__(self):
		return "Manafacturer: " + self.name

class ManufacturerModel(models.Model):
	manufacturer = models.ForeignKey(Manufacturer)
	model = models.CharField(max_length = 30)

	def __unicode__(self):
		return str(self.manufacturer) + ", Model: " + str(self.model)

class RepairShop(models.Model):
	name = models.CharField(max_length = 20)
	number =  models.CharField(max_length=14)
	address = models.CharField(max_length = 150)

	def __unicode__(self):
		return "Contact: " + str(self.name) + ", Address: " + str(self.address) + ", Phone Number: " + str(self.number)

class Shop(models.Model):
	name = models.CharField(max_length = 20)
	number = models.CharField(max_length = 14)
	address = models.CharField(max_length = 150)

	def __unicode__(self):
		return "Contact: " + str(self.name) + ", Address: " + str(self.address) + ", Phone Number: " + str(self.number)


class EquipmentCategory(models.Model):
	name = models.CharField(max_length = 25)

	def __unicode__(self):
		return "name: " + str(self.name)

class EquipmentType(models.Model):
	category = models.ForeignKey(EquipmentCategory)
	name = models.CharField(max_length = 25)

	def __unicode__(self):
		return "Name: " + str(self.name) + ", Category: " + str(self.category.name)

class GPS(models.Model):
	latitude = models.FloatField()
	longitude = models.FloatField()

	def __unicode__(self):
		return "Latitude: " +str(self.latitude) + " " +  "Longitude: " +str(self.longitude)

### DEMO ###
class Beacon(models.Model):
	REFERS_CHOICES = (
		(1, 'Machine'),
		(2, 'Implement'),
	)

	beacon_serial = models.CharField(max_length=10, null = True)
	refers = models.IntegerField(choices = REFERS_CHOICES)

	def __unicode__(self):
		if self.refers == 1:
			return 'Machine Beacon: serial = ' + self.beacon_serial
		else:
			return 'Implement Beacon: serial = ' + self.beacon_serial
### DEMO ###

### DEMO ###
class BeaconGPS(models.Model):
	beacon = models.ForeignKey(Beacon)
	gps = models.ForeignKey(GPS)
	timestamp = models.DateTimeField()

	def __unicode__(self):
		return str(self.beacon) + ' ' +  str (self.gps) + ' Timestamp:' + str(self.timestamp)
### DEMO ###

class Machine(models.Model):
	#Status
	STOK = 1 #Status ok
	STAT = 2 #Status needs attentions
	STBR = 3 #Status broken
	STQU = 4 #Status quarentine

	HITCH_CHOICES = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4N'),
		(5, '4'),
		(6, '5'),
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
	STATUS_CHOICES = (
		(STOK, 'Ok'),
		(STAT, 'Attention'),
		(STBR, 'Broken'),
		(STQU, 'Quarantine'),
	)
	OPERATORSTATION_CHOICES = (
		('a', 'Cab'),
		('b', 'Open'),
		('c', 'Canopy'),
	)
	MTYPE_CHOICES = (
		('T', 'Track'),
		('W', 'Wheels'),
	)
	STEERING_CHOICES = (
		('M', 'Manual'),
		('G', 'GPS'),
	)
	manufacturer_model = models.ForeignKey(ManufacturerModel)
	repair_shop = models.ForeignKey(RepairShop)
	shop = models.ForeignKey(Shop)
	nickname = models.CharField(max_length = 20)
	qr_code = models.CharField(max_length = 10)
	asset_number = models.CharField(max_length = 15)
	serial_number = models.CharField(max_length = 25, null = True)
	horsepower = models.IntegerField()
	hitch_capacity = models.IntegerField()
	hitch_category = models.IntegerField(choices = HITCH_CHOICES)
	drawbar_category = models.IntegerField(choices = DRAWBAR_CHOICES)
	speed_range_min = models.FloatField()
	speed_range_max = models.FloatField()
	year_purchased = models.IntegerField()
	engine_hours = models.IntegerField()
	service_interval = models.IntegerField()
	base_cost = models.FloatField(default = 0)
	m_type = models.CharField(max_length = 1, choices = MTYPE_CHOICES)
	front_tires = models.CharField(max_length = 20)
	rear_tires = models.CharField(max_length = 20)
	steering = models.CharField(max_length = 1, choices = STEERING_CHOICES)
	operator_station = models.CharField(max_length = 1, choices = OPERATORSTATION_CHOICES)
	status = models.IntegerField(choices = STATUS_CHOICES, null = True)
	hour_cost = models.FloatField()
	photo = models.URLField(max_length = 200, blank = True)
	photo1 = models.URLField(max_length = 200, blank = True)
	photo2 = models.URLField(max_length = 200, blank = True)
	note = models.CharField(max_length = 250, blank = True)
	beacon = models.ForeignKey(Beacon, blank = True, null = True) #DEMO

	def __unicode__(self):
		return "Manufacturer: " + str(self.manufacturer_model.manufacturer.name) + ", Model: " + str(self.manufacturer_model.model) + ", QRcode: " + str(self.qr_code)

class Implement(models.Model):
	manufacturer_model = models.ForeignKey(ManufacturerModel)
	repair_shop = models.ForeignKey(RepairShop)
	shop = models.ForeignKey(Shop)
	nickname = models.CharField(max_length = 20)
	qr_code = models.CharField(max_length = 10)
	asset_number = models.CharField(max_length = 15)
	serial_number = models.CharField(max_length = 25)
	horse_power_req = models.IntegerField()
	hitch_capacity_req = models.IntegerField(null = True, blank = True)
	hitch_category = models.IntegerField(choices = Machine.HITCH_CHOICES)
	drawbar_category = models.IntegerField(choices = Machine.DRAWBAR_CHOICES)
	speed_range_min = models.FloatField()
	speed_range_max = models.FloatField()
	year_purchased = models.IntegerField()
	implement_hours = models.IntegerField()
	service_interval = models.IntegerField()
	base_cost = models.FloatField()
	hour_cost = models.FloatField()
	status = models.IntegerField(choices = Machine.STATUS_CHOICES)
	equipment_type = models.ForeignKey(EquipmentType)
	photo = models.URLField(max_length = 200, blank = True)
	photo1 = models.URLField(max_length = 200, blank = True)
	photo2 = models.URLField(max_length = 200, blank = True)
	note = models.CharField(max_length = 250, blank = True)
	beacon = models.ForeignKey(Beacon, blank = True, null = True) #DEMO

	def __unicode__(self):
		return "Manufacturer: " + str(self.manufacturer_model.manufacturer.name) + ", Model: " + str(self.manufacturer_model.model) + ", QRcode: " + str(self.qr_code)

class Field(models.Model):
	name = models.CharField(max_length = 50)
	organic = models.BooleanField()
	size =  models.FloatField()

	def __unicode__(self):
		return "Name: " + str(self.name) + ", Organic: " +  str(self.organic) + ", Size: " +  str(self.size)

class TaskCategory(models.Model):
	description = models.CharField(max_length = 30)

	def __unicode__(self):
		return "ID: " + str(self.id) + ", Category: " + str(self.description)

class TaskCode(models.Model):
	name = models.CharField(max_length = 100)
	category = models.ForeignKey(TaskCategory)

	def __unicode__(self):
		return "ID: " + str(self.id) + ", Name: " + str(self.name) + ", Category" + str(self.category)


class Task(models.Model):
	STATUS_CHOICES = (
		(1, 'Pending'),
		(2, 'Approved'),
		(3, 'Denied'),
		(4, 'Ongoing'),
		(5, 'Paused'),
		(6, 'Finished'),
	)
	# field = models.ForeignKey(Field)
	field = models.CharField(null = True, max_length = 100, default = 0)
	# code = models.ForeignKey(TaskCode)
	code = models.CharField(null = True, max_length = 100, default = 0)
	rate_cost = models.FloatField(null = True, default = 0)
	date_assigned = models.DateTimeField(null = True)
	hours_prediction = models.FloatField(null = True, default = 0)
	description =  models.CharField(null = True, max_length = 500)
	passes = models.IntegerField(null = True, default = 0)
	task_init = models.DateTimeField(null = True, blank = True)
	task_end = models.DateTimeField(null = True, blank = True)
	hours_spent = models.FloatField(null = True, default = 0)
	pause_start = models.DateTimeField(null = True, blank = True)
	pause_end = models.DateTimeField(null = True, blank = True)
	pause_total = models.FloatField(null = True, blank = True)
	status = models.IntegerField(null = True, choices = STATUS_CHOICES, default = 1)

	def __unicode__(self):
		return "Field Name: " + str(self.field) + " Code: " + str(self.code) + ", Hour Cost: " +  str(self.rate_cost) + ", Description: " +  str(self.description)

class Employee(models.Model):
	LANGUAGE_CHOICES = (
		(1, 'pt-br'),
		(2, 'es'),
		(3, 'en'),
	)
	last_task = models.ForeignKey(Task,null = True, blank = True)
	user = models.OneToOneField(User)
	active = models.BooleanField(default = True)
	company_id = models.CharField(max_length = 10, blank = True, null = True)
	language = models.IntegerField(choices = LANGUAGE_CHOICES, default = 3)
	qr_code = models.CharField(max_length = 10, blank  = True, null = True)
	start_date = models.DateField(blank = True, null = True)
	hour_cost = models.FloatField(blank = True, null = True)
	contact_number = models.CharField(max_length = 14, blank = True)
	permission_level = models.IntegerField(choices = ((1, 'Driver'), (2, 'Manager')), default = 1)
	photo = models.URLField(max_length = 200, blank = True, null = True)
	notes = models.CharField(max_length = 250, null = True, blank = True)
	manager = models.ForeignKey('self', null = True, blank = True)

	def __unicode__(self):
		return  "First Name: " + str(self.user.first_name) + ", Last Name: " + str(self.user.last_name) + ", User ID: " + str(self.user.id) + ", ID: " + str(self.id)

class EmployeeWithdrawn(models.Model):
	employee = models.ForeignKey(Employee)
	date = models.DateField()

	def __unicode__(self):
		return "Date: " + str(self.date) + ", Name: " + str(self.employee.user.last_name)

class EmployeeAttendance(models.Model):
	employee = models.ForeignKey(Employee)
	date = models.DateField()
	hour_started = models.TimeField()
	hour_ended = models.TimeField(null = True, blank = True)
	signature = models.CharField(max_length = 5000, null = True, blank = True)


	def __unicode__(self):
		return "Employee: " + str(self.employee) + ", Date: " + str(self.date)

class Break(models.Model):
	BREAK_NUM = (
		(1, '0'),
		(2, '1'),
		(3, '2'),
		(4, '3'),
		(5, '4'),
		(6, '5'),
	)
	attendance = models.ForeignKey(EmployeeAttendance)
	lunch = models.BooleanField(default=False)
	start = models.TimeField()
	end = models.TimeField(null = True, blank = True)
	break_num = models.IntegerField(choices = BREAK_NUM, default=1)

	def __unicode__(self):
		return "Employee: " + str(self.attendance.employee.user.last_name) + ", start: " + str(self.start) + ", end: " + str(self.end) + ", break number: " + str(self.break_num)

class Qualification(models.Model):
	description = models.CharField(max_length = 50)

	def __unicode__(self):
		return "Description: " + str(self.description)

class Certification(models.Model):
	description = models.CharField(max_length = 50)
	year = models.IntegerField(null = True, blank = True)

	def __unicode__(self):
		return  "Description: " + str(self.description)

class EmployeeQualifications(models.Model):
	LEVEL_CHOICES = (
		(1, 'Low'),
		(2, 'Medium'),
		(3, 'High'),
	)
	employee = models.ForeignKey(Employee)
	qualification = models.ForeignKey(Qualification)
	level = models.IntegerField(choices = LEVEL_CHOICES)

	def __unicode__(self):
		return str(self.employee) +  ", Qualification: " + str(self.qualification.id) + ", Level: "+ str(self.level)

class EmployeeCertifications(models.Model):
	employee = models.ForeignKey(Employee)
	certification = models.ForeignKey(Certification)

	def __unicode__(self):
		return "Employee ID: " + str(self.employee.id) + ", Last Name: " + str(self.employee.user.last_name) + ", Certification ID: " + str(self.certification.id)

class MachineQualification(models.Model):
	machine = models.ForeignKey(Machine)
	qualification = models.ForeignKey(Qualification)
	qualification_required = models.IntegerField(choices = EmployeeQualifications.LEVEL_CHOICES)

	def __unicode__(self):
		return "Machine ID: " + str(self.machine.id) + ", Qualification ID: " + str(self.qualification) + ", Qualification level required: " +  str(self.qualification_required) + ", Machine QRcode: " + str(self.machine.qr_code)

class MachineCertification(models.Model):
	machine =  models.ForeignKey(Machine)
	certification = models.ForeignKey(Certification)

	def __unicode__(self):
		return "Machine ID: " + str(self.machine.id) + ", Certification ID:" +  str(self.certification.id) + ", Machine QRcode: " + str(self.machine.qr_code)

class ImplementQualification(models.Model):
	implement = models.ForeignKey(Implement)
	qualification = models.ForeignKey(Qualification)
	qualification_required = models.IntegerField(choices = EmployeeQualifications.LEVEL_CHOICES)

	def __unicode__(self):
		return "Implement ID: " + str(self.implement.id) + ", Qualification ID: " + str(self.qualification.id) + ", Qualification Required: " + str(self.qualification_required) + ", Implement QRcode: " + str(self.implement.qr_code)

class ImplementCertification(models.Model):
	implement = models.ForeignKey(Implement)
	certification =  models.ForeignKey(Certification)

	def __unicode__(self):
		return str(self.implement) + " " +  str(self.certification)

class FieldLocalization(models.Model):
	field = models.ForeignKey(Field)
	gps = models.ForeignKey(GPS)

	def __unicode__(self):

		return "Field: " + str(self.field.name) + ", GPS ID: " + str( self.gps)

class EmployeeLocalization(models.Model):
	employee = models.ForeignKey(Employee)
	latitude = models.FloatField()
	longitude = models.FloatField()
	e_time = models.DateTimeField()

	def __unicode__(self):
		return "Employee: " + str(self.employee.user.last_name) + ", Latitude: " +  str(self.latitude) + ", Longitude: " +  str(self.longitude) + ", Date: " + str(self.e_time)

class EmployeeTask(models.Model):
	employee = models.ForeignKey(Employee)
	task = models.ForeignKey(Task)
	start_time = models.DateTimeField(null = True, blank = True)
	end_time = models.DateTimeField(null = True, blank = True)
	hours_spent = models.FloatField(default = 0)

	def __unicode__(self):
		return "Employee ID: " + str(self.employee.id) + ", Task Begin: " +  str(self.start_time) + " Hours Spent: " +  str(self.hours_spent)

class MachineTask(models.Model):
	task = models.ForeignKey(Task)
	machine = models.ForeignKey(Machine)
	employee_task = models.ForeignKey(EmployeeTask)

	def __unicode__(self):
		return "Task ID: " + str(self.task.id) + ", Machine ID: " +  str(self.machine.id) + ", Employee Task ID:" +  str(self.employee_task.id)

class ImplementTask(models.Model):
	task = models.ForeignKey(Task)
	machine_task = models.ForeignKey(MachineTask)
	implement = models.ForeignKey(Implement)

	def __unicode__(self):
		return "Task ID: " + str(self.task.id) + ", Machine ID: " +  str(self.machine_task.id) + ", Implement:" +  str(self.implement.id)

class Appendix(models.Model):
	a_type =  models.CharField(max_length = 20)

	def __unicode__(self):
		return "Appendix: " + str(self.id) + ", Category: " + str(self.a_type)

class AppendixTask(models.Model):
	appendix = models.ForeignKey(Appendix)
	task = models.ForeignKey(Task)
	quantity = models.IntegerField()
	brand = models.CharField(max_length = 20)

	def __unicode__(self):
		return "Category: " + str(self.appendix.a_type) + ", Brand: " + str(self.brand)

class ServiceCategory(models.Model):
	service_category = models.CharField(max_length = 30)

	def __unicode__(self):
		return "Service Category: " + str(self.service_category)

class MachineService(models.Model):
	machine = models.ForeignKey(Machine)
	service = models.ForeignKey(ServiceCategory)
	description = models.CharField(max_length = 200)
	assigned_date = models.DateTimeField()
	expected_date = models.DateTimeField()
	accomplished_date = models.DateTimeField(null = True, blank = True)
	price = models.FloatField()

	def __unicode__(self):
		return "Description " + str(self.description) + ", Expected Date: " +  str(self.expected_date) + ", Price:  " +  str(self.price)

class ImplementService(models.Model):
	implement = models.ForeignKey(Implement)
	service = models.ForeignKey(ServiceCategory)
	description = models.CharField(max_length = 200)
	assigned_date = models.DateTimeField()
	expected_date = models.DateTimeField()
	accomplished_date = models.DateTimeField(null = True, blank = True)
	price = models.FloatField()

	def __unicode__(self):
		return "Description: " + str(self.description) + ", Expected Date: " + str(self.expected_date) + ", Price: " + str(self.price)

class Question(models.Model):
	NONE = 0
	MACHINE = 1
	IMPLEMENT = 2

	CATDEFAULT = 5

	QUESTION_CHOICES = (
		(1, 'Before Lunch Break'),
		(2, 'Post Lunch Pre Start'),
		(3, 'Post Lunch Start'),
		(4, 'End of Day Inspection'),
		(5, 'Default'),
	)
	REFERS_CHOICES = (
		(MACHINE, 'Machine'),
		(IMPLEMENT, 'Implement'),
	)
	description = models.CharField(max_length = 250)
	category = models.IntegerField(choices = QUESTION_CHOICES)
	refers = models.IntegerField(choices = REFERS_CHOICES)

	def __unicode__(self):
		return "Description: " + str(self.description)


class TranslatedQuestion(models.Model):
	SPANISH  = 1
	BRPORTUGUESE = 2 

	IDIOMS = (
		(SPANISH, 'es'),
		(BRPORTUGUESE, 'pt-br'),
	)

	question = models.ForeignKey(Question)
	description = models.CharField(max_length = 250)
	idiom = models.IntegerField(choices = IDIOMS, default = SPANISH)


	def __unicode__(self):
		return "Idiom: " + self.get_idiom_display() + " Description: " + self.description

class MachineChecklist(models.Model):
	question = models.ForeignKey(Question)
	qr_code = models.ForeignKey(Machine)
	employee = models.ForeignKey(Employee, null = True, blank = True)
	answer = models.BooleanField()
	note = models.CharField(max_length = 200,blank = True)
	date = models.DateTimeField()
	photo = models.URLField(max_length = 200, blank = True)

	def __unicode__(self):
		return "Machine: " + str(self.qr_code.manufacturer_model) + ", Answer: " + str(self.answer) + ", Note: " + str(self.note)


class ImplementChecklist(models.Model):
	question = models.ForeignKey(Question)
	qr_code = models.ForeignKey(Implement)
	employee = models.ForeignKey(Employee, null = True, blank = True)
	answer = models.BooleanField()
	note = models.CharField(max_length = 200, blank = True)
	date = models.DateTimeField()
	photo = models.URLField(max_length = 200, blank = True)

	def __unicode__(self):
		return "Answer: " + str(self.answer) + ", Note: " + str(self.note)
