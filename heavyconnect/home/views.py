from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.utils.dateformat import DateFormat

from django.template.loader import render_to_string
from django.db import transaction


import json
import datetime

from home.forms import *
from home.models import *


def home(request):
	if request.user.is_authenticated():
		employee = Employee.objects.get(user_id = request.user.id)
		if employee.permission_level == 1: #Driver
			return redirect('driver')
		elif employee.permission_level == 2: #Manager
			return redirect('indexManager')
	else:
		return render(request, 'login.html')

def updatedDate(request):
	dt = datetime.now()
	df = DateFormat(dt)
	result = df.format('D, F j Y - g:i A')
	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def taskflow(request):
	return render(request, 'taskflow.html')

@login_required
def createNewTask1(request):
	form = taskForm(request.POST)
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			if form.is_valid():
				try:
					employee = Employee.objects.get(user_id = request.user.id)
					field = form.cleaned_data['field']
					category = form.cleaned_data['category']
					hours_prediction = float(form.cleaned_data['hours_prediction'])
					description = form.cleaned_data['description']
					passes = int(form.cleaned_data['passes'])
					time = form.cleaned_data['time']
					date = form.cleaned_data['date']
					date = date + datetime.timedelta(hours = time.hour, minutes = time.minute)
					task = Task(field = field, category = category, hours_prediction = hours_prediction, description = description, passes = passes, date = date)
					task.save()
					result['success'] = True
				except Employee.DoesNotExist:
					result['code'] =  1 #There is no users associated with this
			else:
				result['code'] = 2 #No all data is valid
		else:
			result['code'] = 3 #Use ajax to perform requests
	else:
		result['code'] = 4 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def createNewTask2(request):
	result = {'success' : False}


	return HttpResponse(json.dumps(result),content_type='application/json')

# Receives, as argument, filter information
# from front-end (size, manufacturer, etc) and Implement_id
# (if chosen or NULL if not chosen). Then, retrieves all machines
# from Machine table, filtering by those information.
# Check with Patrick whi info should be filtered and what info retrieved.
# Used tables: Machines, Implements
@login_required
def retrieveMachine(request):
	result = {'success' : False}

	machine = Machine.objects.all()
	print machine

	# if request.method == 'POST':
	# 	if request.is_ajax():
	# 		try:
	# 			...
	# 		except Employee.DoesNotExist:
	# 			result['code'] =  1 #There is no users associated with this
	# 	else:
	# 		result['code'] = 2 #Use ajax to perform requests
	# else:
	# 	result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def startShift(request):
	result = {'success' : False}

	if request.method == "POST":
		if request.is_ajax():
			try:
				identifier = request.POST['id']
				employee = Employee.objects.get(id = int(identifier))
				now = datetime.datetime.now()
				attendance, created = EmployeeAttendance.objects.get_or_create(employee_id = employee, defaults = {'date' : now, 'hour_started' : now})
				if created:
					result['success'] = True
					result['hour_started'] = str(attendance.hour_started)
				else:
					result['code'] = 1 #The shift for today was already created
			except Employee.DoesNotExist:
				result['code'] =  2 #There is no users associated with this id
		else:
			result['code'] = 3 #Use ajax to perform requests
	else:
		result['code'] = 4 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def stopShift(request):
	result = {'success' : False}

	if request.method == "POST":
		if request.is_ajax():
			try:
				identifier = request.POST['id']
				employee = Employee.objects.get(id = int(identifier))
				now = datetime.datetime.now()
				attendance, created = EmployeeAttendance.objects.get_or_create(employee_id = employee, defaults = {'date' : now, 'hour_ended' : now})
				if created:
					result['success'] = True
					result['hour_ended'] = str(attendance.hour_ended)
				else:
					result['code'] = 1 #The shift for today was already finished
			except Employee.DoesNotExist:
				result['code'] =  2 #There is no users associated with this id
		else:
			result['code'] = 3 #Use ajax to perform requests
	else:
		result['code'] = 4 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def startStopBreak(request):
	result = {'success' : False}

	if request.method == 'POST': #check if the method used for the request was POST
		if request.is_ajax(): #check if the request came from ajax request

			identifier = request.POST['id']
			employee = Employee.objects.get(id = int(identifier))

			now = datetime.datetime.now()
			start_date = datetime.datetime.combine(now, datetime.time.min)
			end_date = datetime.datetime.combine(now, datetime.time.max)

			optcode = request.POST['optcode']

			try:
				attendance = EmployeeAttendance.objects.get(employee_id = employee.id, date__range = (start_date, end_date))

				if optcode == '1':
					if attendance.break_one is None:
						attendance.break_one = now
						result['success'] = True
						result['time'] = str(now)
					else:
						result['code'] = 1 #break one already started
				elif optcode == '2':
					if attendance.break_one_end is None:
						attendance.break_one_end = now
						result['success'] = True
						result['time'] = str(now)
					else:
						result['code'] = 2 #break one already ended
				elif optcode == '3':
					if attendance.break_two is None:
						attendance.break_two = now
						result['success'] = True
						result['time'] = str(now)
					else:
						result['code'] = 3 #break two already started
				elif optcode == '4':
					if attendance.break_two_end is None:
						attendance.break_two_end = now
						result['success'] = True
						result['time'] = str(now)
					else:
						result['code'] = 4 #break two already ended
				elif optcode == '5':
					if attendance.break_three is None:
						attendance.break_three = now
						result['success'] = True
						result['time'] = str(now)
					else:
						result['code'] = 5 #break three already started
				elif optcode == '6':
					if attendance.break_three_end is None:
						attendance.break_three_end = now
						result['success'] = True
						result['time'] = str(now)
					else:
						result['code'] = 6 #break two already ended
				else:
					result['code'] = 7 #Invalid optcode

				attendance.save()
			except EmployeeAttendance.DoesNotExist:
				result['code'] = 8 #You have not started your shift yet
		else:
	 		result['code'] = 9 #Use ajax to perform requests
	else:
		result['code'] = 10 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getEmployeeLocation(request):
	result = {'success' : False}

	if request.method == 'POST': #check if the method used for the request was POST
		if request.is_ajax(): #check if the request came from ajax request
			try:
				employee = Employee.objects.get(user_id = request.user.id)
				localization = EmployeeLocalization.objects.filter(employee_id = employee.id).order_by('-e_time').values('latitude','longitude')[0]
				result['latitude'] = localization['latitude']
				result['longitude'] = localization['longitude']
				result['success'] = True
			except Employee.DoesNotExist:
				result['code'] = 1 #There is no users associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

