from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.utils.dateformat import DateFormat
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

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

def createNewTask(request):
	form = taskForm(request.POST)
	result = {'success' : False}

	if request.method == 'POST':
		if request.is_ajax():
			if form.is_valid():
				try:
					#Getting the employee that are logged in
					employee = Employee.objects.get(user_id = request.user.id)

					#Extracting the fields from the form
					field = form.cleaned_data['field']
					category = form.cleaned_data['category']
					hours_prediction = float(form.cleaned_data['hours_prediction'])
					description = form.cleaned_data['description']
					passes = int(form.cleaned_data['passes'])
					time = form.cleaned_data['time']
					date = form.cleaned_data['date']
					machine = form.cleaned_data['machine']
					implement = form.cleaned_data['implement']
					implement2 = form.cleaned_data['implement2']
					#Creating Task
					date = date + datetime.timedelta(hours = time.hour, minutes = time.minute)
					task, created = Task.objects.get_or_create(field = field, category = category, hours_prediction = hours_prediction, description = description, passes = passes, date_assigned = date)
					if created:
						#Creating association between Employee and Task
						empTask = EmployeeTask(employee = employee, task = task)
						empTask.save()

						#Creating association between Machine and Task
						macTask = MachineTask(task = task, machine = machine, employee_task = empTask)
						macTask.save()

						#Creating association between Implement and Task
						impTask = ImplementTask(task = task, machine_task = macTask, implement = implement)
						impTask.save()

						if implement2 is not None:
							#Creating association between Implement2 and Task
							impTask2 = ImplementTask(task = task, machine_task = macTask, implement = implement2)
							impTask2.save()

						result['success'] = True
					else:
						result['code'] = 1 #This task was already created
				except Employee.DoesNotExist:
					result['code'] =  2 #There is no users associated with this
			else:
				result['code'] = 3 #No all data are valid
				result['errors'] = form.errors
		else:
			result['code'] = 4 #Use ajax to perform requests
	else:
		result['code'] = 5 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

def startNewTask(request):
 	result = {'success' : False}
 	if request.method == 'POST':
		task_id = request.POST['task_id']
 		if request.is_ajax():
			try:
				task = Task.objects.get(id = task_id)
				try:
					employeeTask = EmployeeTask.objects.get(task_id = task_id)
					now = datetime.datetime.now()
					employeeTask.start_time = now
					if task.task_init == None:
						task.task_init = now
					task.status = 4 # Update status for Ongoing
					employeeTask.save()
					task.save()
					result['success'] = True # Task table updated with success
				except EmployeeTask.DoesNotExist:
					result['code'] =  1 # EmployeeTask DoesNotExist
			except Task.DoesNotExist:
				result['code'] =  1 # Task DoesNotExist
 		else:
			result['code'] = 2 #Use ajax to perform requests
 	else:
		result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

def endTask(request):
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			try:
				task = EmployeeTask.objects.get(task_id = request.POST['task_id'])
				now = datetime.datetime.now()
				task.hours_spent = now - task.task_init
				task.save()
				result['success'] = True
			except Employee.DoesNotExist:
				result['code'] = 1 #Task DoesNotExist
		else:
			result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST
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
				employee = Employee.objects.get(user_id = request.user.id)

				now = datetime.datetime.now()
				start_date = datetime.datetime.combine(now, datetime.time.min)
				end_date = datetime.datetime.combine(now, datetime.time.max)

				attendance, created = EmployeeAttendance.objects.get_or_create(employee_id = employee.id, date__range = (start_date, end_date), defaults = {'date' : now, 'hour_started' : now})
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
				employee = Employee.objects.get(user_id = request.user.id)

				now = datetime.datetime.now()
				start_date = datetime.datetime.combine(now, datetime.time.min)
				end_date = datetime.datetime.combine(now, datetime.time.max)

				attendance = EmployeeAttendance.objects.get(employee_id = employee, date__range = (start_date, end_date))

				t_break = Break.objects.filter(attendance_id = attendance).order_by('start')
				amount = t_break.count()

				if attendance.hour_ended is None:
					if amount >= 3:
						attendance.hour_ended = now
						attendence.signature = request.POST['signature']
						attendance.save()
						result['success'] = True
						result['hour_ended'] = str(attendance.hour_ended)
					else:
						result['code'] = 1 #You need to take at least tree breaks
				else:
					result['code'] = 2 #The shift for today was already finished

			except EmployeeAttendance.DoesNotExist:
				result['code'] = 3 #You have not started your shift yet
			except Employee.DoesNotExist:
				result['code'] = 4 #There is no users associated with this id
		else:
			result['code'] = 5 #Use ajax to perform requests
	else:
		result['code'] = 6 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def startBreak(request):
	result = {'success' : False}

	if request.method == "POST":
		if request.is_ajax():
			try:
				employee = Employee.objects.get(user_id = request.user.id)

				now = datetime.datetime.now()
				start_date = datetime.datetime.combine(now, datetime.time.min)
				end_date = datetime.datetime.combine(now, datetime.time.max)

				attendance = EmployeeAttendance.objects.get(employee_id = employee, date__range = (start_date, end_date))

				if attendance.hour_ended is None:
					t_break = Break.objects.filter(attendance_id = attendance).order_by('-start')
					count = t_break.count()

					if count == 0 or t_break[0].end is not None:
						t2_break = Break(attendance = attendance, start = now)
						t2_break.save()
						result['success'] = True
						result['time'] = str(t2_break.start)
					else:
						result['code'] = 1 #You cannot start two breaks at the same time
				else:
					result['code'] = 2 #The shift for today was already finished
			except EmployeeAttendance.DoesNotExist:
				result['code'] = 3 #You need to start a shift first
		else:
			result['code'] = 4 #Use ajax to perform requests
	else:
		result['code'] = 5 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def stopBreak(request):
	result = {'success' : False}

	if request.method == "POST":
		if request.is_ajax():
			try:
				employee = Employee.objects.get(user_id = request.user.id)

				now = datetime.datetime.now()
				start_date = datetime.datetime.combine(now, datetime.time.min)
				end_date = datetime.datetime.combine(now, datetime.time.max)

				attendance = EmployeeAttendance.objects.get(employee_id = employee, date__range = (start_date, end_date))

				if attendance.hour_ended is None:
					t_break = Break.objects.filter(attendance_id = attendance).order_by('-start')
					count = t_break.count()

					if (count != 0) and t_break[0].end is None:
						t_break = t_break[0]
						t_break.end = now
						t_break.save()
						result['success'] = True
						result['time'] = str(t_break.end)
					else:
						result['code'] = 1 #You need to start a break first
				else:
					result['code'] = 2 #The shift for today was already finished
			except EmployeeAttendance.DoesNotExist:
				result['code'] = 3 #You need to start a shift first
		else:
			result['code'] = 4 #Use ajax to perform requests
	else:
		result['code'] = 5 #Request was not POST

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
				# Attention: This function is using the USER.ID instead of the Employee.ID
				employee =  Employee.objects.get(user_id = request.user.id)
				result['first_name'] = employee.user.first_name
				result['last_name'] = employee.user.last_name
				result['company_id'] = employee.company_id
				result['qr_code'] = employee.qr_code
				result['hire_date'] = str(employee.start_date)
				result['utilization'] = 0
				result['hours_today'] = getHoursToday(employee.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) # Salles changed it in order to keep the function working with the function
				result['hours_week'] = getHoursWeek(employee.id, datetime.date.today())
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

