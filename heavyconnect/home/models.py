from django.db import models
from django.contrib.auth.models import User


class Manufacturer(models.Model):
	name = models.CharField(max_length = 20)

	def __unicode__(self):
		return "Manafacturer: " + self.name

class ManufacturerModel(models.Model):
	manufacturer = models.ForeignKey(Manufacturer)
	model = models.CharField(max_length = 10)

	def __unicode__(self):
		return "Model: " + str(self.model) + ", Manufacturer: " + str(self.manufacturer)

class RepairShop(models.Model):
	name = models.CharField(max_length = 20)
	number =  models.CharField(max_length=14)
	address = models.CharField(max_length = 150)

	def __unicode__(self):
		return "Contact: " + str(self.name) + ", Phone Number: " + str(self.number) + ", Address: " + str(self.address)

class Shop(models.Model):
	name = models.CharField(max_length = 20)
	number = models.CharField(max_length = 14)
	address = models.CharField(max_length = 150)

	def __unicode__(self):
		return "Contact: " + str(self.name) + "\n" + "Phone Number: " + str(self.number) + "\n" + "Address: " + str(self.address)

class Machine(models.Model):
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
		(1, 'Ok'),
		(2, 'Attention'),
		(3, 'Broken'),
		(4, 'Quarantine'),
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
	base_cost = models.FloatField()
	m_type = models.CharField(max_length = 1, choices = (('T', 'Track'), ('W', 'Wheels'))) 
	front_tires = models.CharField(max_length = 20)														
	rear_tires = models.CharField(max_length = 20)
	steering = models.CharField(max_length = 1, choices = (('M', 'Manual'), ('G', 'GPS')))
	operator_station =  models.CharField(max_length = 1, choices = (('C', 'Cab'), ('O', 'Open')))
	status = models.IntegerField(choices = STATUS_CHOICES, null = True)
	hour_cost = models.FloatField()
	photo = models.URLField(max_length = 200)

	def __unicode__(self):
		return "QRcode: " + str(self.qr_code) + ", Model: " + str(self.manufacturer_model.model)

class Implement(models.Model):
	manufacturer_model = models.ForeignKey(ManufacturerModel)
	repair_shop = models.ForeignKey(RepairShop)
	shop = models.ForeignKey(Shop)
	nickname = models.CharField(max_length = 20)
	qr_code = models.CharField(max_length = 10)
	asset_number = models.CharField(max_length = 15)
	serial_number = models.CharField(max_length = 25)
	horse_power_req = models.IntegerField()
	hitch_capacity_req = models.IntegerField()
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
	photo = models.URLField(max_length = 200)

	def __unicode__(self):
		return "QRcode: " + str(self.qr_code) + ", Model: " + str(self.manufacturer_model.model)

class Employee(models.Model):
	LANGUAGE_CHOICES = (
		(1, 'pt-br'),
		(2, 'es'),
		(3, 'en'),
	)
	user = models.OneToOneField(User)
	company_id = models.CharField(max_length = 10)
	language = models.IntegerField(choices = LANGUAGE_CHOICES)
	qr_code = models.CharField(max_length = 10)
	start_date = models.DateField()
	hour_cost = models.FloatField()
	contact_number = models.CharField(max_length = 14)
	permission_level = models.IntegerField(choices = ((1, 'Driver'), (2, 'Manager')))
	photo = models.URLField(max_length = 200)

	def __unicode__(self):
		return  "User ID: " + str(self.user.id) + ", First Name: " + str(self.user.first_name) + ", Last Name: " + str(self.user.last_name)

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
	break_one = models.TimeField(null = True, blank = True)
	break_one_end = models.TimeField(null = True, blank = True)
	break_two = models.TimeField(null = True, blank = True)
	break_two_end = models.TimeField(null = True, blank = True)
	break_three = models.TimeField(null = True, blank = True)
	break_three_end = models.TimeField(null = True, blank = True)

	def __unicode__(self):
		return "Employee: " + str(self.employee) + ", Date: " + str(self.date)

class Qualification(models.Model):
	description = models.CharField(max_length = 50)

	def __unicode__(self):
		return "Description: " + str(self.description)

class Certification(models.Model):
	category = models.IntegerField()
	description = models.CharField(max_length = 50)

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

class Field(models.Model):
	name = models.CharField(max_length = 50)
	organic = models.BooleanField()
	size =  models.FloatField()

	def __unicode__(self):
		return "Name: " + str(self.name) + ", Organic: " +  str(self.organic) + ", Size: " +  str(self.size)

