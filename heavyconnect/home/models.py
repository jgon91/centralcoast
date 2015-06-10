from django.db import models
from django.contrib.auth.models import User


class Manufacturer(models.Model):
	name = models.CharField(max_length = 20)

	def __unicode__(self):
		return self.name

class ManufacturerModel(models.Model):
	manufacturer_id = models.ForeignKey(Manufacturer)
	model = models.CharField(max_length = 10)

	def __unicode__(self):
		return str(self.model) + " : " + str(self.manufacturer_id)

class RepairShop(models.Model):
	contact_name = models.CharField(max_length = 20)
	contact_number =  models.CharField(max_length=14)
	contact_address = models.CharField(max_length = 150)

	def __unicode__(self):
		return "Contact: " + str(self.contact_name) + "\n" + "Phone Number: " + str(self.contact_number) + "\n" + "Address: " + str(self.contact_address)

class Shop(models.Model):
	contact_name = models.CharField(max_length = 20)
	contact_number = models.CharField(max_length=14)
	contact_address = models.CharField(max_length = 150)

	def __unicode__(self):
		return "Contact: " + str(self.contact_name) + "\n" + "Phone Number: " + str(self.contact_number) + "\n" + "Address: " + str(self.contact_address)

class Machine(models.Model):
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
	manufacturer_model_id = models.ForeignKey(ManufacturerModel)
	repair_shop_id = models.ForeignKey(RepairShop)
	shop_id = models.ForeignKey(Shop)
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
	m_type = models.CharField(max_length = 1, choices = (('T', 'Track'), ('W', 'Wheels')), null = True) # at the moment if there is a null = true, it is to allow changes after the db has been created
	front_tires = models.CharField(max_length = 20)														
	rear_tires = models.CharField(max_length = 20)
	steering = models.CharField(max_length = 1, choices = (('M', 'Manual'), ('G', 'GPS')), null = True)
	operator_station =  models.CharField(max_length = 1, choices = (('C', 'Cab'), ('O', 'Open')), null = True)
	status = models.IntegerField(choices = ((1, 'Ok'), (2, 'Attention'), (3, 'Broken'), (4, 'Quarantine')), null = True)
	hour_cost = models.FloatField()
	photo = models.URLField(max_length=200)

	def __unicode__(self):
		return "QRcode: " + str(self.qr_code) + " Year of Purchased: " + str(self.year_purchased)

class Implement(models.Model):
	manufacturer_model_id = models.ForeignKey(ManufacturerModel)
	repair_shop_id = models.ForeignKey(RepairShop)
	shop_id = models.ForeignKey(Shop)
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
	status = models.IntegerField(choices = ((1, 'Ok'), (2, 'Attention'), (3, 'Broken'), (4, 'Quarantine')), null = True)
	photo = models.URLField(max_length=200)

	def __unicode__(self):
		return "QRcode: " + str(self.qr_code) + " Year of Purchased: " + str(self.year_purchased)

class Employee(models.Model):
	user = models.OneToOneField(User)
	company_id = models.CharField(max_length = 10)
	qr_code = models.CharField(max_length = 10)
	start_date = models.DateField()
	hour_cost = models.FloatField()
	contact_number = models.CharField(max_length=14, null = True)
	permission_level = models.IntegerField(choices = ((1, 'Driver'), (2, 'Manager')), null = True)
	photo = models.URLField(max_length=200)

	def __unicode__(self):
		return str(self.user.first_name) + " : " + str(self.user.last_name)


class EmployeeAttendance(models.Model):
	employee_id = models.ForeignKey(Employee)
	date = models.DateField()
	hour_started = models.TimeField()
	hour_ended = models.TimeField()
	morning_break = models.TimeField()
	morning_break_end = models.TimeField()
	afternoon_break = models.TimeField()
	afternoon_break_end = models.TimeField()
	evening_break = models.TimeField()
	evening_break_end = models.TimeField()

	def __unicode__(self):
		return str(self.date)

class Qualification(models.Model):
	description = models.CharField(max_length = 50)

	def __unicode__(self):
		return str(self.description)

class Certification(models.Model):
	category = models.IntegerField()
	description = models.CharField(max_length = 50)

	def __unicode__(self):
		return str(self.description)

class EmployeeQualifications(models.Model):
	employee_id =  models.ForeignKey(Employee)
	qualification_id =  models.ForeignKey(Qualification)
	level = models.IntegerField(choices = ((1, 'Low'), (2, 'Medium'), (3, 'High')), null = True)

	def __unicode__(self):
		return str(self.employee_id) +  " " + str(self.qualification_id.id) + str(self.level)

class EmployeeCertifications(models.Model):
	employee_id = models.ForeignKey(Employee)
	certification_id = models.ForeignKey(Certification)

	def __unicode__(self):
		return str(self.employee_id.id) + str(self.certification_id.id)