@login_required
def getQRCodeStatusForEquipment(request):
	result = {'success' : False}
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				machine = Machine.objects.get(qr_code = request.POST['qr_code'])
				result['success'] = True
			except Machine.DoesNotExist:
				try:
					implement = Implement.objects.get(qr_code = request.POST['qr_code'])
					result['success'] = True
				except Implement.DoesNotExist:
	 				result['code'] = 1 #There is no equipment for this qr_code
	 	else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

def updateEquipmentStatus(request):
	result = {'success' : False}
	if request.method == 'POST':
		machine_qr_code = request.POST['qr_code']
		new_status = request.POST['status']
	 	if request.is_ajax():
			try:
				machine = Machine.objects.get(qr_code = machine_qr_code)
				machine.status = new_status
				machine.save()
				result = {'success' : True}
			except Machine.DoesNotExist:
				try:
					implement = Implement.objects.get(qr_code = machine_qr_code)
					implement.status = new_status
					implement.save()
					result = {'success' : True}
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
				result['photo1'] = machine.photo1
				result['photo2'] = machine.photo2
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
					result['photo1'] = implement.photo1
					result['photo2'] = implement.photo2
					result['success'] = True
				except Implement.DoesNotExist:
					result['code'] = 1 #There is no equipment associated with this
	 	else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')



# Driver 6.3.1.3
# It will retrieve id + description of all task categories in database.
def getAllTaskCategory(request):
	each_result = {}
	result = []
	result.append({'success' : False})
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				all_task_category = TaskCategory.objects.filter()
				for each in all_task_category:
					each_result['id'] = each.id
					each_result['description'] = each.description
					result.append(each_result)
					each_result = {}
				result[0] = {'success' : True}
			except TaskCategory.DoesNotExist:
				result.append({'code' : 1}) #There is no task associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3})  #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')



# Driver 6.1.1
# Retrieve Task Information from task on the list of Pending Tasks
#####################################################################################
# obs: This function is expeting just one employee for each Task. No continues of   #
# past task are supported now. However, when this change, it will be needed just to #
# change object.get for object.filter, and use the higher index on each table   	#
# that match with Task.id desired, since the higher foreing key for Task will   	#
# corresponde to the last person assigned to the Task.id desired.					#
#####################################################################################
@login_required
def getTaskInfo(request):
	result = {'success' : False}
	if request.method == 'POST':
		task_id = request.POST['task_id']
	 	if request.is_ajax():
			try: # Check if task is added on the Task table
				task = Task.objects.get(id = task_id)
				try: # Check if task is added on MachineTask table
					machineTask = MachineTask.objects.get(task__id = task_id)
					try: # Check if task is added on ImplementTask table
						implementTask = ImplementTask.objects.get(task__id = task_id)
						try: # Check if task is added on EmployeeTask table
							employeeTask = EmployeeTask.objects.get(task__id = task_id)
							result['employee'] = str(employeeTask.employee.user.first_name)+' '+str(employeeTask.employee.user.last_name)
							result['field'] = task.field.name
							result['category'] = task.category.description
							result['description'] = task.description
							result['machine_nickname'] = machineTask.machine.nickname
							result['machine_photo'] = machineTask.machine.photo
							result['machine_qr_code'] = machineTask.machine.qr_code
							result['implement_nickname'] = implementTask.implement.nickname
							result['implement_photo'] = implementTask.implement.photo
							result['implement_qr_code'] = implementTask.implement.qr_code
							result['success'] = True
						except EmployeeTask.DoesNotExist:
							result['error4'] = 'Assigned employee not found for this task' #No Task associated on EmployeeTask table
					except ImplementTask.DoesNotExist:
						result['error3'] = 'Assigned implement not found for this task' #No Task associated on ImplementTask table
				except MachineTask.DoesNotExist:
					result['error2'] = 'Assigned machine not found for this task' #No Task associated on MachineTask table
			except Task.DoesNotExist:
				result['error1'] = 'Task not found' #There is no Task associated on Task table
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')




# This function givew back the Machine information, big part of them
# This function will be used on Equipment Page (not TaskFlow page)
@login_required
def retrieveScannedMachine(request):
	result = {'success' : False}
  	if request.method == 'POST':
 		if request.is_ajax():
 			try:
				machine = Machine.objects.get(qr_code = request.POST['qr_code'])
				result['qr_code'] = machine.qr_code
				result['manufacture'] = machine.manufacturer_model.manufacturer.name
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
				result['photo1'] = machine.photo1
				result['photo2'] = machine.photo2
				if result['status'] is 1:
 					result['success'] = True
			except Machine.DoesNotExist:
				result['code'] = 1 #There is no users associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
 	return HttpResponse(json.dumps(result),content_type='application/json')