class GPS(models.Model):
	latitude = models.FloatField()
	longitude = models.FloatField()

	def __unicode__(self):
		return "Latitude: " +str(self.latitude) + " " +  "Longitude: " +str(self.longitude)

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

class TaskCategory(models.Model):
	description = models.CharField(max_length = 30)

	def __unicode__(self):
		return "ID: " + str(self.id) + ", Category: " + str(self.description)

class Task(models.Model):
	APPROVAL_CHOICES = (
		(1, 'Approved'),
		(2, 'Denied'),
		(3, 'Pending'),
	)
	field = models.ForeignKey(Field)
	category = models.ForeignKey(TaskCategory)
	rate_cost = models.FloatField()
	hours_spent = models.FloatField()
	hours_prediction = models.FloatField()
	description =  models.CharField(max_length = 500)
	passes = models.IntegerField()
	date = models.DateTimeField()
	accomplished = models.BooleanField()
	approval = models.IntegerField(choices = APPROVAL_CHOICES)

	def __unicode__(self):
		return "Field Name: " + str(self.field.name) + " Category: " + str(self.category.description) + ", Hour Cost: " +  str(self.rate_cost) + ", Description: " +  str(self.description)

class EmployeeTask(models.Model):
	employee = models.ForeignKey(Employee)
	task = models.ForeignKey(Task)
	task_init = models.DateTimeField()
	hours_spent = models.FloatField()
	substitution = models.BooleanField()

	def __unicode__(self):
		return "Employee ID: " + str(self.employee.id) + ", Task Begin: " +  str(self.task_init) + " Hours Spent: " +  str(self.hours_spent)

class TaskImplementMachine(models.Model):
	task = models.ForeignKey(Task)
	machine = models.ForeignKey(Machine)
	implement = models.ForeignKey(Implement)
	machine = models.BooleanField()

	def __unicode__(self):
		return "Task ID: " + str(self.task.id) + ", Machine ID: " +  str(self.machine.id) + ", Implement ID:" +  str(self.implement.id)

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

class Service(models.Model):
	category = models.ForeignKey(ServiceCategory)
	date = models.DateTimeField()
	done = models.BooleanField()

	def __unicode__(self):
		return str(self.category) + ", Date: " +  str(self.date) + ", Done: " +  str(self.done)

class MachineService(models.Model):
	machine = models.ForeignKey(Machine)
	service = models.ForeignKey(Service)
	description = models.CharField(max_length = 200)
	done = models.BooleanField()
	expected_date = models.DateTimeField()
	price = models.FloatField()

	def __unicode__(self):
		return "Description " + str(self.description) + ", Expected Date: " +  str(self.expected_date) + ", Price:  " +  str(self.price) + ", Done: " +  str(self.done)

class ImplementService(models.Model):
	implement = models.ForeignKey(Implement)
	service = models.ForeignKey(Service)
	description = models.CharField(max_length = 200)
	expected_date = models.DateTimeField()
	done = models.BooleanField()
	price = models.FloatField()

	def __unicode__(self):
		return "Description: " + str(self.description) + ", Expected Date: " + str(self.expected_date) + ", Price: " + str(self.price) + ", Done " + str(self.done) 

class Question(models.Model):
	description = models.CharField(max_length = 250)
	category = models.IntegerField()
	refers = models.IntegerField(choices = ((1, 'Machine'), (2, 'Implement')))

	def __unicode__(self):
		return "Description: " + str(self.description) + ", category: " + str(self.category) + ", refers: " + str(self.refers)


class MachineChecklist(models.Model):
	question = models.ForeignKey(Question)
	qrCode = models.ForeignKey(Machine)
	answer = models.BooleanField()
	note = models.CharField(max_length = 200,blank = True)
	date = models.DateTimeField()
	photo = models.URLField(max_length = 200, blank = True)

	def __unicode__(self):
		return "Answer: " + str(self.answer) + ", note: " + str(self.note)


class ImplementChecklist(models.Model):
	question = models.ForeignKey(Question)
	qrCode = models.ForeignKey(Implement)
	answer = models.BooleanField()
	note = models.CharField(max_length = 200, blank = True)
	date = models.DateTimeField()
	photo = models.URLField(max_length = 200, blank = True)

	def __unicode__(self):
		return "Answer: " + str(self.answer) + ", note: " + str(self.note)




