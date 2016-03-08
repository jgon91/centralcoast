from django.db import models
from django.contrib.auth.models import User
import base64

class Manufacturer(models.Model):
	name = models.CharField(max_length = 20)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Manafacturer: " + self.name

class ManufacturerModel(models.Model):
	manufacturer = models.ForeignKey(Manufacturer)
	model = models.CharField(max_length = 30)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return str(self.manufacturer) + ", Model: " + str(self.model)

class RepairShop(models.Model):
	name = models.CharField(max_length = 20)
	number =  models.CharField(max_length=14)
	address = models.CharField(max_length = 150)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Contact: " + str(self.name) + ", Address: " + str(self.address) + ", Phone Number: " + str(self.number)

class Shop(models.Model):
	name = models.CharField(max_length = 20)
	number = models.CharField(max_length = 14)
	address = models.CharField(max_length = 150)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Contact: " + str(self.name) + ", Address: " + str(self.address) + ", Phone Number: " + str(self.number)


class EquipmentCategory(models.Model):
	name = models.CharField(max_length = 25)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "name: " + str(self.name)

class EquipmentType(models.Model):
	category = models.ForeignKey(EquipmentCategory)
	name = models.CharField(max_length = 25)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Name: " + str(self.name) + ", Category: " + str(self.category.name)

class GPS(models.Model):
	latitude = models.FloatField()
	longitude = models.FloatField()
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

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
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

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
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

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
	repair_shop = models.ForeignKey(RepairShop, null = True, blank = True)
	shop = models.ForeignKey(Shop, null = True, blank = True)
	nickname = models.CharField(max_length = 20)
	qr_code = models.CharField(max_length = 10, null = True, blank = True)
	asset_number = models.CharField(max_length = 15)
	serial_number = models.CharField(max_length = 25, null = True, blank = True)
	horsepower = models.IntegerField(null = True, blank = True)
	hitch_capacity = models.IntegerField(null = True, blank = True)
	hitch_category = models.IntegerField(choices = HITCH_CHOICES, null = True, blank = True)
	drawbar_category = models.IntegerField(choices = DRAWBAR_CHOICES, null = True, blank = True)
	speed_range_min = models.FloatField(blank = True, null = True)
	speed_range_max = models.FloatField(blank = True, null = True)
	year_purchased = models.IntegerField(null = True, blank = True)
	engine_hours = models.IntegerField(null = True, blank = True)
	service_interval = models.IntegerField(null = True, blank = True)
	base_cost = models.FloatField(blank = True, null = True)
	m_type = models.CharField(max_length = 1, choices = MTYPE_CHOICES, blank = True, null = True)
	front_tires = models.CharField(max_length = 20, blank = True, null = True)
	rear_tires = models.CharField(max_length = 20, blank = True, null = True)
	steering = models.CharField(max_length = 1, choices = STEERING_CHOICES, blank = True, null = True)
	operator_station = models.CharField(max_length = 1, choices = OPERATORSTATION_CHOICES, blank = True, null = True)
	status = models.IntegerField(choices = STATUS_CHOICES, default = 1)
	hour_cost = models.FloatField(blank = True, null = True)
	photo = models.URLField(max_length = 200, blank = True, null = True)
	photo1 = models.URLField(max_length = 200,blank = True, null = True)
	photo2 = models.URLField(max_length = 200, blank = True, null = True)
	note = models.CharField(max_length = 250, blank = True, null = True)
	beacon = models.ForeignKey(Beacon, blank = True, null = True) #DEMO
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Manufacturer: " + str(self.manufacturer_model.manufacturer.name) + ", Model: " + str(self.manufacturer_model.model) + ", QRcode: " + str(self.qr_code)