class MachineQualification(models.Model):
	machine_id = models.ForeignKey(Machine)
	qualification_id = models.ForeignKey(Qualification)
	qualification_required = models.IntegerField(choices = ((1, 'Low'), (2, 'Medium'), (3, 'High')), null = True)

	def __unicode__(self):
		return str(self.machine_id) + " " + str(self.qualification_id) + " " +  str(self.qualification_required)

class MachineCertification(models.Model):
	machine_id =  models.ForeignKey(Machine)
	certification_id = models.ForeignKey(Certification)

	def __unicode__(self):
		return str(self.machine_id.id) + " " +  str(self.certification_id)

class ImplementQualification(models.Model):
	implement_id = models.ForeignKey(Implement)
	qualification_id = models.ForeignKey(Qualification)
	qualification_required = models.IntegerField(choices = ((1, 'Low'), (2, 'Medium'), (3, 'High')), null = True)

	def __unicode__(self):
		return str(self.implement_id) + " " +  str(self.qualification_id) + " " +  str(self.qualification_required)

class ImplementCertification(models.Model):
	implement_id = models.ForeignKey(Implement)
	certification_id =  models.ForeignKey(Certification)

	def __unicode__(self):
		return str(self.implement_id) + " " +  str(self.certification_id)

class Field(models.Model):
	name = models.CharField(max_length = 50)
	organic = models.BooleanField()
	size =  models.FloatField()

	def __unicode__(self):
		return str(self.name) + " " +  str(self.organic) + " " +  str(self.size)

class GPS(models.Model):
	latitude = models.CharField(max_length = 15)
	longitude = models.CharField(max_length = 15)

	def __unicode__(self):
		return "Lati: " +str(self.latitude) + " " +  "Long: " +str(self.longitude)

class FieldLocalization(models.Model):
	field_id = models.ForeignKey(Field)
	gps_id = models.ForeignKey(GPS)

	def __unicode__(self):
		return str(self.field_id) + " " + str( self.gps_id)

class EmployeeLocalization(models.Model):
	employee_id = models.ForeignKey(Employee)
	gps_id = models.ForeignKey(GPS)
	e_time = models.DateTimeField()

	def __unicode__(self):
		return str(self.employee_id) + " " +  str(self.gps_id) + " " +  str(self.e_time)

class Task(models.Model):
	field_id = models.ForeignKey(Field)
	t_type = models.CharField(max_length = 100)
	rate_cost = models.FloatField()
	hours_spent = models.FloatField()
	hours_prediction = models.FloatField()
	description =  models.CharField(max_length = 500)
	passes = models.IntegerField()
	date = models.DateTimeField()
	accomplished = models.BooleanField()
	approval = models.BooleanField()

	def __unicode__(self):
		return str(self.field_id) + " " +  str(self.rate_cost) + " " +  str(self.description)

class EmployeeTask(models.Model):
	employee_id = models.ForeignKey(Employee)
	task_id = models.ForeignKey(Task)
	task_init = models.DateField()
	hours_spent = models.FloatField()
	substitution = models.BooleanField()

	def __unicode__(self):
		return str(self.employee_id) + " " +  str(self.task_init) + " " +  str(self.hours_spent)

class TaskImplementMachine(models.Model):
	task_id = models.ForeignKey(Task)
	machine_id = models.ForeignKey(Machine)
	implement_id = models.ForeignKey(Implement)
	machine = models.BooleanField()

	def __unicode__(self):
		return str(self.task_id) + " " +  str(self.machine_id) + " " +  str(self.implement_id)

class Appendix(models.Model):
	a_type =  models.CharField(max_length = 20)

	def __unicode__(self):
		return str(self.id) + " " + str(self.a_type)

class AppendixTask(models.Model):
	appendix_id = models.ForeignKey(Appendix)
	task_id = models.ForeignKey(Task)
	quantity = models.IntegerField()
	brand = models.CharField(max_length = 20)

	def __unicode__(self):
		return str(self.appendix_id) + " " + str(self.brand)

class ServiceCategory(models.Model):
	service_category = models.CharField(max_length = 30)

	def __unicode__(self):
		return str(self.service_category)

class Service(models.Model):
	category_id = models.ForeignKey(ServiceCategory)
	date = models.DateTimeField()
	done = models.BooleanField()

	def __unicode__(self):
		return str(self.category_id) + " " +  str(self.date) + " " +  str(self.done)

class MachineService(models.Model):
	machine_id = models.ForeignKey(Machine)
	service_id = models.ForeignKey(Service)
	description = models.CharField(max_length = 200)
	done = models.BooleanField()
	expected_date = models.DateTimeField()
	price = models.FloatField()

	def __unicode__(self):
		return str(self.description) + " " +  str(self.expected_date) + " " +  str(self.price) + " " +  str(self.done)

class ImplementService(models.Model):
	implement_id = models.ForeignKey(Implement)
	service_id = models.ForeignKey(Service)
	description = models.CharField(max_length = 200)
	expected_date = models.DateTimeField()
	done = models.BooleanField()
	price = models.FloatField()

	def __unicode__(self):
		return self.description + "Data: " + str(self.expected_date)