# Driver 6.3.2.1
# Just retrieve a Machine according with qr_code passed as argument. And check if implement is compatible, if it was chosen.
@login_required
def getScannedMachine(request):
	result = {'success' : False}
	machine_is_valid = True
  	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				machine = Machine.objects.get(qr_code = request.POST['qr_code'])
				# Check if Implement was chosed. If yes, check its compatibility with machine.
				implement_qr_code = request.POST['implement_qr_code']
				if implement_qr_code:
					try:
						implement = Implement.objects.get(qr_code = implement_qr_code)
						if machine.hitch_capacity < implement.hitch_capacity_req:
							machine_is_valid = False
							result['error1'] = 'Machine does not have enough hitch capacity for this Implement'
						if machine.horsepower < implement.horse_power_req:
							machine_is_valid = False
							result['error2'] = 'Machine does not have enough horse power for this Implement'
						if machine.hitch_category != implement.hitch_category:
							machine_is_valid = False
							result['error3'] = 'Machine does not have the same hitch category of Implement'
						if machine.drawbar_category != implement.drawbar_category:
							machine_is_valid = False
							result['error4'] = 'Machine does not have the same drawbar category of Implement'
					except Implement.DoesNotExist:
						result['error'] = 'Implement do not found' #There is no machine associated
				# if Machine is compatible with implement (or if implement wasn't chosen),
				# save the desireble machine's data and return it to front end.
				if machine_is_valid == True:
					result['qr_code'] = machine.qr_code
					result['nickname'] = machine.nickname
					result['year_purchased'] = machine.year_purchased
					result['photo'] = machine.photo
					result['manufacturer_model'] = machine.manufacturer_model.manufacturer.name
					result['asset_number'] = machine.asset_number
			 		result['horse_power'] = machine.horsepower
					result['hitch_capacity'] = machine.hitch_capacity
					result['status'] = machine.status
					result['speed_range_max'] = machine.speed_range_max
					result['success'] = True
				else:
					result['code'] = 1 # Implement chosen early doesn't support scanned Machine.
			except Machine.DoesNotExist:
				result['code'] = 1 #There is no Machine associated
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')





# Driver 6.3.2.2
# Just retrieve a Implement according with qr_code passed as argument. And check if machine is compatible, if it was chosen.
@login_required
def getScannedImplement(request):
	result = {'success' : False}
	implement_is_valid = True
  	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				implement = Implement.objects.get(qr_code = request.POST['qr_code'])
				# Check if Machine was chosed. If yes, check its compatibility with implement.
				machine_qr_code = request.POST['machine_qr_code']
				if machine_qr_code:
					try:
						machine = Machine.objects.get(qr_code = machine_qr_code)
						if machine.hitch_capacity < implement.hitch_capacity_req:
							implement_is_valid = False
							result['error1'] = 'Implement requires more hitch capacity than Machine supports'
						if machine.horsepower < implement.horse_power_req:
							implement_is_valid = False
							result['error2'] = 'Implement requires more horse power than Machine supports'
						if machine.hitch_category != implement.hitch_category:
							implement_is_valid = False
							result['error3'] = 'Implement does not have the same hitch category of Machine'
						if machine.drawbar_category != implement.drawbar_category:
							implement_is_valid = False
							result['error4'] = 'Implement does not have the same drawbar category of Machine'
					except Machine.DoesNotExist:
						result['error'] = 'Machine do not found' #There is no machine associated

				# if Implement is compatible with machine (or if machine wasn't chosen),
				# save the desireble implement data and return it to front end.
				if implement_is_valid == True:
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
				else:
					result['code'] = 1 # Machine chosen early doesn't support scanned Implement.
			except Implement.DoesNotExist:
				result['code'] = 1 #There is no implement associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')



# Driver 6.3.2.3
# It will return (some) information of all machines on database.
# The result will be in a vector of dictionaries, with the 'success' on first position.
@login_required
def getAllMachineInfo(request):
	each_result = {}
	result = []
	result.append({'success' : False})
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				machine_tmp = Machine.objects.filter()
				# Remove implement with status = 'broken' and status = 'quarantine'
				machine = machine_tmp.exclude(status__gte = 3)
				for each in machine:
					each_result['qr_code'] = each.qr_code
					each_result['year_purchased'] = each.year_purchased
					each_result['nickname'] = each.nickname
					each_result['photo'] = each.photo
					each_result['manufacturer_model'] = each.manufacturer_model.manufacturer.name
					each_result['asset_number'] = each.asset_number
			 		each_result['horsepower'] = each.horsepower
					each_result['hitch_capacity'] = each.hitch_capacity
					each_result['status'] = each.status
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