def login(request):
	#validating the received form
	form = loginForm(request.POST)
	result = {'success' : False}

	if request.method == 'POST': #check if the method used for the request was POST
		if request.is_ajax(): #check if the request came from a ajax request
			if form.is_valid():	#checking if the form with the login information is valid and has all the information
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						auth_login(request,user)
						#return redirect('driver')
						result['success'] = True
					else:
						result['code'] = 1 #This user is not active in the system
 				else:
 					result['code'] = 2 #Wrong password or username
 			else:
 				result['code'] = 3 #Invalid form
		else:
			result['code'] = 4 #Use ajax to perform requests
	else:
		result['code'] = 5 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getDriverInformation(request):
	result = {'success' : False}

	if request.method == 'POST':
		if request.is_ajax():
			try:
				employee =  Employee.objects.get(user_id = request.user.id)
				result['first_name'] = employee.user.first_name
				result['last_name'] = employee.user.last_name
				result['company_id'] = employee.company_id
				result['qr_code'] = employee.qr_code
				result['hire_date'] = str(employee.start_date)
				result['utilization'] = 0
				result['hours_today'] = getHoursToday(employee.id)
				result['hours_week'] = getWeekHours(employee.id)
				result['success'] = True
			except DoesNotExist:
				result['code'] = 1 #There is no users associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

#Get basic information about the User
@login_required
def getQuickUser(request):
	result = {'success' : False}

	if request.method == 'POST':
	 	if request.is_ajax():
	 		try:
				employee = Employee.objects.get(user_id = request.user.id)
				result['first_name'] = employee.user.first_name
				result['last_name'] = employee.user.last_name
				result['permission_level'] = employee.permission_level
				result['user_id'] = employee.user_id
				result['url'] = employee.photo
				result['success'] = True
	 		except Employee.DoesNotExist:
	 			result['code'] = 1 #There is no users associated with this
	 	else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

