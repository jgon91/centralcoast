from django.db import models
from django.contrib.auth.models import User

class Manufacturer(models.Model):
	name = models.CharField(max_length = 20)

	def __unicode__(self):
		return self.name

class ManufacturerModel(models.Model):
	manufacturer_id = models.IntegerField
	model = models.ForeignKey(Manufacturer)

	def __unicode__(self):
		return self.model + self.manufacturer_id

class RepairShop(models.Model):
	contact_name = models.CharField(max_length = 20)
	contact_number = models.IntegerField()
	contact_address = models.CharField(max_length = 150)

	def __unicode__(self):
		return "Contact: " + self.contact_name + "\n" + "Phone Number: " + self.contact_number + "\n" + "Address: " + self.contact_address

class Shop(models.Model):
	contact_name = models.CharField(max_length = 20)
	contact_number = models.IntegerField()
	contact_address = models.CharField(max_length = 150)

	def __unicode__(self):
		return "Contact: " + self.contact_name + "\n" + "Phone Number: " + self.contact_number + "\n" + "Address: " + self.contact_address

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
	m_type = (('Track', 'T'), ('Wheels', 'W'))
	front_tires = models.CharField(max_length = 20)
	rear_tires = models.CharField(max_length = 20)
	steering = (('Manual', 'M'), ('GPS', 'G'))
	operator_station = (('Cab', 'C'), ('Open', 'O'))
	status = (('Ok', 1), ('Attention', 2), ('Broken', 3), ('Quarantine', 4))
	hour_cost = models.FloatField()
	photo = models.URLField(max_length=200)

	def __unicode__(self):
		return "QRcode: " + self.qr_code + " Year of Purchased: " + year_purchased

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
	implement_status = (('Ok', 1), ('Attention', 2), ('Broken', 3), ('Quarantine', 4))
	photo = models.URLField(max_length=200)

	def __unicode__(self):
		return "QRcode: " + self.qr_code + " Year of Purchased: " + year_purchased

class Employee(models.Model):
	user = models.OneToOneField(User)
	company_id = models.CharField(max_length = 10)
	qr_code = models.CharField(max_length = 10)
	start_date = models.DateField()
	hour_cost = models.FloatField()
	permission_level = (('Driver', 1), ('Manager', 2))
	photo = models.URLField(max_length=200)

	def __unicode__(self):
		return self.first_name + " : " + self.user.first_name


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
		return self.e_date

class Qualification(models.Model):
	description = models.CharField(max_length = 50)

	def __unicode__(self):
		return self.description 

class Certification(models.Model):
	category = models.IntegerField()
	description = models.CharField(max_length = 50)

class EmployeeQualifications(models.Model):
	employee_id =  models.ForeignKey(Employee)
	qualification_id =  models.ForeignKey(Qualification)
	level = (('Low', 1), ('Medium', 2), ('High', 3))

	def __unicode__(self):
		return self.employee_id + qualification_id + q_level

class EmployeeCertifications(models.Model):
	employee_id = models.ForeignKey(Employee)
	certification_id = models.ForeignKey(Certification)

	def __unicode__(self):
		return self.employee_id + certification_id

class MachineQualification(models.Model):
	machine_id = models.ForeignKey(Machine)
	qualification_id = models.ForeignKey(Qualification)
	qualification_required = models.IntegerField()

	def __unicode__(self):
		return self.Machine_id + self.qualification_id + qualification_required

class MachineCertification(models.Model):
	machine_id =  models.ForeignKey(Machine)
	certification_id = models.ForeignKey(Certification)

	def __unicode__(self):
		return self.Machine_id + self.certification_id

class ImplementQualification(models.Model):
	implement_id = models.ForeignKey(Implement)
	qualification_id = models.ForeignKey(Qualification)
	qualification_required = models.IntegerField()

	def __unicode__(self):
		return self.implement_id + self.qualification_id + qualification_required

class ImplementCertification(models.Model):
	implement_id = models.ForeignKey(Implement)
	certification_id =  models.ForeignKey(Certification)

	def __unicode__(self):
		return self.implement_id + self.certification_id

class Field(models.Model):
	name = models.CharField(max_length = 50)
	organic = models.BooleanField()
	size =  models.FloatField()

	def __unicode__(self):
		return self.name + self.organic + self.size

class GPS(models.Model):
	latitude = models.CharField(max_length = 15)
	longitude = models.CharField(max_length = 15)

	def __unicode__(self):
		return self.latitude + self.longitude

class FieldLocalization(models.Model):
	field_id = models.ForeignKey(Field)
	gps_id = models.ForeignKey(GPS)

	def __unicode__(self):
		return self.field_id + self.gps_id

class EmployeeLocalization(models.Model):
	employee_id = models.ForeignKey(Employee)
	gps_id = models.ForeignKey(GPS)
	e_time = models.DateTimeField()

	def __unicode__(self):
		return self.field_id + self.gps_id + self.gps_id

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
		return self.field_id + self.rate_cost + self.description

class EmployeeTask(models.Model):
	employee_id = models.IntegerField()
	task_id = models.IntegerField()
	task_init = models.DateField()
	hours_sepnt = models.FloatField()
	substitution = models.BooleanField()

	def __unicode__(self):
		return self.employee_id + self.task_init + self.hours_sepnt

class TaskImplementMachine(models.Model):
	task_id = models.IntegerField()
	machine_id = models.IntegerField()
	implement_id = models.IntegerField()
	machine = models.BooleanField()

	def __unicode__(self):
		return self.task_id + self.Machine_id + self.implement_id

class Appendix(models.Model):
	a_type =  models.CharField(max_length = 20)

	def __unicode__(self):
		return self.a_id + self.a_type

class AppendixTask(models.Model):
	appendix_id = models.ForeignKey(Appendix)
	task_id = models.ForeignKey(Task)
	quantity = models.IntegerField()
	brand = models.CharField(max_length = 20)

	def __unicode__(self):
		return self.appendix_id + self.brand

class ServiceCategory(models.Model):
	service_category = models.CharField(max_length = 30)

	def __unicode__(self):
		return self.service_category

class Service(models.Model):
	category_id = models.IntegerField()
	date = models.DateTimeField()
	done = models.BooleanField()

	def __unicode__(self):
		return self.category_id + self.s_date + self.done

class MachineService(models.Model):
	machine_id = models.ForeignKey(Machine)
	service_id = models.ForeignKey(Service)
	description = models.CharField(max_length = 200)
	done = models.BooleanField()
	expected_date = models.DateTimeField()
	price = models.FloatField()

	def __unicode__(self):
		return self.description + self.expected_date + self.price + self.done

class ImplementService(models.Model):
	implement_id = models.ForeignKey(Implement)
	service_id = models.ForeignKey(Service)
	description = models.CharField(max_length = 200)
	expected_date = models.DateTimeField()
	done = models.BooleanField()
	price = models.FloatField()