# Driver 6.3.2.4
# It will return (some) information of all implements on database.
# The result will be in a vector of dictionaries, with the 'success' on first position.
@login_required
def getAllImplementInfo(request):
	each_result = {}
	result = []
	result.append({'success' : False})
	if request.method == 'POST':
	 	if request.is_ajax():
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
					result.append(each_result)
					each_result = {} # I have to clean it, otherwise it will keep the same value always
				result[0] = {'success' : True}
			except Implement.DoesNotExist:
				result.append({'code' : 1}) #There is no machine associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3}) #result[0]['code'] = 3 #Request was not POST
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
		# Set minimum values in case no filters were not applied for those option
		if not hitch_capacity:
			hitch_capacity = -1
		if not horse_power:
			horse_power = -1
		# Set the correct values for all status filters
		# All status filters will receive True or False.
		#   - If False, it will change to the correct value on the database  (1, 2, 3, or 4)
		#   - If True, it will still with 0
		status_ok = 0
		status_attention = 0
		status_broken = 0
		status_quarantine = 0
		if request.POST['status_ok'] == 'False':
			status_ok = 1
		if request.POST['status_attention'] == 'False':
			status_attention = 2
		if request.POST['status_broken'] == 'False':
			status_broken = 3
		if request.POST['status_quarantine'] == 'False':
			status_quarantine = 4

	 	if request.is_ajax():
	 		try:
				# Filtering by manufacturer, hitch_cap, horse_power, and status.
				# Do not filter by manufacture in case if this filter hasn't been chosen
				if manufacturer == '' or manufacturer == None:
					machine = Machine.objects.filter(
					hitch_capacity__gte = hitch_capacity,
					horsepower__gte = horse_power)
				else:
					machine = Machine.objects.filter(
					manufacturer_model__manufacturer__id = manufacturer,
					hitch_capacity__gte = hitch_capacity,
					horsepower__gte = horse_power)
				# Filter the machine with the correct desired status
				machine = machine.exclude(status = status_ok)
				machine = machine.exclude(status = status_attention)
				machine = machine.exclude(status = status_broken)
				machine = machine.exclude(status = status_quarantine)
				# Remove those machines that doesn't support the hitch capacity required by the selected implement,
				# Remove those machines that doesn't support the horsepower required by the selected implement
				# Remove those machines that have different hitch category then the selected implement
				# And remove those machines that have different drawbar category then the selected implement
				if implement_qr_code:
					implement = Implement.objects.get(qr_code = implement_qr_code)
					machine2 = machine.exclude(hitch_capacity__lt = implement.hitch_capacity_req)															# Remove Machine with less hitch_capacity
					machine3 = machine2.exclude(horsepower__lt = implement.horse_power_req)																	# Remove Machine with less horse_power
					machine2 = machine3.exclude(hitch_category__gt = implement.hitch_category).exclude(hitch_category__lt = implement.hitch_category)		# Remove Machine with different hitch_category
					machine = machine2.exclude(drawbar_category__gt = implement.drawbar_category).exclude(drawbar_category__lt = implement.drawbar_category)# Remove Machine with different drawbar_category
				# Selecting which field will be retrieved to fron-end
				for each in machine:
					each_result['qr_code'] = each.qr_code
					each_result['nickname'] = each.nickname
					each_result['photo'] = each.photo
					each_result['horse_power'] = each.horsepower
					each_result['asset_number'] = each.asset_number
					each_result['drawbar_category'] = each.drawbar_category
					each_result['status'] = each.status
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
		# Set the correct values for all status filters
		# All status filters will receive True or False.
		#   - If False, it will change to the correct value on the database  (1, 2, 3, or 4)
		#   - If True, it will still with 0
		status_ok = 0
		status_attention = 0
		status_broken = 0
		status_quarantine = 0
		if request.POST['status_ok'] == 'False':
			status_ok = 1
		if request.POST['status_attention'] == 'False':
			status_attention = 2
		if request.POST['status_broken'] == 'False':
			status_broken = 3
		if request.POST['status_quarantine'] == 'False':
			status_quarantine = 4

	 	if request.is_ajax():
	 		try:
				# Filtering by manufacturer, hitch_cap_req, horse_power_req, and status.
				# Do not filter by manufacture in case if this filter hasn't been chosen
				if manufacturer == '' or manufacturer == None:
					implement = Implement.objects.filter(
					hitch_capacity_req__gte = hitch_capacity_req,
					horse_power_req__gte = horse_power_req)
				else:
					implement = Implement.objects.filter(
					manufacturer_model__manufacturer__id = manufacturer,
					hitch_capacity_req__gte = hitch_capacity_req,
					horse_power_req__gte = horse_power_req)
				# Filter the machine with the correct desired status
				implement = implement.exclude(status = status_ok)
				implement = implement.exclude(status = status_attention)
				implement = implement.exclude(status = status_broken)
				implement = implement.exclude(status = status_quarantine)
				# Remove those implements that requires more hitch capacity then the selected machine can carry,
				# Remove those implements that requires more horse_power then the selected machine have,
				# Remove those implements that have different hitch category then the selected machine,
				# And remove those implements that have different drawbar category then the selected machine
				if machine_qr_code:
					machine = Machine.objects.get(qr_code = machine_qr_code)
					implement2 = implement.exclude(hitch_capacity_req__gt = machine.hitch_capacity)		# Remove Implement with more hitch_capacity req
					implement3 = implement2.exclude(horse_power_req__gt = machine.horsepower)			# Remove Implement with more horse_power req
					implement2 = implement3.exclude(hitch_category__gt = machine.hitch_category).exclude(hitch_category__lt = machine.hitch_category)	# Remove Implement with different hitch_category
					implement = implement2.exclude(drawbar_category__gt = machine.drawbar_category).exclude(drawbar_category__lt = machine.drawbar_category)# Remove Implement with different drawbar_category
				# Selecting which field will be retrieved to fron-end
				for each in implement:
					each_result['qr_code'] = each.qr_code
					each_result['nickname'] = each.nickname
					each_result['photo'] = each.photo
					each_result['horse_power_req'] = each.horse_power_req
					each_result['asset_number'] = each.asset_number
					each_result['drawbar_category'] = each.drawbar_category
					each_result['status'] = each.status
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