#Receive one url to a picture and changes the old url in the user profile
@login_required
def updatePhoto(request):
	result = {'success' : False}
	if request.method == 'POST':
	 	if request.is_ajax():
	 		try:
				employee = Employee.objects.get(user_id = request.user.id)
				employee.photo = request.POST['photo']
				result['photo'] = employee.photo
				result['success'] = True
				employee.save()
			except DoesNotExist:
	 			result['code'] = 1 #There is no users associated with this
	 	else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')


# Driver 3.4.1.1
# Get equipment status, which can be a machine or a implement
# Remember the Fron-End guys that Status is mapped as:
# 1 = OK, 2 = Attention, 3 = Broken, 4 = Quarantine
@login_required
def getEquipmentStatus(request):
	result = {'success' : False}
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				machine = Machine.objects.get(qr_code = request.POST['qr_code'])
				result['status'] = machine.status
				result['success'] = True
			except Machine.DoesNotExist:
				try:
					implement = Implement.objects.get(qr_code = request.POST['qr_code'])
					result['status'] = implement.status
					result['success'] = True
				except Implement.DoesNotExist:
	 				result['code'] = 1 #There is no equipment for this qr_code
	 	else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

# Driver 3.2
# Get equipment info by qr_code, which can be a machine or a implement and return it
@login_required
def getEquipmentInfo(request):
	result = {'success' : False}
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				machine = Machine.objects.get(qr_code = request.POST['qr_code'])
				result['manufacturer'] = machine.manufacturer_model.manufacturer.name
				result['model'] = machine.manufacturer_model.model
				result['asset_number'] = machine.asset_number
				result['serial_number'] = machine.serial_number
				result['horse_power'] = machine.horsepower
				result['hitch_capacity'] = machine.hitch_capacity
				result['drawbar_category'] = machine.drawbar_category
				result['year_purchased'] = machine.year_purchased
				result['status'] = machine.status
				result['hour_cost'] = machine.hour_cost
				result['photo'] = machine.photo
				result['success'] = True
			except Machine.DoesNotExist:
				try:
					implement = Implement.objects.get(qr_code = request.POST['qr_code'])
					result['manufacturer'] = implement.manufacturer_model.manufacturer.name
					result['model'] = implement.manufacturer_model.model
					result['asset_number'] = implement.asset_number
					result['serial_number'] = implement.serial_number
					result['horse_power_req'] = implement.horse_power_req
					result['hitch_capacity'] = implement.hitch_capacity_req
					result['drawbar_category'] = implement.drawbar_category
					result['year_purchased'] = implement.year_purchased
					result['status'] = implement.status
					result['hour_cost'] = implement.hour_cost
					result['photo'] = implement.photo
					result['success'] = True
				except Implement.DoesNotExist:
					result['code'] = 1 #There is no equipment associated with this
	 	else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

#This function givew back the Machine information, big part of them
@login_required
def retrieveScannedMachine(request):
	result = {'success' : False}
  	if request.method == 'POST':
	 	if request.is_ajax():
	 		try:
		 		machine = Machine.objects.get(qr_code = request.POST['qr_code'])
	 			models = ManufacturerModel.objects.get(manufacturer = machine.manufacturer_model.id)
		 		manufacturers = Manufacturer.objects.get(id = models.id)
				result['manufacture'] = manufacturers.name
				result['serial'] = machine.serial_number
				result['status'] = machine.status
				result['model'] = models.model
				result['asset_number'] = machine.asset_number
				result['horsepower'] = machine.horsepower
				result['hitch_capacity'] = machine.hitch_capacity
				result['hitch_category'] = machine.hitch_category
				result['drawbar_category'] = machine.drawbar_category
				result['speed_range_min'] = machine.speed_range_min
				result['speed_range_max'] = machine.speed_range_max
				result['year_purchased'] = machine.year_purchased
				result['engine_hours'] = machine.engine_hours
				result['base_cost'] = machine.base_cost
				result['m_type'] = machine.m_type
				result['front_tires'] = machine.front_tires
				result['rear_tires'] = machine.rear_tires
				result['steering'] = machine.steering
				result['operator_station'] = machine.operator_station
				result['hour_cost'] = machine.hour_cost
				result['photo'] = machine.photo
				if result['status'] is 1:
 					result['success'] = True
			except Machine.DoesNotExist:
				result['code'] = 1 #There is no users associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
 	return HttpResponse(json.dumps(result),content_type='application/json')