class Implement(models.Model):
	manufacturer_model = models.ForeignKey(ManufacturerModel)
	repair_shop = models.ForeignKey(RepairShop, null = True, blank = True)
	shop = models.ForeignKey(Shop, null = True, blank = True)
	nickname = models.CharField(max_length = 20)
	qr_code = models.CharField(max_length = 10, null = True, blank = True)
	asset_number = models.CharField(max_length = 15)
	serial_number = models.CharField(max_length = 25)
	horse_power_req = models.IntegerField(null = True, blank = True)
	hitch_capacity_req = models.IntegerField(null = True, blank = True)
	hitch_category = models.IntegerField(choices = Machine.HITCH_CHOICES, null = True, blank = True)
	drawbar_category = models.IntegerField(choices = Machine.DRAWBAR_CHOICES, null = True, blank = True)
	speed_range_min = models.FloatField(null = True, blank = True)
	speed_range_max = models.FloatField(null = True, blank = True)
	year_purchased = models.IntegerField(null = True, blank = True)
	implement_hours = models.IntegerField(null = True, blank = True)
	service_interval = models.IntegerField(null = True, blank = True)
	base_cost = models.FloatField(null = True, blank = True)
	hour_cost = models.FloatField(null = True, blank = True)
	status = models.IntegerField(choices = Machine.STATUS_CHOICES)
	#equipment_type = models.ForeignKey(EquipmentType)
	photo = models.URLField(max_length = 200, null = True, blank = True)
	photo1 = models.URLField(max_length = 200, null = True, blank = True)
	photo2 = models.URLField(max_length = 200, null = True, blank = True)
	note = models.CharField(max_length = 250, null = True, blank = True)
	beacon = models.ForeignKey(Beacon, blank = True, null = True) #DEMO
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Manufacturer: " + str(self.manufacturer_model.manufacturer.name) + ", Model: " + str(self.manufacturer_model.model) + ", QRcode: " + str(self.qr_code)

class Field(models.Model):
	name = models.CharField(max_length = 50)
	organic = models.BooleanField()
	size =  models.FloatField()
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Name: " + str(self.name) + ", Organic: " +  str(self.organic) + ", Size: " +  str(self.size)

class TaskCategory(models.Model):
	description = models.CharField(max_length = 30)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "ID: " + str(self.id) + ", Category: " + str(self.description)

class TaskCode(models.Model):
	name = models.CharField(max_length = 100)
	category = models.ForeignKey(TaskCategory)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "ID: " + str(self.id) + ", Name: " + str(self.name) + ", Category" + str(self.category)

class Employee(models.Model):
	LANGUAGE_CHOICES = (
		(1, 'pt-br'),
		(2, 'es'),
		(3, 'en-us'),
	)
	user = models.OneToOneField(User)
	active = models.BooleanField(default = True)
	company_id = models.CharField(max_length = 10, blank = True, null = True)
	language = models.IntegerField(choices = LANGUAGE_CHOICES, default = 3)
	qr_code = models.CharField(max_length = 10, blank  = True, null = True)
	start_date = models.DateField(blank = True, null = True)
	hour_cost = models.FloatField(blank = True, null = True)
	contact_number = models.CharField(max_length = 14, blank = True)
	permission_level = models.IntegerField(choices = ((1, 'Driver'), (2, 'Manager'), (3, 'Shop')), default = 1)
	notes = models.CharField(max_length = 250, null = True, blank = True)
	manager = models.ForeignKey('self', null = True, blank = True)
	teamManager = models.BooleanField(default = False)
	photoEmployee = models.ImageField(upload_to='employee', default='employee/no.jpg')
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return  "First Name: " + str(self.user.first_name) + ", Last Name: " + str(self.user.last_name) + ", User ID: " + str(self.user.id) + ", ID: " + str(self.id) + " Team Manager :" + str(self.teamManager)

class Group(models.Model):
	name = models.CharField(max_length = 20)
	creator = models.ForeignKey(Employee)
	date = models.DateField()
	permanent = models.BooleanField(default = False)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Creator: " + str(self.creator) + ", DateField: " + str(self.date) + ", Name: " + str(self.name) + ", ID Group: " + str(self.id)