# Driver 6.3.3.1
# It will receive some employee qr_code, and maybe machine_qr_code and implement_qr_code, and it will
# return: first name, company_id, and photo; if its certification/qualification is enough for the
# machine and implement, if they were selected.
@login_required
def getScannedFilteredEmployee(request):
	result = []
	each_result = {}
	employee_is_able = True
	result.append({'success' : False})
  	if request.method == 'POST':
		# Save values from request
		employee_qr_code = request.POST['employee_qr_code']
		implement_qr_code = request.POST['implement_qr_code']
		machine_qr_code = request.POST['machine_qr_code']

	 	if request.is_ajax():
	 		try:
				# Create list of Qualifications that the employee has
				employee_used = Employee.objects.get(qr_code = employee_qr_code)
				emp_qualification = EmployeeQualifications.objects.filter(employee__id = employee_used.id)
				emp_qualification_list = []
				emp_qualification_level_list = {}
				for each in emp_qualification:
					emp_qualification_list.append(each.qualification.id)
					emp_qualification_level_list[str(each.qualification.id)] = each.level
				# Create list of Certifications that the employee has
				emp_certification = EmployeeCertifications.objects.filter(employee__id = employee_used.id)
				emp_certification_list = []
				for each in emp_certification:
					emp_certification_list.append(each.certification.id)

				# Check if the employee has all Qualifications required by Implement, if it was chosen
				if implement_qr_code:
					implement_used = Implement.objects.get(qr_code = implement_qr_code)
					imp_qualification = ImplementQualification.objects.filter(implement__id = implement_used.id)
					for each in imp_qualification:
						if each.qualification.id in emp_qualification_list:
							if each.qualification_required > emp_qualification_level_list[str(each.qualification.id)]:
								employee_is_able = False
								error = 'Insuficient level for qualification: '+str(each.qualification.description)+' required by selected Implement'
								result.append({'error':error})
						else:
							employee_is_able = False
							error = 'Missing qualification: '+str(each.qualification.description)+' required by selected Implement'
							result.append({'error':error})
					# Check if the employee has all Certifications required by Implement, if it was chosen
					imp_certification = ImplementCertification.objects.filter(implement__id = implement_used.id)
					for each in imp_certification:
						if not each.certification.id in emp_certification_list:
							employee_is_able = False
							error = 'Missing certification: '+str(each.certification.description)+' required by selected Implement'
							result.append({'error':error})

				# Check if the employee has all Qualifications required by Machine, if it was chosen
				if machine_qr_code:
					machine_used = Machine.objects.get(qr_code = machine_qr_code)
					mac_qualification = MachineQualification.objects.filter(machine__id = machine_used.id)
					for each in mac_qualification:
						if each.qualification.id in emp_qualification_list:
							if each.qualification_required > emp_qualification_level_list[str(each.qualification.id)]:
								employee_is_able = False
								error = 'Insuficient level for qualification: '+str(each.qualification.description)+' required by selected Machine'
								result.append({'error':error})
						else:
							employee_is_able = False
							error = 'Missing qualification: '+str(each.qualification.description)+' required by selected Machine'
							result.append({'error':error})
					# Check if the employee has all Certifications required by Machine, if it was chosen
					mac_certification = MachineCertification.objects.filter(machine__id = machine_used.id)
					for each in mac_certification:
						if not each.certification.id in emp_certification_list:
							employee_is_able = False
							error = 'Missing certification: '+str(each.certification.description)+' required by selected Machine'
							result.append({'error':error})

				if employee_is_able == True:
					result[0] = {'success' : True}
					each_result['name'] = str(employee_used.user.first_name)
					each_result['photo'] = employee_used.photo
					each_result['company_id'] = employee_used.company_id
					result.append(each_result)
			except Machine.DoesNotExist:
				result.append({'code' : 1}) #There is no users associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3}) #Request was not POST
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
				off = int(request.POST['offset'])
				limit = int(request.POST['limit'])
				# Filter EmployeeTask by user, date and status task != Finished
				emploTask   =  EmployeeTask.objects.filter(employee__user__id = request.user.id, task__date_assigned__lte = date2, task__status__lt = 6)[off:limit+off]
				invalidTasks = EmployeeTask.objects.filter(employee__user__id = request.user.id, task__date_assigned__lte = date2, task__status = 4)
				emploTaskList = []
				# Filter again EmployeeTask removing task with status = Ongoing
				for each in emploTask:
					if not each in invalidTasks:
						emploTaskList.append(each)
					
				for item in emploTaskList:
					aux['category'] = item.task.description
					aux['field'] = item.task.field.name
					aux['date'] = str(item.task.date_assigned)
					aux['task_id'] = item.task.id
					aux['employee_id'] = item.employee.id
					aux['employee_first_name'] = item.employee.user.first_name
					aux['employee_last_name'] = item.employee.user.last_name
					try:
						machineTask = MachineTask.objects.get(task__id = item.task.id)
						aux['machine_model'] = machineTask.machine.manufacturer_model.model
						aux['machine_nickname'] = machineTask.machine.nickname
						aux['machine_id'] = machineTask.machine.id
					except MachineTask.DoesNotExist:
						aux['machine_id'] = "NONE"
					try:
						# For now, this function just accept ONE implement per task
						# objects.get() has to be changed to objects.filter() later
						implementTask = ImplementTask.objects.get(task__id = item.task.id)
						aux['implement_model'] = implementTask.implement.manufacturer_model.model
						aux['implement_nickname'] = implementTask.implement.nickname
						aux['implement_id'] = implementTask.implement.id
					except ImplementTask.DoesNotExist:
						aux['implement_id'] = "NONE"
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



##Return task that are not complished until today, the number of task returned is according to the number n
@login_required
def pastTaskList(request):
	result = []
	result.append({'success' : False})
	if request.method == 'POST':
	 	if request.is_ajax():
			try:				
				aux = {}
				off = int(request.POST['offset'])
				limit = int(request.POST['limit'])
				# Filter EmployeeTask by user, date and status task != Finished
				emploTask   =  EmployeeTask.objects.order_by('-end_time').filter(employee__user__id = request.user.id, task__status = 6)[off:limit+off]
				print emploTask
				for item in emploTask:
					aux['category'] = item.task.description
					aux['field'] = item.task.field.name
					aux['date'] = str(item.start_time)
					aux['description'] = item.task.description
					# Calculate the duratio of the task based on EmployeeTask table (not in Task table)
					duration = datetime.timedelta( hours = item.end_time.hour - item.start_time.hour, 
													minutes = item.end_time.minute - item.start_time.minute, 	
													seconds=item.end_time.second - item.start_time.second)
					aux['duration'] = str(duration)
					aux['task_id'] = item.task.id
					aux['employee_id'] = item.employee.id
					aux['employee_first_name'] = item.employee.user.first_name
					aux['employee_last_name'] = item.employee.user.last_name
					try:
						machineTask = MachineTask.objects.get(task__id = item.task.id)
						aux['machine_model'] = machineTask.machine.manufacturer_model.model
						aux['machine_nickname'] = machineTask.machine.nickname
						aux['machine_id'] = machineTask.machine.id
					except MachineTask.DoesNotExist:
						aux['machine_id'] = "NONE"
					try:
						# For now, this function just accept ONE implement per task
						# objects.get() has to be changed to objects.filter() later
						implementTask = ImplementTask.objects.get(task__id = item.task.id)
						aux['implement_model'] = implementTask.implement.manufacturer_model.model
						aux['implement_nickname'] = implementTask.implement.nickname
						aux['implement_id'] = implementTask.implement.id
					except ImplementTask.DoesNotExist:
						aux['implement_id'] = "NONE"
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