# Driver 6.3.2.5
# It will return the Machine filtered by some options and the Implement (if it has been chosed)
# In the Front End, it will have choices with ids for Manufacture.
# Attention: This function will return only machines with status = 'OK' and status = 'Attention'
# So in case no machine have returned, consider machine 'Broken' or in 'Quarantine'
@login_required
def getFilteredMachine(request):
	result = []
	each_result = {}

	result.append({'success' : False})
  	if request.method == 'POST':
		# Save values from request
		manufacturer = request.POST['manufacturer']
		hitch_capacity = request.POST['hitch_capacity']
		horse_power = request.POST['horse_power']
		implement_qr_code = request.POST['implement_qr_code']
		# Set minimum values in case no filters were applied for those option
		if hitch_capacity == '' or hitch_capacity == None:
			hitch_capacity = -1
		if horse_power == '' or horse_power == None:
			horse_power = -1

	 	if request.is_ajax():
	 		try:
				# Filtering by manufacturer, hitch_cap, horse_power, and status.
				# Do not filter by manufacture in case if this filter hasn't been chosen
				if manufacturer == '' or manufacturer == None:
					machine = Machine.objects.filter(
					hitch_capacity__gte = hitch_capacity,
					horsepower__gte = horse_power,
					status__lte = 2)
				else:
					machine = Machine.objects.filter(
					manufacturer_model__manufacturer__id = manufacturer,
					hitch_capacity__gte = hitch_capacity,
					horsepower__gte = horse_power,
					status__lte = 2)
				# Remove those machines that doesn't support the hitch capacity required by the selected implement,
				# and those machines that have different hitch category then the selected implement
				if implement_qr_code != '' or implement_qr_code != None:
					implement = Implement.objects.get(qr_code = implement_qr_code)
					machine2 = machine.exclude(hitch_capacity__lt = implement.hitch_capacity_req)
					machine3 = machine2.exclude(hitch_category__gt = implement.hitch_category).exclude(hitch_category__lt = implement.hitch_category)
				# Selecting which field will be retrieved to fron-end
				for each in machine3:
					each_result['qr_code'] = each.qr_code
					each_result['nickname'] = each.nickname
					each_result['photo'] = each.photo
					each_result['horse_power'] = each.horsepower
					each_result['asset_number'] = each.asset_number
					each_result['drawbar_category'] = each.drawbar_category
					result.append(each_result)
					each_result = {}
				result[0] = {'success' : True}
			except Machine.DoesNotExist:
				result.append({'code' : 1}) #There is no users associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3}) #Request was not POST
 	return HttpResponse(json.dumps(result),content_type='application/json')