class EmployeeAttendance(models.Model):
	employee = models.ForeignKey(Employee)
	date = models.DateField()
	hour_started = models.TimeField()
	hour_ended = models.TimeField(null = True, blank = True)
	signature = models.CharField(max_length = 5000, null = True, blank = True)
	group = models.ForeignKey(Group, null = True, blank = True)
	edited = models.BooleanField(default = False)
	hours_worked = models.TimeField(null = True, blank = True)
	declined = models.BooleanField(default = False)
	manager_rejected = models.BooleanField(default = False)
	manager_approved = models.BooleanField(default = False)
	manager = models.CharField(default = "", max_length = 5000, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Employee: " + str(self.employee) + ", Date: " + str(self.date) + ", AttendanceID: " + str(self.id) + ", Worked: " + str(self.hours_worked)

class Task(models.Model):
	STATUS_CHOICES = (
		(1, 'Pending'),
		(2, 'Approved'),
		(3, 'Denied'),
		(4, 'Ongoing'),
		(5, 'Paused'),
		(6, 'Finished'),
	)
	attendance = models.ForeignKey(EmployeeAttendance, null=True)
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
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Field Name: " + str(self.field) + " Code: " + str(self.code) + ", Hour Cost: " +  str(self.rate_cost) + ", Description: " +  str(self.description)


class EmployeeWithdrawn(models.Model):
	employee = models.ForeignKey(Employee)
	date = models.DateField()
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Date: " + str(self.date) + ", Name: " + str(self.employee.user.last_name)


class GroupParticipant(models.Model):
	group = models.ForeignKey(Group)
	participant = models.ForeignKey(Employee)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Group: " + str(self.group) + ", participant: " + str(self.participant)



class Break(models.Model):
	attendance = models.ForeignKey(EmployeeAttendance)
	lunch = models.BooleanField()
	edited = models.BooleanField(default = False)
	start = models.TimeField()
	end = models.TimeField(null = True, blank = True)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Employee: " + str(self.attendance.employee.user.last_name) + ", start: " + str(self.start) + ", end: " + str(self.end)

class Qualification(models.Model):
	description = models.CharField(max_length = 50)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Description: " + str(self.description)

class Certification(models.Model):
	description = models.CharField(max_length = 50)
	year = models.IntegerField(null = True, blank = True)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

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
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return str(self.employee) +  ", Qualification: " + str(self.qualification.id) + ", Level: "+ str(self.level)

class EmployeeCertifications(models.Model):
	employee = models.ForeignKey(Employee)
	certification = models.ForeignKey(Certification)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Employee ID: " + str(self.employee.id) + ", Last Name: " + str(self.employee.user.last_name) + ", Certification ID: " + str(self.certification.id)

class MachineQualification(models.Model):
	machine = models.ForeignKey(Machine)
	qualification = models.ForeignKey(Qualification)
	qualification_required = models.IntegerField(choices = EmployeeQualifications.LEVEL_CHOICES)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Machine ID: " + str(self.machine.id) + ", Qualification ID: " + str(self.qualification) + ", Qualification level required: " +  str(self.qualification_required) + ", Machine QRcode: " + str(self.machine.qr_code)

class MachineCertification(models.Model):
	machine =  models.ForeignKey(Machine)
	certification = models.ForeignKey(Certification)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Machine ID: " + str(self.machine.id) + ", Certification ID:" +  str(self.certification.id) + ", Machine QRcode: " + str(self.machine.qr_code)

class ImplementQualification(models.Model):
	implement = models.ForeignKey(Implement)
	qualification = models.ForeignKey(Qualification)
	qualification_required = models.IntegerField(choices = EmployeeQualifications.LEVEL_CHOICES)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Implement ID: " + str(self.implement.id) + ", Qualification ID: " + str(self.qualification.id) + ", Qualification Required: " + str(self.qualification_required) + ", Implement QRcode: " + str(self.implement.qr_code)

class ImplementCertification(models.Model):
	implement = models.ForeignKey(Implement)
	certification =  models.ForeignKey(Certification)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return str(self.implement) + " " +  str(self.certification)

class FieldLocalization(models.Model):
	field = models.ForeignKey(Field)
	gps = models.ForeignKey(GPS)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):

		return "Field: " + str(self.field.name) + ", GPS ID: " + str( self.gps)

class EmployeeLocalization(models.Model):
	employee = models.ForeignKey(Employee)
	latitude = models.FloatField()
	longitude = models.FloatField()
	e_time = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Employee: " + str(self.employee.user.last_name) + ", Latitude: " +  str(self.latitude) + ", Longitude: " +  str(self.longitude) + ", Date: " + str(self.e_time)

class EmployeeTask(models.Model):
	employee = models.ForeignKey(Employee)
	task = models.ForeignKey(Task)
	start_time = models.DateTimeField(null = True, blank = True)
	end_time = models.DateTimeField(null = True, blank = True)
	hours_spent = models.FloatField(default = 0)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Employee ID: " + str(self.employee.id) + ", Task Begin: " +  str(self.start_time) + " Hours Spent: " +  str(self.hours_spent)

class MachineTask(models.Model):
	task = models.ForeignKey(Task)
	machine = models.ForeignKey(Machine)
	employee_task = models.ForeignKey(EmployeeTask)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Task ID: " + str(self.task.id) + ", Machine ID: " +  str(self.machine.id) + ", Employee Task ID:" +  str(self.employee_task.id)

class ImplementTask(models.Model):
	task = models.ForeignKey(Task)
	machine_task = models.ForeignKey(MachineTask)
	implement = models.ForeignKey(Implement)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Task ID: " + str(self.task.id) + ", Machine ID: " +  str(self.machine_task.id) + ", Implement:" +  str(self.implement.id)

class Appendix(models.Model):
	a_type =  models.CharField(max_length = 20)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Appendix: " + str(self.id) + ", Category: " + str(self.a_type)