# Get Employee current Task information if he is doing some task at the moment.
# Retrieve what Field he is and what Machine and Implement he is using
def getEmployeeCurrentTaskInfo(request):
	result = {}
	result['success'] = False
	if request.method == 'POST':
		employee_id = request.POST['employee_id']
	 	if request.is_ajax():
			try:				
				employeeTask = EmployeeTask.objects.get(employee__id = employee_id, task__status = 4)# Return Ongoing task of requested Employee
				result['task_id'] = employeeTask.task.id
				result['task_description'] = employeeTask.task.category.description
				result['field'] = employeeTask.task.field.name
				result['success'] = True
				try:
					machineTask = MachineTask.objects.get(task__id = employeeTask.task.id)
					result['machine_id'] = machineTask.machine.id
					result['machine_photo'] = machineTask.machine.photo
					result['machine_model'] = machineTask.machine.manufacturer_model.manufacturer.name
					result['machine_nickname'] = machineTask.machine.nickname
				except MachineTask.DoesNotExist:
					aux['machine_id'] = "NONE"
				try:
					implementTask = ImplementTask.objects.get(task__id = employeeTask.task.id)
					result['implement_id'] = implementTask.implement.id
					result['implement_photo'] = implementTask.implement.photo
					result['implement_model'] = implementTask.implement.manufacturer_model.manufacturer.name
					result['implement_nickname'] = implementTask.implement.nickname
				except ImplementTask.DoesNotExist:
					aux['implement_id'] = "NONE"
			except EmployeeTask.DoesNotExist:
				result['code'] = 1#There is no Implement associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3  #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

# change back:
# parametro request, voltar para employee_id, date_entry
# retirar os GET

def getHoursToday(employee_id, date_entry):
	realDate = datetime.datetime.strptime(date_entry, '%Y-%m-%d %H:%M:%S')
	start_date = datetime.datetime.combine(realDate, datetime.time.min)
	end_date = datetime.datetime.combine(realDate, datetime.time.max)
	employeeAttendance = EmployeeAttendance.objects.filter(employee_id = employee_id, date__range = (end_date,start_date)).order_by('date')
	count = datetime.timedelta(hours = 0, minutes = 0, seconds = 0) #counter to keep all the worked hours
	midnight = datetime.timedelta(hours = 23, minutes = 59, seconds = 59) # it is used when the hours changed from one day to another
	keeper = datetime.timedelta(hours = 0, minutes = 0, seconds = 0) #this variable will keep the last break. It is useful when the shift is not done
	keeper2 =  datetime.timedelta(hours = 0, minutes = 0, seconds = 0) # when the break is on another day
	count2 = 0          #this variable will keep track of which interration I am. It will help with the bug of break without shift end
	for item in employeeAttendance:
		breaks = Break.objects.filter(attendance__id = item.id)
		aux = datetime.timedelta(hours = 0, minutes = 0, seconds = 0)
		lenght = len(breaks)
		count2 = 0
		addition = datetime.timedelta(hours = 0, minutes = 0, seconds = 0) #addition works to add the time of the last break on the count. It is because the lastbreak should not be counted on if the attendance has the end value none
		for doc in breaks:
			docStart = datetime.timedelta(hours = doc.start.hour, minutes = doc.start.minute, seconds = doc.start.second)
			if docStart > keeper: #keeps the bigger break start
				keeper = docStart
			elif docStart < itemStart and docStart > keeper2: # if the bigger break is on another day
				keeper2 = docStart
			if doc.end != None and doc.end >= doc.start:
				aux += datetime.timedelta(hours = doc.end.hour, minutes = doc.end.minute, seconds = doc.end.second) - docStart
				if count2 == lenght-1:
					addition = datetime.timedelta(hours = doc.end.hour, minutes = doc.end.minute, seconds = doc.end.second) - docStart
			elif doc.end != None:
				aux += datetime.timedelta(hours = doc.end.hour, minutes = doc.end.minute, seconds = doc.end.second) + (midnight -  docStart)
				if count2 == lenght-1:
					addition = datetime.timedelta(hours = doc.end.hour, minutes = doc.end.minute, seconds = doc.end.second) - docStart
		itemStart = datetime.timedelta(hours = item.hour_started.hour, minutes = item.hour_started.minute, seconds = item.hour_started.second)
		if item.hour_ended != None: #this if will treat if the attendance does not have the end field proprely filled
			if item.hour_ended >= item.hour_started:
				count += (datetime.timedelta(hours = item.hour_ended.hour, minutes = item.hour_ended.minute, seconds = item.hour_ended.second) - itemStart) - aux
			else:  #if the end time is in another day
				count += (datetime.timedelta(hours = item.hour_ended.hour, minutes = item.hour_ended.minute, seconds = item.hour_ended.second) + (midnight - itemStart)) - aux
		elif keeper2 > datetime.timedelta(hours = 0, minutes = 0, seconds = 0): # if the keeper2 is changed means that the shift crossed midnight
			count += keeper2 - datetime.timedelta(hours = item.hour_started.hour, minutes = item.hour_started.minute, seconds = item.hour_started.second) - aux + addition
		else:
			count += keeper - datetime.timedelta(hours = item.hour_started.hour, minutes = item.hour_started.minute, seconds = item.hour_started.second) - aux + addition
			count2 += 1

	return str(count)