# Driver 6.3.2.6
# It will return the Implement filtered by some options and the Machine (if it has been chosed)
# In the Front End, it will have choices with ids for Manufacture.
# Attention: This function will return only machines with status = 'OK' and status = 'Attention'
# So in case no implements have returned, consider implements 'Broken' or in 'Quarantine'
@login_required
def getFilteredImplement(request):
	result = []
	each_result = {}
	result.append({'success' : False})
  	if request.method == 'POST':
		# Save values from request
		manufacturer = request.POST['manufacturer']
		hitch_capacity_req = request.POST['hitch_capacity_req']
		horse_power_req = request.POST['horse_power_req']
		machine_qr_code = request.POST['machine_qr_code']
		# Set minimum values in case no filters were applied for those option
		if hitch_capacity_req == '' or hitch_capacity_req == None:
			hitch_capacity_req = -1
		if horse_power_req == '' or horse_power_req == None:
			horse_power_req = -1

	 	if request.is_ajax():
	 		try:
				# Filtering by manufacturer, hitch_cap_req, horse_power_req, and status.
				# Do not filter by manufacture in case if this filter hasn't been chosen
				if manufacturer == '' or manufacturer == None:
					implement = Implement.objects.filter(
					hitch_capacity_req__gte = hitch_capacity_req,
					horse_power_req__gte = horse_power_req,
					status__lte = 2)
				else:
					implement = Implement.objects.filter(
					manufacturer_model__manufacturer__id = manufacturer,
					hitch_capacity_req__gte = hitch_capacity_req,
					horse_power_req__gte = horse_power_req,
					status__lte = 2)
				# Remove those implements that requires more hitch capacity then the selected machine can carry,
				# and those implements that have different hitch category then the selected machine
				if machine_qr_code != '' or machine_qr_code != None:
					machine = Machine.objects.get(qr_code = machine_qr_code)
					implement2 = implement.exclude(hitch_capacity_req__gt = machine.hitch_capacity)
					implement3 = implement2.exclude(hitch_category__gt = machine.hitch_category).exclude(hitch_category__lt = machine.hitch_category)
				# Selecting which field will be retrieved to fron-end
				for each in implement3:
					each_result['qr_code'] = each.qr_code
					each_result['nickname'] = each.nickname
					each_result['photo'] = each.photo
					each_result['horse_power_req'] = each.horse_power_req
					each_result['asset_number'] = each.asset_number
					each_result['drawbar_category'] = each.drawbar_category
					result.append(each_result)
					each_result = {}
				result[0] = {'success' : True}
			except Machine.DoesNotExist:
				result.append({'code' : 1}) #There is no users associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3}) #Request was not POST
 	return HttpResponse(json.dumps(result),content_type='application/json')



# Driver 6.3.2.2
# Just retrieve a Implement according with qr_code passed as argument
@login_required
def getScannedImplement(request):
	result = {'success' : False}
  	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				implement = Implement.objects.get(qr_code = request.POST['qr_code'])
				result['qr_code'] = implement.qr_code
				result['nickname'] = implement.nickname
				result['year_purchased'] = implement.year_purchased
				result['photo'] = implement.photo
				result['manufacturer_model'] = implement.manufacturer_model.manufacturer.name
				result['asset_number'] = implement.asset_number
		 		result['horse_power_req'] = implement.horse_power_req
				result['hitch_capacity_req'] = implement.hitch_capacity_req
				result['status'] = implement.status
				result['speed_range_max'] = implement.speed_range_max
				result['success'] = True
			except Implement.DoesNotExist:
				result['code'] = 1 #There is no users associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

# Driver 6.3.2.4
# It will return (some) information of all implements on database.
# The result will be and vector of dictionaries, with the 'success' on first position.
@login_required
def getAllImplementInfo(request):
	each_result = {}
	result = []
	result.append({'success' : False})
	if not request.method == 'POST':
	 	if not request.is_ajax():
			try:
				implements_tmp = Implement.objects.filter()
				# Remove implement with status = 'broken' and status = 'quarantine'
				implements = implements_tmp.exclude(status__gte = 3)
				for each in implements:
					each_result['qr_code'] = each.qr_code
					each_result['year_purchased'] = each.year_purchased
					each_result['nickname'] = each.nickname
					each_result['photo'] = each.photo
					each_result['manufacturer_model'] = each.manufacturer_model.manufacturer.name
					each_result['asset_number'] = each.asset_number
			 		each_result['horse_power_req'] = each.horse_power_req
					each_result['hitch_capacity_req'] = each.hitch_capacity_req
					each_result['status'] = each.status
					each_result['speed_range_max'] = each.speed_range_max
					result.append(each_result)
					each_result = {} # I have to clean it, otherwise it will keep the same value always
				result[0] = {'success' : True}
			except Machine.DoesNotExist:
				result.append({'code' : 1}) #There is no machine associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3}) #result[0]['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

#This function gives back the picture of the refered QrCode
@login_required
def loadEquipmentImage(request):
	result = {'success' : False}
	if request.method == 'POST':
		qrCode = request.POST['qr_code']
	 	if request.is_ajax():
			try:
				equipment = Machine.objects.get(qr_code = qrCode)
				result['url'] = equipment.photo
				result['success'] = True
			except Machine.DoesNotExist:
				try:
					equipment = Implement.objects.get(qr_code = qrCode)
					result['url'] = equipment.photo
					result['success'] = True
				except Implement.DoesNotExist:
					result['code'] = 1 #There is no equipment associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