class AppendixTask(models.Model):
	appendix = models.ForeignKey(Appendix)
	task = models.ForeignKey(Task)
	quantity = models.IntegerField()
	brand = models.CharField(max_length = 20)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Category: " + str(self.appendix.a_type) + ", Brand: " + str(self.brand)

class ServiceCategory(models.Model):
	service_category = models.CharField(max_length = 30)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

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
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

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
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Description: " + str(self.description) + ", Expected Date: " + str(self.expected_date) + ", Price: " + str(self.price)

class Question(models.Model):
	NONE = 0
	MACHINE = 1
	IMPLEMENT = 2
	EMPLOYEE = 3

	CATDEFAULT = 5

	QUESTION_CHOICES = (
		(1, 'Default'),
		(2, 'Before Lunch Break'),
		(3, 'Post Lunch Pre Start'),
		(4, 'Post Lunch Start'),
		(5, 'End of Day Inspection'),
		(6, 'End of shift'),
	)
	REFERS_CHOICES = (
		(MACHINE, 'Machine'),
		(IMPLEMENT, 'Implement'),
		(EMPLOYEE, 'Employee'),
	)
	description = models.CharField(max_length = 250)
	category = models.IntegerField(choices = QUESTION_CHOICES)
	refers = models.IntegerField(choices = REFERS_CHOICES)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

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
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)


	def __unicode__(self):
		return "Idiom: " + self.get_idiom_display() + " Description: " + self.description

class MachineChecklist(models.Model):
	question = models.ForeignKey(Question)
	qr_code = models.ForeignKey(Machine)
	employee = models.ForeignKey(Employee, null = True, blank = True)
	answer = models.BooleanField()
	note = models.CharField(max_length = 200,blank = True)
	date = models.DateTimeField()
	photo = models.TextField(max_length = 550000,blank = True)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def set_data(self, data):
		self.photo = base64.encodestring(data)

	def get_data(self):
 		return base64.decodestring(self.photo)

	def __unicode__(self):
		return "ID: " + str(self.id) + " Machine: " + str(self.qr_code.manufacturer_model) + ", Answer: " + str(self.answer) + ", Note: " + str(self.note) +', Date: '+ str(self.date)

class EmployeeAttendanceChecklist(models.Model):
	question = models.ForeignKey(Question)
	attendance = models.ForeignKey(EmployeeAttendance)
	answer = models.CharField(max_length = 200, blank = True)

	def __unicode__(self):
		return "ID: " + str(self.id) + " Answer: " + str(self.answer) + ", Question: " + str(self.question.description) + ", Attendance: " + str(self.attendance.employee)


class ImplementChecklist(models.Model):
	question = models.ForeignKey(Question)
	qr_code = models.ForeignKey(Implement)
	employee = models.ForeignKey(Employee, null = True, blank = True)
	answer = models.BooleanField()
	note = models.CharField(max_length = 200, blank = True)
	date = models.DateTimeField()
	photo = models.TextField(blank = True)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def set_data(self, data):
		self.photo = base64.encodestring(data)

	def get_data(self):
		return base64.decodestring(self.photo)

	def __unicode__(self):
		return "Answer: " + str(self.answer) + ", Note: " + str(self.note)

class TimeKeeperRules(models.Model):
	hour = models.TimeField()
	breaks = models.IntegerField()
	lunchs = models.IntegerField()
	lunchBool = models.BooleanField() #if ti is required to ask about the lunch
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "ID: " + str(self.id) + ", Hours: " + str(self.hour) + ", Breaks: " + str(self.breaks) + ", Lunch: " +  str(self.lunchs) + ", LunchBool: " + str(self.lunchBool)


class AttendanceChecklist(models.Model):
	QUESTION_CHOICES = (
		(1, 'Always'),
		(2, 'Less lunch than Expected'),
		(3, 'Less Breaks than Expected'),
		(4, 'Optional Lunch'),
	)
	category = models.IntegerField(choices = QUESTION_CHOICES)
	description = models.CharField(max_length = 2000)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Id: " + str(self.id) + ", category: " + str(self.category) + ", description: " + str(self.description)

class ConfirmationCheck(models.Model):
	question = models.ForeignKey(AttendanceChecklist)
	attendance = models.ForeignKey(EmployeeAttendance) #It has date, employee
	answer = models.BooleanField()
	note = models.CharField(max_length = 200, blank = True)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return "Id: " + str(self.id) + ", question: " + str(self.question)

class CompanyStatus(models.Model):
	active = models.BooleanField(default = True)
	employ_limit = models.IntegerField(default = 10)

	def __unicode__(self):
		return "Active: " + str(self.active) + ", Limit: " + str(self.employ_limit)