# This function call getHoursToday() for each day in the week of the desired day passed as argument
# It requries a employee_id and any day of the week, and the function will check all days of that week.
# Obs: A week is defined as starting at Sunday 00:00:00 and ending at next Saturday at 23:59:59
def getHoursWeek(employeeid, desired_date):
	hours_worked_week = datetime.timedelta(hours=0, minutes=0, seconds=0)
	today = datetime.date.today()
	begin_of_week = today.isoweekday()
	if begin_of_week == 7: # Avoid calculate wrong week when desired_day is a Sunday
		begin_of_week = 0
	first_week_day = desired_date - datetime.timedelta(days=begin_of_week) # Last Sunday's
	last_week_day = desired_date - datetime.timedelta(days=begin_of_week, weeks=-1	) # Next Sunday's

	attendance = EmployeeAttendance.objects.filter(employee_id = employeeid)
	for each in attendance:
		if each.date >= first_week_day and each.date < last_week_day:
			hours_today = getHoursToday(employeeid, str(each.date)+' 00:00:00') # getHoursToday expects [%Y-%M-%D %h:%m:%s] format
			times = hours_today.split(':')
			hours_worked_today = datetime.timedelta(hours=int(times[0]), minutes=int(times[1]), seconds=int(times[2]))
			hours_worked_week = hours_worked_week + hours_worked_today
	return str(hours_worked_week)



#Return the information about the driver and his or her schedule
@login_required
def getEmployeeShifts(request):
	result = {'success' : False}

	if request.method == 'POST':
		if request.is_ajax():

			employee = Employee.objects.get(user_id = request.user.id)

			try:
				attendance = EmployeeAttendance.objects.filter(employee_id = employee.id).order_by('date').first()
				result['first_name'] = employee.user.first_name
				result['last_name'] = employee.user.last_name
				result['qr_code'] = employee.qr_code
				result['contact_number'] = employee. contact_number
				result['permission_level'] = employee.permission_level
				result['photo_url'] = employee.photo

				if attendance is None:
					result['hour_started'] = ''
					result['hour_ended'] = ''
				else:
					result['hour_started'] = str(attendance.hour_started)
					result['hour_ended'] = str(attendance.hour_ended)
					breaks = Break.objects.filter(attendance_id = attendance.id).order_by('start').values()
					
					temp = []
					for item in breaks:
						temp.append((str(item['start']),str(item['end'])))

					result['breaks'] = temp
				result['success'] = True
			except EmployeeAttendance.DoesNotExist:
				result['code'] = 1 #There is no shift records for this employee
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getEmployeeSchedulePart(request):
	result = []
	if request.method == 'GET':
		if request.is_ajax():
			aux = request.GET['start'] #get the date in the POST request
			aux2 = request.GET['end']
			date_start = datetime.datetime.strptime(aux, '%Y-%m-%d')
			date_end = datetime.datetime.strptime(aux2, '%Y-%m-%d') + datetime.timedelta(days = 1)
			date_end = datetime.datetime.combine(date_end, datetime.time.max)
			emploTask = EmployeeTask.objects.filter(employee__user__id = request.user.id, task__date_assigned__range = (date_start, date_end))
			for item in emploTask:
				if item.task.status != 6:
					aux = {}
					auxHour = int(item.task.hours_prediction)
					auxMin = float(item.task.hours_prediction - auxHour) * 60
					data_prediction = item.task.date_assigned + datetime.timedelta(hours = auxHour, minutes = auxMin)
					equipment = getTaskImplementMachine(item.task.id, item.id)
					aux['start'] = str(item.task.date_assigned)
					aux['end'] = str(data_prediction)
					aux['description'] = item.task.description
					aux['field'] = item.task.field.name
					aux['category'] =  item.task.category.description
					# aux['equipment'] = equipment
					if len(equipment['implement']) > 0:
						aux['machine'] = equipment['machine']
						aux['implement'] = equipment['implement']
					else:
						aux['machine'] = []
						aux['implement'] = []
					result.append(aux)
				else:
					aux = {}
					aux['start'] = str(item.task.date_assigned)
					aux['end'] = str(item.task.task_end)
					aux['description'] = item.task.description
					aux['field'] = item.task.field.name
					aux['category'] =  item.task.category.description
					equipment = getTaskImplementMachine(item.task.id, item.id)
					if len(equipment['implement']) > 0:
						aux['machine'] = equipment['machine']
						aux['implement'] = equipment['implement']
					else:
						aux['machine'] = []
						aux['implement'] = []
					result.append(aux)
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3}) #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

#This function will return all implement and one machine of the certain employtask
def getTaskImplementMachine(taskId,EmploTaskId):
	result = {}
	implement = ImplementTask.objects.filter(task = taskId, machine_task__employee_task__id = EmploTaskId)
	tmp = []
	flag = 0
	for item in implement:
		if flag == 0:
			result['machine'] = item.machine_task.machine.qr_code
			flag += 1
		tmp.append(item.implement.qr_code)
	result['implement'] = tmp
	return result





def getAllManufacturers(request):
	each_result = {}
	result = []
	result.append({'success' : False})
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				all_manufacturers = Manufacturer.objects.filter()
				for each in all_manufacturers:
					each_result['id'] = each.id
					each_result['name'] = each.name
					result.append(each_result)
					each_result = {}
				result[0] = {'success' : True}
			except Manufacturer.DoesNotExist:
				result.append({'code' : 1}) #There is no task associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3})  #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

def getAllFields(request):
	each_result = {}
	result = []
	result.append({'success' : False})
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				all_fields = Field.objects.filter()
				for each in all_fields:
					each_result['id'] = each.id
					each_result['name'] = each.name
					each_result['organic'] = each.organic
					each_result['size'] = each.size
					result.append(each_result)
					each_result = {}
				result[0] = {'success' : True}
			except Manufacturer.DoesNotExist:
				result.append({'code' : 1}) #There is no task associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3})  #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

def validatePermission(request):
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			try:
				employee = Employee.objects.get(user = request.user)
				
				if employee.permission_level == 2:
					result['success'] = True
			except Employee.DoesNotExist:
				result['code'] = 1 #There is no shift records for this employee
		else:
			result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