#Look just into Machines
@login_required
def loadMachinesImage(request):
	result = {'success' : False}
	if request.method == 'POST':
		qrCode = request.POST['qr_code']
	 	if request.is_ajax():
			try:
				qrCode = request.POST['qr_code']
				machine = Machine.objects.get(qr_code = qrCode)
				result['url'] = machine.photo
				result['success'] = True
			except Machine.DoesNotExist:
				result['code'] = 1 #There is no machine associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

#Look just into Implements
@login_required
def loadImplementsImage(request):
	result = {'success' : False}
	if request.method == 'POST':
		qrCode = request.POST['qr_code']
	 	if request.is_ajax():
			try:
				qrCode = request.POST['qr_code']
				Implement = Implement.objects.get(qr_code = qrCode)
				result['url'] = Implement.photo
				result['success'] = True
			except Implement.DoesNotExist:
				result['code'] = 1 #There is no Implement associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

#Return task that are not complished until today, the number of task returned is according to the number n
@login_required
def retrievePendingTask(request):
	result = []
	result.append({'success' : False})
	date1 = datetime.timedelta(days = 1) #it will work as increment to the current day
	date2 =  datetime.datetime.now() + date1
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				aux = {}
				n = int(request.POST['N'])
				if n > 0:
					emploTask = EmployeeTask.objects.filter(employee__id = request.user.id, task_init__lte =  date2, task__accomplished = False)[:n]
					for item in emploTask:
						aux['category'] = item.task.description
						aux['field'] = item.task.field.name
						aux['date'] = str(item.task.date)
						aux['task_id'] = item.task.id
						machine = Machine.objects.filter(machine_id = TaskImplementMachine.objects.filter(task_id = item.task.id))
						aux['qr_code'] = machine.qr_code
						result.append(aux)
						aux = {}
					result[0] = {'success' : True}
				else:
					result.append({'result' : 11})#Index is invalid
			except EmployeeTask.DoesNotExist:
				result.append({'result' : 1})#There is no Implement associated with this
		else:
	 		result.append({'result' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'result' : 3}) #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

#Return
@login_required
def pastTaskList(request):
	result = []
	aux = {}
	result.append({'success' : False})
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				off = int(request.POST['offset'])
				limit =int(request.POST['limit'])
				if off >= 0 and limit > 0:
					tasks = EmployeeTask.objects.filter(employee__user__id = request.user.id, task__accomplished = False)[off:limit]
					for item in tasks:
						try:
							equipment = TaskImplementMachine.objects.get(task__id = item.task.id)
							aux['machine'] = equipment.machine.qr_code
						except:
							aux['machine'] = 'NONE'
						try:
							implement = TaskImplementMachine.objects.get(task__id = item.task.id)
							aux['implement'] = equipment.implement.qr_code
						except:
							aux['implement'] = 'NONE'
						aux['duration'] = item.hours_spent
						aux['task_id'] = item.task.id
						aux['category'] = item.task.description
						aux['field'] = item.task.field.name
						aux['date'] = str(item.task.date)
						result.append(aux)
						aux = {}
					result[0] = {'success' : True}
				else:
					result.append({'result' : 11})#Index is invalid
			except EmployeeTask.DoesNotExist:
				result.append({'result' : 1})#There is no Implement associated with this
		else:
	 		result.append({'result' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'result' : 3}) #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')


def getHoursToday(id):
	# now = datetime.datetime.now()
	# attendance = EmployeeAttendance.objects.get(employee_id = id)

	# if attendance.break_one is None:
	# 	delta = now - attendance.hour_started
	# elif
	#date__range = (datetime.datetime.combine(now, datetime.time.min),datetime.datetime.combine(now, datetime.time.max))
	return 0

def getWeekHours(id):
	return 0

#Return the information about the driver and his or her schedule
def getEmployeeSchedule(request):
	result = {'success' : False}

	if request.method == 'POST':
		if request.is_ajax():
			qrc = request.POST['qr_code']
			employee = Employee.objects.get(qr_code = qrc)

			#creating the data range for the day, generating the 00:00:00 and the 23:59:59 of the current day
			now = datetime.datetime.now()
			start_date = datetime.datetime.combine(now, datetime.time.min)
			end_date = datetime.datetime.combine(now, datetime.time.max)
			try:
				attendance = EmployeeAttendance.objects.get(employee_id = employee.id, date__range = (start_date, end_date))
				result['first_name'] = employee.user.first_name
				result['last_name'] = employee.user.last_name
				result['qr_code'] = employee.qr_code
				result['contact_number'] = employee. contact_number
				result['permission_level'] = employee.permission_level
				result['photo_url'] = employee.photo
				result['hour_started'] = str(attendance.hour_started)
				result['hour_ended'] = str(attendance.hour_ended)
				result['break_one'] = str(attendance.break_one)
				result['break_one_end'] = str(attendance.break_one_end)
				result['break_two'] = str(attendance.break_two)
				result['break_two_end'] = str(attendance.break_two_end)
				result['break_three'] = str(attendance.break_three)
				result['break_three_end'] = str(attendance.break_three_end)
				result['success'] = True
			except EmployeeAttendance.DoesNotExist:
				result['code'] = 1 #There is no shift records for this employee
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

def getAllManufacturers(request):
	result = []
	result.append({'success' : False})
	if request.method == 'POST':
		if request.is_ajax:
			try:
				manufacturers = Manufacturer.objects.all()
				result.append(str(manufacturers))
			except Manufacture.DoesNotExist:
				result.append({'code' : 1}) #There is no manufacture on the database
		else:
			result.append({'code': 2}) #result[0]['code'] = 2 #request is not ajax
	else:
		result.append({'code' : 3}) #result[0]['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

def getAllFields(request):
	result = []
	result.append({'success' : False})
	if request.method == 'POST':
		if request.is_ajax:
			try:
				fields = Field.objects.all()
				result.append(str(fields))
			except Manufacture.DoesNotExist:
				result.append({'code' : 1}) #There is no field on the database
		else:
			result.append({'code': 2}) #result[0]['code'] = 2 #request is not ajax
	else:
		result.append({'code' : 3}) #result[0]['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

def validatePermission(request):
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			try:
				employee = Employee.objects.get(id = request.user.id)
				aux = employee.permission_level
				result['authorized'] = False
				if aux == 2 or aux == 3:
					result['authorized'] = True
				result['success'] = True
			except Employee.DoesNotExist:
				result['code'] = 1 #There is no shift records for this employee
		else:
			result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')


def logout(request):
	auth_logout(request)
	return redirect('home')


@login_required
def driver(request):
    return render(request, 'driver/home.html')

@login_required
def profile(request):
    return render(request, 'driver/profile.html')

@login_required
def headerDriver(request):
    return render(request, 'template/headerDriver.html')

@login_required
def headerHome(request):
    return render(request, 'template/headerHome.html')

@login_required
def footer(request):
	return render(request, 'template/footer.html')

@login_required
def taskFlow(request):
	return render(request, 'driver/taskFlow.html')

@login_required
def time_keeper(request):
	return render(request, 'driver/timeKeeper.html')

@login_required
def equipament(request):
    return render(request, 'driver/equipment.html')

@login_required
def schedule(request):
    return render(request, 'driver/schedule.html')

@login_required
def updateStatus(request):
    return render(request, 'driver/updateStatus.html')

@login_required
def checklist(request):
    return render(request, 'driver/checklist.html')

@login_required
def headerManager(request):
    return render(request, 'template/headerManager.html')

@login_required
def createTask(request):
    return render(request, 'driver/createTask.html')

@login_required
def pastTasks(request):
    return render(request, 'driver/pastTasks.html')

@login_required
def startTask(request):
    return render(request, 'driver/startTask.html')

@login_required
def scanQRCode(request):
    return render(request, 'driver/scanQRCode.html')

@login_required
def indexManager(request):
    return render(request, 'manager/home.html')

@login_required
def fleet(request):
    return render(request, 'manager/fleet.html')

@login_required
def equipmentManager(request):
    return render(request, 'manager/equipment.html')

@login_required
def profileManager(request):
    return render(request, 'manager/profile.html')