def timeKeeperReportAux(attendance, finished):
	result = u''
	employee = Employee.objects.get(id = attendance['employee_id'])
	breaks = Break.objects.filter(attendance = attendance['id']).order_by('start')

	count = 1

	result += u'\tName: ' + employee.user.first_name + u' ' + employee.user.last_name + u' \t\tID: ' + employee.company_id + u'\n'
	result += u'\t\tStarted shift: ' + attendance['hour_started'].strftime("%I:%M %p") + u'\n'

	if finished:
		if breaks.count() == 0:
			result += u'No breaks reported!\n'
		else:
			for b in breaks:
				result += u'\t\t\tBreak ' + str(count) + u': ' + b.start.strftime("%I:%M %p") + u' - '
				if b.end is None:
					result += u'Not provided\n'
				else:
					now = datetime.datetime.now()
					delta = datetime.datetime.combine(now, b.end) - datetime.datetime.combine(now, b.start)
					result += b.end.strftime("%I:%M %p") + u' (' + u'{0:.2f}'.format(delta.total_seconds()/60) + u' minutes(s))\n'
				count += 1
		result += u'\t\tEnded shift: ' + attendance['hour_ended'].strftime("%I:%M %p") + u'\n'
	else:
		count = breaks.count()

		if count == 0:
			result += u'\t\t\tNo breaks reported yet.\n'
		else:
			temp = []
			first = True
			for b in reversed(breaks):
				temp2 = u'\t\t\tBreak ' + str(count) + u': ' + b.start.strftime("%I:%M %p") + u' - '
				if first:
					if b.end is None:
						temp2 += u'Ongoing or Not provided\n'
					else:
						now = datetime.datetime.now()
						delta = datetime.datetime.combine(now, b.end) - datetime.datetime.combine(now, b.start)
						temp2 += b.end.strftime("%I:%M %p") + u' (' + u'{0:.2f}'.format(delta.total_seconds()/60) + u' minute(s))\n'
					first = False
				else:
					if b.end is None:
						temp2 += u'Not provided\n'
					else:
						now = datetime.datetime.now()
						delta = datetime.datetime.combine(now, b.end) - datetime.datetime.combine(now, b.start)
						temp2 += b.end.strftime("%I:%M %p") + u' (' + u'{0:.2f}'.format(delta.total_seconds()/60) + u' minute(s))\n'
				temp.append(temp2)
				count -= 1

			for t in reversed(temp):
				result += t

		result += u'\t\tEnded shift: Ongoing or Not provided\n'
	return result

#This function generates a report for the timekeeper for the current day
#This function will also generate the body of the e-mail
def timeKeeperReport(request):
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():

			#Creating the data range to filter the attendaces
			now = datetime.datetime.now()
			start_date = datetime.datetime.combine(now, datetime.time.min)

			attendances = EmployeeAttendance.objects.filter(date__range = (start_date, now))
			#Building the body of the e-mail
			message = u'Heavy Connect TimeKeeper Report\n'
			message += u'You report includes information of ' + str(attendances.count()) + u' employees.\n'
			message += u'The period of time covered in this report starts at ' + start_date.strftime("%m/%d/%Y %I:%M %p") + u' and ends at ' + now.strftime("%m/%d/%Y %I:%M %p") + '.\n'

			finished = []
			unfinished = []

			#Splitting the attendance entries between finished and unfinished
			for attendance in attendances.values():
				if attendance['hour_ended'] is None:
					unfinished.append(attendance)
				else:
					finished.append(attendance)

			count = 1
			message += u'--------------------Ongoing Shifts (or not provided)--------------------\n'
			for i in unfinished:
				message += u'Employee ' + str(count) + ':'
				message += timeKeeperReportAux(i,False)
				message += '\n'
				count += 1

			message += u'----------------------------Complete Shifts-----------------------------\n'
			for j in finished:
				message += u'Employee ' + str(count) + ':'
				message += timeKeeperReportAux(j,True)
				message += '\n'
				count += 1

			subject = 'Heavy Connect TimeKeeper Report - ' + now.strftime("%m/%d/%Y")
			recipients = request.POST['recipients']
			email = EmailMessage(subject = subject, body = message, to = recipients, from_email = 'customersupport@heavyconnect.com', )
			if email.send(fail_silently=True) >= 1:
				result['success'] = True

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
def map(request):
    return render(request, 'manager/map.html')

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

def expandInfoBox(request):
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			try:
				employeeTask = EmployeeTask.objects.get(id = request.POST['id'])
				task = Task.objects.get(id = request.POST['id'])
				taskImplementMachine = TaskImplementMachine.objects.get(id = request.POST['id'])
				field = Field.objects.get(id = request.POST['id'])
				time_now = datetime.datetime.now();
				date = task.date
				boolean = bool(str(time_now) > str(date))
				print boolean
				if bool(str(time_now) > str(date)):
					employee = Employee.objects.get(id = employeeTask.employee_id)
					result['employee_id'] = employeeTask.employee_id
					result['hours_spent'] = employeeTask.hours_spent
					result['user.id'] = employee.user.id
					result['first_name'] = employee.user.first_name
					result['last_name'] = employee.user.last_name
					result['company_id'] = employee.company_id
					result['taskImplementMachine.id'] = taskImplementMachine.id
					result['implement.id'] = taskImplementMachine.implement.id
					result['field.id'] = field.id
				elif bool(str(time_now) < str(date)):
					result['hours_prediction'] = task.hours_prediction
				result[0] = {'success' : True}
			except DoesNotExist:
				result['code'] =  1 #There is no Implement associated with this
		else:
			result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

# Create a entry on TaskImplementMachine table and insert the following fields with information from the front-end:
# Task_id (task_id created on last sudb-page), Machine_id, Implement_id.

# Used tables: Task, TaskImplementMachine.
# def createEntryOnTaskImplementMachine(request):
# 	form = taskForm(request.POST)
# 	result = {'success' : False}

# 	taskImplementMachine = Task.objects.get(id = 1)#request.POST['id'])
# 	print "task ID: " + taskImplementMachine
# 	machine_id = form.cleaned_data['machine_id']
# 	print "machine ID: " + machine_id
# 	implement_id = form.cleaned_data['implement_id']
# 	print "implement_id: " + implement_id
# 	taskImplementMachine = TaskImplementMachine(task_id= taskImplementMachine, machine_id = machine_id, implement_id = implement_id)
# 	print TaskImplementMachine
# 	# TaskImplementMachine.save()
# 	result['success'] = True
# 	return HttpResponse(json.dumps(result),content_type='application/json')



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

def breakFormView(request):
	form = breakForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})