def retrieveScannedEmployee(request):
	result = {'success' : False}
  	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				employee = Employee.objects.get(qr_code = request.POST['qr_code'])
				result['first_name'] = employee.user.first_name
				result['last_name'] = employee.user.last_name
				result['photo'] = employee.photo
			except Employee.DoesNotExist:
				result['code'] = 1 #There is no records for this employee
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
 	return HttpResponse(json.dumps(result),content_type='application/json')

def continueTask(request):
	result = []
	result.append({'success' : False})
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				flag = 0
				aux = {}
				employeeTask = EmployeeTask.objects.filter(task_id_id__id = request.POST['id'], task_id__accomplished = False)
				for item in employeeTask:
						aux['description'] = item.task_id.description
						aux['id'] = item.task_id.field_id_id
						aux['passes'] = item.task_id.passes
						aux['hours_prediction'] = item.task_id.hours_prediction
						aux['hour_started'] = str(item.task_init)
						result.append(aux)
						aux = {}
				result[0] = {'success' : True}
			except EmployeeTask.DoesNotExist:
				result.append({'result' : 1})#There is no Implement associated with this
		else:
	 		result.append({'result' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'result' : 3}) #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

# @menezescode: Page only to show the form was correctly sended.
def formOk(request):
	return render(request, 'formOk.html')

'''
<menezescode:
Just a quick explanation on how to test forms:
	def FORMNAMEREHE(request):
	    if request.method == 'POST': # If the form has been submitted...
	        form = FORMNAMEREHE(request.POST) # A form bound to the POST data
	        if form.is_valid(): # All validation rules pass
	            # Process the data in form.cleaned_data
	            # ...
	            return HttpResponseRedirect('/thanks/') # Redirect after POST
	    else:
	        form = ContactForm() # An unbound form

	    return render(request, 'THEPAGEYOUWANTTOBERETURNED.html', {
	        'form': form,
	    })
</menezescode>

@menezescode: 	Those are the forms. At the current point 06/22/2015,
				each view does nothgin besides render the page and redirect
				to a different page (formOk) if it's correct and reload the page
				if the form was sent incorrectly
'''
def manufacturerFormView(request):
	result = {'success' : False}
	if request.method == 'POST':
		form = manufacturerForm(request.POST)
		if form.is_valid():
			# return redirect('formOk')
			man_name = form.cleaned_data['name']
			new_manufacturer = Manufacturer(name = man_name)
			new_manufacturer.save()
			result['success'] = True
			return HttpResponse(json.dumps(result),content_type='application/json')
		else:
			return render(request, 'formTest.html', {'form': form})

def manufacturerModelFormView(request):
	form = manufacturerModelForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def repairShopFormView(request):
	form = repairShopForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def shopFormView(request):
	form = shopForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def equipmentCategoryFormView(request):
	form = EquipmentCategoryForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def equipmentTypeFormView(request):
	form = EquipmentTypeForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def machineFormView(request):
	form = machineForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def implementFormView(request):
	form = implementForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})
def employeeFormView(request):
	form = employeeForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def employeeAttendanceFormView(request):
	form = employeeAttendanceForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def qualificationFormView(request):
	form = qualificationForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def certificationFormView(request):
	form = certificationForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def employeeQualificationsFormView(request):
	form = employeeQualificationsForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def machineQualificationFormView(request):
	form = machineQualificationForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})
def implementQualificationFormView(request):
	form = implementQualificationForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def fieldFormView(request):
	form = fieldForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def gpsFormView(request):
	form = gpsForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def employeeLocalizationFormView(request):
	form = employeeLocalizationForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def taskFormView(request):
	form = taskForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def taskCategoryFormView(request):
	form = taskCategoryForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})
def employeeTaskFormView(request):
	form = employeeTaskForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def taskImplementMachineFormView(request):
	form = taskImplementMachineForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def appendixFormView(request):
	form = appendixForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def appendixTaskFormView(request):
	form = appendixTaskForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def serviceCategoryFormView(request):
	form = serviceCategoryForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def serviceFormView(request):
	form = serviceForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def machineServiceFormView(request):
	form = machineServiceForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def implementServiceFormView(request):
	form = implementServiceForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def questionFormView(request):
	form = questionForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def machineChecklistFormView(request):
	form = machineChecklistForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

def implementChecklistFormView(request):
	form = implementChecklistForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})
