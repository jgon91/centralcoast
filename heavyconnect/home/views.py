from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.utils.dateformat import DateFormat
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

import json
from datetime import datetime
from datetime import date
import time

from home.forms import *
from home.models import *


def home(request):
	if request.user.is_authenticated():
		employee = Employee.objects.get(user = request.user)
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
					status = 1
					#Getting the employee that are logged in or passed in the ajax call	        
					if 'employeeId' not in request.POST:
					    employee = Employee.objects.get(user_id = request.user.id)
					else:
						employee = Employee.objects.get(user_id = request.POST['employeeId'])
						#need put this when employee is a manager
						status = 1	
					
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
					task, created = Task.objects.get_or_create(field = field, category = category, hours_prediction = hours_prediction, description = description, passes = passes, date_assigned = date, status = status)
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


def createShift(employee, result):
	now = datetime.datetime.now()
	eAttendance = EmployeeAttendance(employee = employee, date = now, hour_started = now)
	eAttendance.save()
	result['success'] = True
	# result['hour_started'] = str(eAttendance.hour_started)

	return result

def startShift(idUser):
	result = {'success' : False}
	try:
		employee = Employee.objects.get(user_id = idUser)
		attendance = EmployeeAttendance.objects.filter(employee_id = employee.id).order_by('-date', '-hour_started').first()
		result['Employee'] = employee.id
		if attendance is not None:
			
			#If more than 16 hours was passed since the last shift was started we can consider that now we are creating a new shift
			time_delta = (datetime.datetime.now() - datetime.datetime.combine(attendance.date,attendance.hour_started))
			
			if ((time_delta.seconds / 3600.0) >= 16.17) or (time_delta.days >= 1):
				result = createShift(employee, result)
			else:
				#In case 16 hours haven't passed yet we need to check if the shift we get was finished or not
				if attendance.hour_ended is not None: #The last shift was finished already, so we can start a new one
					result = createShift(employee, result)
				else: #The last shift wasn't finished yet.
					result['code'] = 1 #You need to finish the shift you started already before create a new one

		else: #First time the employee will create a shift
			result = createShift(employee, result)

	except (Employee.DoesNotExist, EmployeeAttendance.DoesNotExist) as e:
		result['code'] =  2 #There is no users associated with this id

	return result

@login_required
def receiveIdShift(request):
	result = {}
	if request.method == "POST":
		if request.is_ajax():
			ids = request.POST.getlist('ids[]')
			aux = []
			for item in ids:
				aux.append(startShift(item))
			result['shifts'] = aux
		else:
			result['code'] = 5 #Use ajax to perform requests
	else:
		result['code'] = 6 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')



def stopShift(idUser):
	result = {}
	try:
		employee = Employee.objects.get(user_id = idUser)
		attendance = EmployeeAttendance.objects.filter(employee_id = employee.id).order_by('-date', '-hour_started').first()

		if attendance is not None:

			result['attendance-date'] = str(attendance.date)
			result['attendance-time'] = str(attendance.hour_started)

			#If more than 16 hours was passed since the last shift was started we can consider that now we are creating a new shift
			time_delta = (datetime.datetime.now() - datetime.datetime.combine(attendance.date,attendance.hour_started))

			if ((time_delta.seconds / 3600.0) < 16.17) or (time_delta.days == 0):
				t_break = Break.objects.filter(attendance_id = attendance).order_by('-start')
				amount = t_break.count()

				if attendance.hour_ended is None:
					for item in t_break: 
						if item.end == None: #if there is a break opened
							item.end = datetime.datetime.now()
							item.save()
						break
					attendance.hour_ended = datetime.datetime.now()
					# attendance.signature = signature
					attendance.save()
					result['success'] = True
					result['hour_ended'] = str(attendance.hour_ended)
				else:
					result['code'] = 2 #The shift for today was already finished
			else:
				result['code'] = 3 #You have not started a shift yet
		else:
			result['code'] = 3 #You have not started a shift yet
	except EmployeeAttendance.DoesNotExist:
		result['code'] = 3 #You have not started your shift yet
	except Employee.DoesNotExist:
		result['code'] = 4 #This user is not authorized to use the system
	return result

@login_required
def receiveIdStopShift(request):
	result = {}
	if request.method == "POST":
		if request.is_ajax():
			ids = request.POST.getlist('ids[]')
			aux = []
			for item in ids:
				aux.append(stopShift(item))
			result['shifts'] = aux
		else:
			result['code'] = 5 #Use ajax to perform requests
	else:
		result['code'] = 6 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')



def startBreak(idUser, paramenterlunch):
	result = {'success' : False}
	try:
		lunch = paramenterlunch
		employee = Employee.objects.get(user = idUser)

		attendance = EmployeeAttendance.objects.filter(employee_id = employee.id).order_by('-date', '-hour_started').first()
		if attendance is not None:
			if attendance.hour_ended is None:
				t_break = Break.objects.filter(attendance_id = attendance).order_by('-start')
				count = t_break.count()

				if count == 0 or t_break[0].end is not None:
					t2_break = Break(attendance = attendance, lunch = lunch, start = datetime.datetime.now())
					t2_break.save()
					result['success'] = True
					# result['time'] = str(t2_break.start)
					result['user'] = idUser
				else:
					result['code'] = 1 #You cannot start two breaks at the same time
			else:
				result['code'] = 2 #The shift for today was already finished
		else:
			result['code'] = 3 #You need to start a shift first
	except EmployeeAttendance.DoesNotExist:
		result['code'] = 3 #You need to start a shift first

	return result

@login_required
def receiveIdBreak(request):
	result = {}
	if request.method == "POST":
		if request.is_ajax():
			ids = request.POST.getlist('ids[]')
			aux = []
			lunch = int(request.POST['lunch'])
			for item in ids:
				aux.append(startBreak(item, lunch))
			result['shifts'] = aux
		else:
			result['code'] = 5 #Use ajax to perform requests
	else:
		result['code'] = 6 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')


def stopBreak(idUser, paramenterlunch):
	result = {'success' : False}
	try:
		lunch = paramenterlunch
		employee = Employee.objects.get(user_id = idUser)
		attendance = EmployeeAttendance.objects.filter(employee_id = employee.id).order_by('-date', '-hour_started').first()
		if attendance.hour_ended is None:
			t_break = Break.objects.filter(attendance_id = attendance).order_by('-start')
			count = t_break.count()
			if (count != 0) and t_break[0].end is None:
				if t_break[0].lunch == lunch:
					t_break = t_break[0]
					t_break.end = datetime.datetime.now()
					t_break.save()
					result['success'] = True
					result['user'] = idUser
					# result['time'] = str(t_break.end)
				else:
					result['code'] = 6 #The break is not compatible with the variable request.lunch
			else:
				result['code'] = 1 #You need to start a break first
		else:
			result['code'] = 2 #The shift for today was already finished
	except EmployeeAttendance.DoesNotExist:
		result['code'] = 3 #You need to start a shift first
	return result

@login_required
def receiveIdStopBreak(request):
	result = {}
	if request.method == "POST":
		if request.is_ajax():
			ids = request.POST.getlist('ids[]')
			aux = []
			lunch = int(request.POST['lunch'])
			for item in ids:
				aux.append(stopBreak(item,lunch))
			result['breaks'] = aux
		else:
			result['code'] = 5 #Use ajax to perform requests
	else:
		result['code'] = 6 #Request was not POST
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
 	if request.is_ajax():
		date = datetime.datetime.now()
		start_date = datetime.datetime.combine(date, datetime.time.min)
		end_date = datetime.datetime.combine(date, datetime.time.max)
		qr_code = request.GET['qr_code']
		try:
			machine = Machine.objects.get(qr_code = qr_code)
			result['nickname'] = machine.nickname
			result['hitch_category'] = machine.hitch_category
			result['speed_range_min'] = machine.speed_range_min
			result['speed_range_max'] = machine.speed_range_max
			result['engine_hours'] = machine.engine_hours
			result['base_cost'] = machine.base_cost
			result['machine_type'] = str(machine.m_type)
			result['front_tires'] = machine.front_tires
			result['rear_tires'] = machine.rear_tires
			result['steering'] = machine.steering
			result['operator_station'] = machine.operator_station
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
			emploTask = EmployeeTask.objects.filter(task__status = 4, start_time__range = (start_date,end_date)).order_by('-start_time') #just task active and with the today date
			control = 0
			for item in emploTask:
				implement = ImplementTask.objects.filter(task__id = item.task.id, machine_task__machine__id = machine.id).order_by('-machine_task__employee_task__start_time')
				if len(implement) != 0:
					temp = []
					for doc in implement:
						temp.append((doc.implement.equipment_type.name))
						if control < doc.machine_task.id:
							control = doc.machine_task.id
							result['employee'] = doc.machine_task.employee_task.employee.user.first_name + " " + doc.machine_task.employee_task.employee.user.last_name
							result['task'] = doc.task.category.description
					result['implement'] = temp
					break
			result['success'] = True
		except Machine.DoesNotExist:
			try:
				implement = Implement.objects.get(qr_code = qr_code)
				result['nickname'] = implement.nickname
				result['hitch_category'] = implement.hitch_category
				result['speed_range_min'] = implement.speed_range_min
				result['speed_range_max'] = implement.speed_range_max
				result['base_cost'] = implement.base_cost
				# result['equipment_type'] = str(implement.equipment_type)
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
				emploTask = EmployeeTask.objects.filter(task__status = 4, start_time__range = (start_date,end_date)).order_by('-start_time') #just task active and with the today date
				control = 0
				for item in emploTask:
					impementTask = ImplementTask.objects.filter(task__id = item.task.id, implement__id = implement.id).order_by('-machine_task__employee_task__start_time')[:1]
					for item2 in impementTask:
						impleTask = ImplementTask.objects.filter(machine_task__id = item2.machine_task.id)
						if len(impleTask) != 0:
							temp = []
							for doc in impleTask:
								if implement.id != doc.implement.id:
									temp.append((doc.implement.equipment_type.name))
								if control < doc.machine_task.id:
									control = doc.machine_task.id
									result['machine'] = doc.machine_task.machine.qr_code
									result['employee'] = doc.machine_task.employee_task.employee.user.first_name + " " + doc.machine_task.employee_task.employee.user.last_name
									result['task'] = doc.task.category.description
							result['implement'] = temp
				result['success'] = True
			except Implement.DoesNotExist:
				result['code'] = 1 #There is no equipment associated with this
 	else:
 		result['code'] = 2 #Use ajax to perform requests
	return HttpResponse(json.dumps(result),content_type='application/json')



# Driver 6.3.1.3
# It will retrieve id + description of all task categories in database.
def getAllTaskCategory(request):
	each_result = {}
	result = {'success' : False}

	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				all_task_category = TaskCategory.objects.filter()
				taskCategorys = []
				for each in all_task_category:
					each_result['id'] = each.id
					each_result['description'] = each.description
					taskCategorys.append(each_result)
					each_result = {}
				result['success'] = True
				result['taskCategorys'] = taskCategorys
			except TaskCategory.DoesNotExist:
				result['code'] = 1 #There is no task associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3  #Request was not POST
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
# machine_qr_code, implement_qr_code, task_category,
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
						implementTask = ImplementTask.objects.filter(task__id = task_id)
						try: # Check if task is added on EmployeeTask table
							employeeTask = EmployeeTask.objects.get(task__id = task_id)
							result['implement1_nickname'] = implementTask[0].implement.nickname
							result['implement1_photo'] = implementTask[0].implement.photo
							result['implement1_model'] = implementTask[0].implement.manufacturer_model.manufacturer.name
							result['implement1_qr_code'] = implementTask[0].implement.qr_code
							if len(implementTask) == 2:
								result['implement2_nickname'] = implementTask[1].implement.nickname
								result['implement2_photo'] = implementTask[1].implement.photo
								result['implement2_model'] = implementTask[1].implement.manufacturer_model.manufacturer.name
								result['implement2_qr_code'] = implementTask[1].implement.qr_code
							result['employee'] = str(employeeTask.employee.user.first_name)+' '+str(employeeTask.employee.user.last_name)
							result['field'] = task.field.name
							result['category'] = task.category.description
							result['description'] = task.description
							result['machine_nickname'] = machineTask.machine.nickname
							result['machine_photo'] = machineTask.machine.photo
							result['machine_qr_code'] = machineTask.machine.qr_code
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
  	if not request.method == 'POST':
 		if not request.is_ajax():
 			try:
				machine = Machine.objects.get(qr_code = '987654k')#request.POST['qr_code'])
				result['qr_code'] = machine.qr_code
				result['manufacture'] = machine.manufacturer_model.manufacturer.name
				result['serial'] = machine.serial_number
				result['status'] = machine.status
				result['model'] = machine.manufacturer_model.model
				result['asset_number'] = machine.asset_number
				result['horsepower'] = machine.horsepower
				result['hitch_capacity'] = machine.hitch_capacity
				result['hitch_category'] = str(machine.hitch_category)
				result['drawbar_category'] = machine.drawbar_category
				result['speed_range_min'] = machine.speed_range_min
				result['speed_range_max'] = machine.speed_range_max
				result['year_purchased'] = machine.year_purchased
				result['engine_hours'] = machine.engine_hours
				result['base_cost'] = str(machine.base_cost)
				result['m_type'] = machine.m_type
				result['front_tires'] = machine.front_tires
				result['rear_tires'] = machine.rear_tires
				result['steering'] = machine.steering
				result['operator_station'] = machine.operator_station
				result['hour_cost'] = machine.hour_cost
				result['photo'] = machine.photo
				result['photo1'] = machine.photo1
				result['photo2'] = machine.photo2
				result['nickname'] = machine.nickname
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
# Attention: This function will return only machines with desired status passed as argument.
# It expects status_ok=True, status_attention=False, and so on.
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
					try:
						implement = Implement.objects.get(qr_code = implement_qr_code)
						machine2 = machine.exclude(hitch_capacity__lt = implement.hitch_capacity_req)													# Remove Machine with less hitch_capacity
						machine3 = machine2.exclude(horsepower__lt = implement.horse_power_req)															# Remove Machine with less horse_power
						machine2 = machine3.exclude(hitch_category__gt = implement.hitch_category).exclude(hitch_category__lt = implement.hitch_category)# Remove Machine with different hitch_category
						machine = machine2.exclude(drawbar_category__gt = implement.drawbar_category).exclude(drawbar_category__lt = implement.drawbar_category)# Remove M different drawbar_category
					except Implement.DoesNotExist:
						result.append({'error' : 'Implement passed does not exist'}) #There is no users associated with this:
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
# Attention: This function will return only machines with desired status passed as argument.
# It expects status_ok=True, status_attention=False, and so on.
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
					try:
						machine = Machine.objects.get(qr_code = machine_qr_code)
						implement2 = implement.exclude(hitch_capacity_req__gt = machine.hitch_capacity)		# Remove Implement with more hitch_capacity req
						implement3 = implement2.exclude(horse_power_req__gt = machine.horsepower)			# Remove Implement with more horse_power req
						implement2 = implement3.exclude(hitch_category__gt = machine.hitch_category).exclude(hitch_category__lt = machine.hitch_category)	# Remove I different hitch_category
						implement = implement2.exclude(drawbar_category__gt = machine.drawbar_category).exclude(drawbar_category__lt = machine.drawbar_category)# Remove I different drawbar_category
					except Machine.DoesNotExist:
						result.append({'error' : 'Machine passed does not exist'}) #There is no users associated with this
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
			except Implement.DoesNotExist:
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




# Return pending tasks, which are tasks that have "approved" status or "paused" 
# status (not "pending" status. This would be waiting for Manager approval)
@login_required
def retrievePendingTask(request):
	result = {'success' : False}
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				aux = {}
				off = int(request.POST['offset'])
				limit = int(request.POST['limit'])
				# Filter EmployeeTask by user and order by assigned date
				emploTask   =  EmployeeTask.objects.order_by('task__date_assigned').filter(employee__user__id = request.user.id)
				# Remove invalid status, letting just tasks with status "Approved" (2) and "Paused" (5)
				emploTask = emploTask.exclude(task__status = 1)
				emploTask = emploTask.exclude(task__status = 3)
				emploTask = emploTask.exclude(task__status = 4)
				emploTask = emploTask.exclude(task__status = 6)
				# Limit by the range passed by the Fron-End (limit and off)
				emploTask = emploTask[off:limit+off]

				each_task_info = []
				for item in emploTask:
					aux['category'] = item.task.category.description
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
						# If task uses more the one implement it will retrieve all. If It just have one, return the only one
						aux2 = {}
						aux_implement = []
						implementTask = ImplementTask.objects.filter(task__id = item.task.id)
						for each_implement in implementTask:
							aux2['implement_model'] = each_implement.implement.manufacturer_model.model
							aux2['implement_nickname'] = each_implement.implement.nickname
							aux2['implement_id'] = each_implement.implement.id
							aux_implement.append(aux2)
							aux2 = {}
						aux['implement'] = aux_implement
					except ImplementTask.DoesNotExist:
						aux['implement'] = "NONE"					
					each_task_info.append(aux)
					aux = {}
				result['each_task_info'] = each_task_info
				result['success'] = True
			except EmployeeTask.DoesNotExist:
				result['code'] = 1 #There is no Implement associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')



##Return task that are not complished until today, the number of task returned is according to the number n
@login_required
def pastTaskList(request):
	result = {'success' : False}
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				aux = {}
				off = int(request.POST['offset'])
				limit = int(request.POST['limit'])
				# Filter EmployeeTask by user and status task == Finished
				emploTask   =  EmployeeTask.objects.order_by('-end_time').filter(employee__user__id = request.user.id, task__status = 6)[off:limit+off]

				each_task_info = []
				for item in emploTask:
					aux['category'] = item.task.description
					aux['field'] = item.task.field.name
					aux['date'] = str(item.start_time)
					aux['description'] = item.task.description
					# Calculate the duratio of the task based on EmployeeTask table (not in Task table)
					duration = datetime.timedelta( hours = item.end_time.hour - item.start_time.hour,
													minutes = item.end_time.minute - item.start_time.minute,
													seconds=item.end_time.second - item.start_time.second)
					# If work is overnight, is treats the "-1 day" that will appear in string "duration"
					if "day" in str(duration):
						duration = str(duration)[7:] 
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
						# If task uses more the one implement it will retrieve all. If It just have one, return the only one
						aux2 = {}
						aux_implement = []
						implementTask = ImplementTask.objects.filter(task__id = item.task.id)
						for each_implement in implementTask:
							aux2['implement_model'] = each_implement.implement.manufacturer_model.model
							aux2['implement_nickname'] = each_implement.implement.nickname
							aux2['implement_id'] = each_implement.implement.id
							aux_implement.append(aux2)
							aux2 = {}
						aux['implement'] = aux_implement
					except ImplementTask.DoesNotExist:
						aux['implement'] = "NONE"
					each_task_info.append(aux)
					aux = {}
				result['each_task_info'] = each_task_info
				result['success'] = True
			except EmployeeTask.DoesNotExist:
				result['code'] = 1#There is no Implement associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
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

@login_required
def getEmployeeSelfCurrentTask(request):
	result = {}
	result['success'] = False
	if request.method == 'POST':
		if request.is_ajax():
			try:
				employeeTask = EmployeeTask.objects.filter(employee__user__id = request.user.id, task__status = 4).order_by('-start_time')
				for item in employeeTask:
					if item.end_time is None:
						result['task_id'] = item.task.id
						result['task_description'] = item.task.description
						result['category'] = item.task.category.description
						result['field'] = item.task.field.name
						result['success'] = True
						equipment = getTaskImplementMachine(item.task.id, item.id)
						if len(equipment['implement']) > 0:
							result['machine'] = equipment['machine']
							result['implement'] = equipment['implement']
					elif item.start_time > item.end_time:
						result['task_id'] = item.task.id
						result['task_description'] = item.task.description
						result['category'] = item.task.category.description
						result['field'] = item.task.field.name
						result['success'] = True
						equipment = getTaskImplementMachine(item.task.id, item.id)
						if len(equipment['implement']) > 0:
							result['machine'] = equipment['machine']
							result['implement'] = equipment['implement']
			except Employee.DoesNotExist:
				result['code'] = 1 #there is no Employee associated with this user.id
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

#this function will retrieve hours worked in the last atendance of the employee, with breaks times and hours worked until the break
def managerRetrieveHoursToday(request):
	result = {}
	if request.method == 'POST':
		if request.is_ajax():
			array_breaks = [] 
			date = datetime.datetime.now() #today date
			start_date = datetime.datetime.combine(date, datetime.time.min) #today date at 0:00 AM
			end_date = datetime.datetime.combine(date, datetime.time.max) # date at 11:59 PM
			employeeAttendance = EmployeeAttendance.objects.filter(employee__user__id = request.user.id, date__range = (start_date,end_date)).order_by('-hour_started')[:1]
			count = datetime.timedelta(hours = 0, minutes = 0, seconds = 0) #counter to keep all the worked hours
			keeper = datetime.timedelta(hours = 0, minutes = 0, seconds = 0) #this variable will keep the last break. It is useful when the shift is not done
			keeper2 =  datetime.timedelta(hours = 23, minutes = 59, seconds = 59) # when the break is on another day
			for item in employeeAttendance:
				breaks = Break.objects.filter(attendance__id = item.id)
				breakDuration = datetime.timedelta(hours = 0, minutes = 0, seconds = 0) #variable used to decrease time from the total when one break still going on
				breakTime = datetime.timedelta(hours = item.hour_started.hour, minutes = item.hour_started.minute, seconds = item.hour_started.second) #help to calculate work time between breaks
				time_aux = datetime.timedelta(hours = item.hour_started.hour, minutes = item.hour_started.minute, seconds = item.hour_started.second) #variable used to remove second of the date
				atten_start = datetime.timedelta(hours = item.hour_started.hour, minutes = item.hour_started.minute,seconds = item.hour_started.second)
				for doc in breaks:
					aux = {} #puts breakStart, breakDuration and workBreak together
					docStart = datetime.timedelta(hours = doc.start.hour, minutes = doc.start.minute, seconds = doc.start.second)
					hours, remainder = divmod(docStart.seconds, 3600)
					minutes, seconds = divmod(remainder, 60) 
					aux['breakStart'] = str(hours) + ':' + str(minutes) #time that the break started
					if breakTime <= docStart:
						time_aux = docStart - breakTime
						hours, remainder = divmod(time_aux.seconds, 3600)
						minutes, seconds = divmod(remainder, 60) 
						aux['workBreak'] = str(hours) + ':' + str(minutes)
						count += docStart - breakTime
					else: #Midnight is between these times
						time_aux = (keeper2 - breakTime) + docStart
						hours, remainder = divmod(time_aux.seconds, 3600)
						minutes, seconds = divmod(remainder, 60) 
						aux['workBreak'] = str(hours) + ':' + str(minutes)
						count += (keeper2 - breakTime) + docStart
					if (doc.end != None):
						docEnd = datetime.timedelta(hours = doc.end.hour, minutes = doc.end.minute, seconds = doc.end.second)
						hours, remainder = divmod(docEnd.seconds, 3600)
						minutes, seconds = divmod(remainder, 60) 
						aux['breakStop'] = str(hours) + ':' + str(minutes)
						breakTime = docEnd
						if docEnd >= docStart:
							time_aux = docEnd - docStart
							hours, remainder = divmod(time_aux.seconds, 3600)
							minutes, seconds = divmod(remainder, 60) 
							aux['breakDuration'] = str(hours) + ':' + str(minutes)
						else: #in case of start and end are in different days, passing by midnight
							time_aux = (keeper2 - docStart) + docEnd
							hours, remainder = divmod(time_aux.seconds, 3600)
							minutes, seconds = divmod(remainder, 60)
							aux['breakDuration'] = str(hours) + ':' + str(minutes)
					else:
						aux['breakStop'] = 'Happening'
						time_now = datetime.datetime.now() #variable used to get the current time
						time_aux = datetime.timedelta(hours = time_now.hour, minutes = time_now.minute, seconds = time_now.second)
						breakTime = docStart
						if time_aux >= docStart:
							breakDuration = time_aux - docStart
							aux['breakDuration'] = str(breakDuration)
						else:
							breakDuration = (keeper2 - docStart) + time_aux
							aux['breakDuration'] = str(breakDuration)
					aux['lunch'] = doc.lunch
					array_breaks.append(aux)
				if item.hour_ended != None:
					endTurn = datetime.timedelta(hours = item.hour_ended.hour, minutes = item.hour_ended.minute, seconds = item.hour_ended.second)
					Attendance_end =  datetime.timedelta(hours = item.hour_ended.hour, minutes = item.hour_ended.minute, seconds = item.hour_ended.second)
					if endTurn >= breakTime:
						count += endTurn - breakTime
					else:
						count += (keeper2 - breakTime) + endTurn
				else:
					Attendance_end = 'Happening'
					time_now = datetime.datetime.now()
					time_aux = datetime.timedelta(hours = time_now.hour, minutes = time_now.minute, seconds = time_now.second)
					if time_aux >= breakTime:
						count += (time_aux - breakTime) - breakDuration
					else:
						count += ((keeper2 - breakTime) + time_aux) - breakDuration		
			hours, remainder = divmod(count.seconds, 3600)
			minutes, seconds = divmod(remainder, 60)
			result['Total'] = str(hours) + ':' + str(minutes)
			hours, remainder = divmod(atten_start.seconds, 3600)
			minutes, seconds = divmod(remainder, 60)
			result['Attendance_start'] = str(hours) + ':' + str(minutes)
			if(Attendance_end != 'Happening'):
				hours, remainder = divmod(Attendance_end.seconds, 3600)
				minutes, seconds = divmod(remainder, 60)
				result['Attendance_end'] = str(hours) + ':' + str(minutes)
			else:
				result['Attendance_end'] = Attendance_end
			result['breaks'] = array_breaks
		else:
			result['Code'] = {'Code' : 1} #request is not ajax
	else:
		result['Code'] = {'Code' : 2} #request is not post
	return HttpResponse(json.dumps(result),content_type='application/json')

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
				
				result['first_name'] = employee.user.first_name
				result['last_name'] = employee.user.last_name
				result['qr_code'] = employee.qr_code
				result['contact_number'] = employee. contact_number
				result['permission_level'] = employee.permission_level
				result['photo_url'] = employee.photo

				attendance = EmployeeAttendance.objects.filter(employee = employee).order_by('-date').first()

				if attendance is not None:
					time_delta = (datetime.datetime.now() - datetime.datetime.combine(attendance.date,attendance.hour_started))
					if ((time_delta.seconds / 3600.0) >= 16.17) or (time_delta.days >=1):
						result['hour_started'] = 'None'
						result['hour_ended'] = 'None'
						result['breaks'] = []
					else:
						result['hour_started'] = str(attendance.hour_started)
						result['hour_ended'] = str(attendance.hour_ended)
						breaks = Break.objects.filter(attendance = attendance).order_by('start').values()


						temp = []
						for item in breaks:
							temp.append((str(item['start']),str(item['end']),(item['lunch'])))

						result['breaks'] = temp
				else:
					result['hour_started'] = 'None'
					result['hour_ended'] = 'None'
					result['breaks'] = []
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
	color = ['#F7F003','#05C60E', '#FF0000', '#B3D1FF','#FF6600', '#A2A9AF']
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
					aux['task_id'] = item.task.id
					aux['status'] = item.task.status
					aux['description'] = item.task.description
					aux['field'] = item.task.field.name
					aux['category'] =  item.task.category.description
					aux['color'] = color[item.task.status - 1]
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
					aux['task_id'] = item.task.id
					aux['status'] = item.task.status
					aux['description'] = item.task.description
					aux['field'] = item.task.field.name
					aux['category'] =  item.task.category.description
					aux['color'] = color[item.task.status - 1]
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


### This function will retorn one string which will refer one color in hexadecimal
def getColor(number):
	colors = ['#85ACFF',  '#7AEFBD', '#F2F472', '#FF0000', '#8AF45C', '#7AD9EF', '#FA5AEF', '#F9B76B', '#FF7979', '#B93CF4', '#9370DB', '#FF1493', '#8B0000', '#00CED1',
	 '#8B0000', '#FF8C00', '#00FA9A', '#F0E68C', '#DAA520', '#808080', '#8A2BE2', '#191970', '#FF69B4', '#40E0D0', '#B22222', '#00FF7F', '#B8860B', '#000080', '#4B0082', '#C71585',
	  '#48D1CC', '#A52A2A', '#90EE90', '#8B4513', '#9400D3', '#0000CD', '#F08080', '#20B2AA', '#FA8072', '#8FBC8F', '#A0522D', '#4169E1', '#800080', '#008B8B', '#E9967A', '#006400', '#CD853F',
	   '#228B22', '#00FF00', '#8B008B', '#1E90FF', '#F08080', '#87CEFA', '#DC143C', '#4682B4', '#FF6347', '#556B2F', '#F4A460' ]
	
	value = number % 58
	
	return colors[value]



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
	result = {'success' : False}

	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				all_manufacturers = Manufacturer.objects.filter()
				manufactures = []
				for each in all_manufacturers:
					each_result['id'] = each.id
					each_result['name'] = each.name
					manufactures.append(each_result)
					each_result = {}
				result['success'] = True
				result['manufactures'] = manufactures
			except Manufacturer.DoesNotExist:
				result['code'] = 1 #There is no Manufacurer in this system
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

def getAllFields(request):
	each_result = {}
	result = {'success' : False}

	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				all_fields = Field.objects.filter()
				fields = []
				for each in all_fields:
					each_result['id'] = each.id
					each_result['name'] = each.name
					each_result['organic'] = each.organic
					each_result['size'] = each.size
					fields.append(each_result)
					each_result = {}
				result['success'] = True
				result['fields'] = fields
			except Field.DoesNotExist:
				result['code'] = 1 #There is no task associated with this
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else:
	 	result['code'] = 3  #Request was not POST
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


def getEmployeeScheduleManager(request):
	print "It is here 2"
	result = []
	color = ['#F7F003','#05C60E', '#FF0000', '#B3D1FF','#FF6600', '#A2A9AF']
	if request.method == 'GET':
		if request.is_ajax():
			print "It is here 3"
			aux = request.GET['start'] #get the date in the POST request
			aux2 = request.GET['end']
			date_start = datetime.datetime.strptime(aux, '%Y-%m-%d')
			date_end = datetime.datetime.strptime(aux2, '%Y-%m-%d') + datetime.timedelta(days = 1)
			date_end = datetime.datetime.combine(date_end, datetime.time.max)
			emplo = Employee.objects.filter(manager__user_id = request.user.id)
			for item in emplo: #this for will get all the employees received
				emploTask = EmployeeTask.objects.filter(employee__user__id = item.user.id, task__date_assigned__range = (date_start, date_end))
				for taskEmplo in emploTask: #it will take care of every task in that time
					if taskEmplo.task.status != 6:
						aux = {}
						auxHour = int(taskEmplo.task.hours_prediction)
						auxMin = float(taskEmplo.task.hours_prediction - auxHour) * 60
						data_prediction = taskEmplo.task.date_assigned + datetime.timedelta(hours = auxHour, minutes = auxMin)
						equipment = getTaskImplementMachine(taskEmplo.task.id, taskEmplo.id)
						aux['employee'] = taskEmplo.employee.user.first_name + " " + taskEmplo.employee.user.last_name
						aux['title'] = aux['employee']
						aux['start'] = str(taskEmplo.task.date_assigned)
						aux['end'] = str(data_prediction)
						aux['task_id'] = taskEmplo.task.id
						aux['status'] = taskEmplo.task.status
						aux['description'] = taskEmplo.task.description
						aux['field'] = taskEmplo.task.field.name
						aux['category'] =  taskEmplo.task.category.description
						aux['color'] = color[taskEmplo.task.status - 1]
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
	 	result.append({'code' : 3}) #Request was not GET
	return HttpResponse(json.dumps(result),content_type='application/json')

### Function to retrieve tasks by employee id
def getEmployeeTaskManager(request):
	result = []
	color = ['#F7F003','#05C60E', '#FF0000', '#B3D1FF','#FF6600', '#A2A9AF']
	if request.method == 'GET':
		if request.is_ajax():
			aux = request.GET['start'] #get the date in the POST request
			aux2 = request.GET['end']
			emplo = request.GET.getlist('optionsSearch[]')
			condition = int(request.GET['condition'])
			date_start = datetime.datetime.strptime(aux, '%Y-%m-%d')
			date_end = datetime.datetime.strptime(aux2, '%Y-%m-%d') + datetime.timedelta(days = 1)
			date_end = datetime.datetime.combine(date_end, datetime.time.max)
			if(condition == 0):
				tasks = EmployeeTask.objects.filter(employee__user__id__in = emplo, task__date_assigned__range = (date_start, date_end))
				for item1 in tasks:
					if item1.task.status != 6:
						aux = {}
						auxHour = int(item1.task.hours_prediction)
						auxMin = float(item1.task.hours_prediction - auxHour) * 60
						data_prediction = item1.task.date_assigned + datetime.timedelta(hours = auxHour, minutes = auxMin)
						equipment = getTaskImplementMachine(item1.task.id, item1.id)
						aux['employee'] = item1.employee.user.first_name + " " + item1.employee.user.last_name
						aux['title'] = aux['employee']
						aux['start'] = str(item1.task.date_assigned)
						aux['end'] = str(data_prediction)
						aux['task_id'] = item1.task.id
						aux['status'] = item1.task.status
						aux['description'] = item1.task.description
						aux['field'] = item1.task.field.name
						aux['category'] =  item1.task.category.description
						aux['color'] = color[item1.task.status - 1]
						if len(equipment['implement']) > 0:
							aux['machine'] = equipment['machine']
							aux['implement'] = equipment['implement']
						else:
							aux['machine'] = []
							aux['implement'] = []
						result.append(aux)
			else:
				tasks = EmployeeTask.objects.filter(employee__user__id__in = emplo, task__date_assigned__range = (date_start, date_end), task__status = condition)
				for item1 in tasks:
					aux = {}
					auxHour = int(item1.task.hours_prediction)
					auxMin = float(item1.task.hours_prediction - auxHour) * 60
					data_prediction = item1.task.date_assigned + datetime.timedelta(hours = auxHour, minutes = auxMin)
					equipment = getTaskImplementMachine(item1.task.id, item1.id)
					aux['employee'] = item1.employee.user.first_name + " " + item1.employee.user.last_name
					aux['title'] = aux['employee']
					aux['start'] = str(item1.task.date_assigned)
					aux['end'] = str(data_prediction)
					aux['task_id'] = item1.task.id
					aux['status'] = item1.task.status
					aux['description'] = item1.task.description
					aux['field'] = item1.task.field.name
					aux['category'] =  item1.task.category.description
					aux['color'] = color[item1.task.status - 1]
					if len(equipment['implement']) > 0:
						aux['machine'] = equipment['machine']
						aux['implement'] = equipment['implement']
					else:
						aux['machine'] = []
						aux['implement'] = []
					result.append(aux)
					print "Result: "
					print result
		else:
			print "test 4"
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
		print "test 5"
	 	result.append({'code' : 3}) #Request was not GET
	return HttpResponse(json.dumps(result),content_type='application/json')


### Function to retrieve tasks by field ###
def getFieldTasksManager(request):
	print "It is here 2.2"
	result = []
	if request.method == 'GET':
		if request.is_ajax():
			color = 0
			control = {} #this dicionary will keep all fields and it colors
			taskStatus = 0;
			aux = request.GET['start'] #get the date in the POST request
			aux2 = request.GET['end']	
			date_start = datetime.datetime.strptime(aux, '%Y-%m-%d')
			date_end = datetime.datetime.strptime(aux2, '%Y-%m-%d') + datetime.timedelta(days = 1)	
			date_end = datetime.datetime.combine(date_end, datetime.time.max)
			condition = int(request.GET['condition'])
			emplo = Employee.objects.filter(manager__user_id = request.user.id)
			if(condition == 0): #It depends on the filter
				for item in emplo: 
					emploTask = EmployeeTask.objects.filter(employee__user__id = item.user.id, task__date_assigned__range = (date_start, date_end))
					for taskEmplo in emploTask:
						if taskEmplo.task.status != 6:
							aux = {}
							auxHour = int(taskEmplo.task.hours_prediction)
							auxMin = float(taskEmplo.task.hours_prediction - auxHour) * 60
							data_prediction = taskEmplo.task.date_assigned + datetime.timedelta(hours = auxHour, minutes = auxMin)
							equipment = getTaskImplementMachine(taskEmplo.task.id, taskEmplo.id)
							aux['employee'] = taskEmplo.employee.user.first_name + " " + taskEmplo.employee.user.last_name
							aux['start'] = str(taskEmplo.task.date_assigned)
							aux['end'] = str(data_prediction)
							aux['task_id'] = taskEmplo.task.id
							aux['status'] = taskEmplo.task.status
							aux['description'] = taskEmplo.task.description
							aux['field'] = taskEmplo.task.field.name
							aux['title'] = aux['field']
							aux['category'] =  taskEmplo.task.category.description
							if not taskEmplo.task.field.name in control:
								control[taskEmplo.task.field.name] = color
								color += 1
							aux['color'] = getColor(control[taskEmplo.task.field.name])
							if len(equipment['implement']) > 0:
								aux['machine'] = equipment['machine']
								aux['implement'] = equipment['implement']
							else:
								aux['machine'] = []
								aux['implement'] = []
							result.append(aux)
			else:
				for item in emplo: 
					emploTask = EmployeeTask.objects.filter(employee__user__id = item.user.id, task__date_assigned__range = (date_start, date_end))
					for taskEmplo in emploTask:
						if taskEmplo.task.status == condition:
							aux = {}
							auxHour = int(taskEmplo.task.hours_prediction)
							auxMin = float(taskEmplo.task.hours_prediction - auxHour) * 60
							data_prediction = taskEmplo.task.date_assigned + datetime.timedelta(hours = auxHour, minutes = auxMin)
							equipment = getTaskImplementMachine(taskEmplo.task.id, taskEmplo.id)
							aux['employee'] = taskEmplo.employee.user.first_name + " " + taskEmplo.employee.user.last_name
							aux['title'] = aux['employee']
							aux['start'] = str(taskEmplo.task.date_assigned)
							aux['end'] = str(data_prediction)
							aux['task_id'] = taskEmplo.task.id
							aux['status'] = taskEmplo.task.status
							aux['description'] = taskEmplo.task.description
							aux['field'] = taskEmplo.task.field.name
							aux['title'] = aux['field']
							aux['category'] =  taskEmplo.task.category.description
							if not taskEmplo.task.field.name in control:
								control[taskEmplo.task.field.name] = color
								color += 1
							aux['color'] = getColor(control[taskEmplo.task.field.name])
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
	 	result.append({'code' : 3}) #Request was not GET

	return HttpResponse(json.dumps(result),content_type='application/json')
### end ###

@login_required
def getFieldTaskNameManager(request):
	result = []
	if request.method == 'GET':
		if request.is_ajax():
			flag = 0
			color = 0
			control = {} #this dicionary will keep all fields and it colors
			taskStatus = 0;
			fields = request.GET.getlist('optionsSearch[]')
			print fields
			aux = request.GET['start'] #get the date in the POST request
			aux1 = request.GET['end']	
			date_start = datetime.datetime.strptime(aux, '%Y-%m-%d')
			date_end = datetime.datetime.strptime(aux1, '%Y-%m-%d') + datetime.timedelta(days = 1)
			date_end = datetime.datetime.combine(date_end, datetime.time.max)
			condition = int(request.GET['condition'])
			emplo = Employee.objects.filter(manager__user_id = request.user.id)
			if(condition == 0): #It depends on the filter
				for item in emplo:
					tasks = EmployeeTask.objects.filter(employee__id = item.id, task__field__id__in = fields, task__date_assigned__range = (date_start, date_end))
					for item1 in tasks:
						aux = {}
						auxHour = int(item1.task.hours_prediction)
						auxMin = float(item1.task.hours_prediction - auxHour) * 60
						data_prediction = item1.task.date_assigned + datetime.timedelta(hours = auxHour, minutes = auxMin)
						equipment = getTaskImplementMachine(item1.task.id, item1.id)
						aux['employee'] = item1.employee.user.first_name + " " + item1.employee.user.last_name
						aux['field'] = str(item1.task.field.name)
						aux['title'] = aux['field']
						aux['category'] =  item1.task.category.description
						aux['start'] = str(item1.task.date_assigned)
						aux['description'] = item1.task.description
						aux['task_id'] = item1.task.id
						aux['status'] = item1.task.status
						aux['end'] = str(data_prediction)
						if not item1.task.field.name in control:
							control[item1.task.field.name] = color
							color += 1
						aux['color'] = getColor(control[item1.task.field.name])
						if len(equipment['implement']) > 0:
							aux['machine'] = equipment['machine']
							aux['implement'] = equipment['implement']
						else:
							aux['machine'] = []
							aux['implement'] = []
						result.append(aux)
			else:
				for item in emplo:
					tasks = EmployeeTask.objects.filter(employee__id = item.id, task__field__id__in = fields, task__date_assigned__range = (date_start, date_end))
					for item1 in tasks:
						if item1.task.status == condition:
							aux = {}
							auxHour = int(item1.task.hours_prediction)
							auxMin = float(item1.task.hours_prediction - auxHour) * 60
							data_prediction = item1.task.date_assigned + datetime.timedelta(hours = auxHour, minutes = auxMin)
							equipment = getTaskImplementMachine(item1.task.id, item1.id)
							aux['employee'] = item1.employee.user.first_name + " " + item1.employee.user.last_name
							aux['field'] = str(item1.task.field.name)
							aux['title'] = aux['field']
							aux['category'] =  item1.task.category.description
							aux['start'] = str(item1.task.date_assigned)
							aux['description'] = item1.task.description
							aux['task_id'] = item1.task.id
							aux['status'] = item1.task.status
							aux['end'] = str(data_prediction)
							if not item1.task.field.name in control:
								control[item1.task.field.name] = color
								color += 1
							aux['color'] = getColor(control[item1.task.field.name])
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
		result.append({'code' : 3}) #Request was not GET
	return HttpResponse(json.dumps(result),content_type='application/json')

funtions = {1 :  getEmployeeScheduleManager,2 : getFieldTasksManager, 3 : getFieldTaskNameManager, 4 : getEmployeeTaskManager}
	### This function will choose which function to call
def switchTaskManager(request):
	print "It is here  " + request.GET['search'] + request.GET['condition']
	search = int(request.GET['search'])
	return funtions[search](request)


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

def beaconUpdate(request):
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			form = beaconForm(request.POST)
			if form.is_valid():
				beacon = form.cleaned_data['beacon']
				timestamp = form.cleaned_data['timestamp']
				latitude = form.cleaned_data['latitude']
				longitude = form.cleaned_data['longitude']
				gps, created = GPS.objects.get_or_create(latitude = latitude, longitude = longitude)
				bgps = BeaconGPS(beacon = beacon, gps = gps, timestamp = timestamp)
				bgps.save()
				result['success'] = True
			else:
				result['code'] = 1 #Use ajax to perform requests
				result['errorString'] = 'Not all data is valid'
				result['errors'] = form.errors
		else:
			result['code'] = 2 #Use ajax to perform requests
			result['errorString'] = 'Use ajax to perform requests'
	else:
		result['code'] = 3 #Request was not POST
		result['errorString'] = 'Request was not POST, your sent a ' + str(request.method)

	return HttpResponse(json.dumps(result),content_type='application/json')

#this function gives back the last localization of the equipment
def equipmentLastLocalization(request):
	result = {'success' : False}
	if request.method == 'POST':
		qr_code = request.POST['qr_code']
		if request.is_ajax():
			try:
				machine = Machine.objects.get(qr_code = qr_code)
				beaconGPS = BeaconGPS.objects.filter(beacon__id = machine.beacon.id).order_by('-timestamp')[:1]
				for item in beaconGPS:
					result['latitude'] = item.gps.latitude
					result['longitude'] = item.gps.longitude
					result['status'] = machine.status
				result['success'] = True
			except:
				try:
					implement = Implement.objects.get(qr_code = qr_code)
					beaconGPS = BeaconGPS.objects.filter(beacon__id = implement.beacon.id).order_by('-timestamp')[:1]
					for item in beaconGPS:
						result['latitude'] = item.gps.latitude
						result['longitude'] = item.gps.longitude
						result['status'] = implement.status
					result['success'] = True
				except Implement.DoesNotExist:
					result['code'] = 1
		else:
				result['code'] = 2 #Use ajax to perform requests
				result['errorString'] = 'Use ajax to perform requests'
	else:
		result['code'] = 3 #Request was not POST
		result['errorString'] = 'Request was not POST, your sent a ' + str(request.method)

	return HttpResponse(json.dumps(result),content_type='application/json')

def updateTaskCalendar(request):
	result = {'success' : False}
	if request.method == "POST":
		if request.is_ajax():
			try:
				task = Task.objects.get(id = request.POST['task_id'])
				aux = request.POST['start'] #get the date in the POST request
				aux2 = request.POST['end']
				date_start = datetime.datetime.strptime(aux, '%Y-%m-%d %H:%M:%S')
				date_end = datetime.datetime.strptime(aux2, '%Y-%m-%d %H:%M:%S')
				task.hours_prediction = abs(date_start - date_end).total_seconds() / 3600.0
				task.date_assigned = aux
				task.save()
				return render(request, 'manager/formSuccess.html')
			except:
				result['code'] = 3 #Task does not exist
		else:
			result['code'] = 2 #The request is not AJAX
	else:
		result['code'] = 1 #The request is not POST
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

def test1(request):
    return render(request, 'manager/test.html')

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
def timeKeeperGroup(request):
	return render(request, 'driver/timeKeeperGroup.html')

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
def createTaskManager(request):
    return render(request, 'manager/createTaskManager.html')
   
@login_required
def templateCreateTaskManager(request):
    return render(request, 'manager/templateCreateTaskManager.html')

@login_required
def templateAddEquipmentManager(request):
    return render(request, 'manager/templateAddEquipment.html')
   
@login_required
def scheduleManager(request):
    return render(request, 'manager/scheduleManager.html')

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
def formSuccess(request):
    return render(request, 'manager/formSuccess.html')

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

@login_required
def manageForms(request):
	return render(request, 'manager/manageForms.html')

@login_required
def listEmployee(request):
	return render(request, 'manager/listEmployee.html')

@login_required
def listMachine(request):
	return render(request, 'manager/listMachine.html')

@login_required
def listShop(request):
	return render(request, 'manager/listShop.html')

@login_required
def listRepairShop(request):
	return render(request, 'manager/listRepairShop.html')

@login_required
def listImplement(request):
	return render(request, 'manager/listImplement.html')

@login_required
def geofence(request):
	return render(request, 'geoFence.html')

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

@login_required
def storeChecklistAnswers(request):
	result = {'success' : False}
	form = storeAnswersForm(request.POST)

	if request.method == 'POST':
		if request.is_ajax():
			if form.is_valid():
				employee = Employee.objects.get(user = request.user)
				responses = form.cleaned_data['answers']
				engine_hours = form.cleaned_data['engine_hours']
				equipment = form.cleaned_data['qr_code']

				if isinstance(equipment, Machine): #If we have a machine we need to account the 
					equipment.engine_hours = engine_hours 
				elif isinstance(equipment, Implement):
					equipment.engine_hours = engine_hours 
				for r in responses:
					r.employee = employee
					if r.answer is False: #If one of the answers was no the machine will have they status changed to broken
						equipment.status = Machine.STBR
					r.save()

				equipment.save()	
				result['success'] = True
			else:
				result['code'] = 1
				result['errorString'] = form.errors
		else:
			result['code'] = 2
	else:
		result['code'] = 3

	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getChecklistEquipment(request):
	result = {'success' : False}
	form = checkListForm(request.POST)
	item = {}

	if request.method == 'POST':
		if request.is_ajax():
			if form.is_valid():
				language = request.LANGUAGE_CODE
				equipment = form.cleaned_data['qr_code']
				category = form.cleaned_data['category']
				refer = Question.NONE

				if isinstance(equipment, Machine):
					refer= Question.MACHINE
				elif isinstance(equipment, Implement):
					refer = Question.IMPLEMENT

				questions = Question.objects.filter(category = category, refers = refer).order_by('id')
				temp = []

				if 'es'in language:
					translations = TranslatedQuestion.objects.filter(idiom = TranslatedQuestion.SPANISH, question__in = questions.values('id')).order_by('question')
					for (q,t) in zip(questions,translations):
						item['id'] = q.id
						item['description'] = t.description
						temp.append(item)
						item = {}
				else: #return the questions in english by default, unless another language was requested
					for q in questions:
						item['id'] = q.id
						item['description'] = q.description
						temp.append(item)
						item = {}
				result['questions'] = temp
				result['success'] = True
			else:
				result['code'] = 2 #Not all data are valid
				result['errorString'] = form.errors
		else:
			result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getFilteredImplementWithGPS(request):
	result = []
	each_result = {}
	result.append({'success' : False})
  	if request.method == 'POST':
		# Save values from request
		manufacturer = request.POST['manufacturer']
		hitch_capacity_req = request.POST['hitch_capacity_req']
		horse_power_req = request.POST['horse_power_req']
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
		#if request.POST['status_ok'] == 'False':
		#	status_ok = 1
		#if request.POST['status_attention'] == 'False':
		#	status_attention = 2
		#if request.POST['status_broken'] == 'False':
		#	status_broken = 3
		#if request.POST['status_quarantine'] == 'False':
		#	status_quarantine = 4

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

				# Selecting which field will be retrieved to fron-end
				for each in implement:
					beacon_gps = BeaconGPS.objects.order_by('-timestamp').filter(beacon__beacon_serial = each.beacon.beacon_serial)[:1]
					each_result['beacon_latitude'] = str(beacon_gps[0].gps.latitude)
					each_result['beacon_longitude'] = str(beacon_gps[0].gps.longitude)
					each_result['timestamp'] = str(beacon_gps[0].timestamp)
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
			except Implement.DoesNotExist:
				result.append({'code' : 1}) #There is no equipment associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3}) #Request was not POST
 	return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getFilteredMachineWithGPS(request):
	result = []
	each_result = {}
	result.append({'success' : False})
  	if request.method == 'POST':
		# Save values from request
		manufacturer = request.POST['manufacturer']
		hitch_capacity = request.POST['hitch_capacity_req']
		horse_power = request.POST['horse_power_req']
		# Set minimum values in case no filters were applied for those option
		if hitch_capacity == '' or hitch_capacity == None:
			hitch_capacity = -1
		if horse_power == '' or horse_power == None:
			horse_power = -1
		# Set the correct values for all status filters
		# All status filters will receive True or False.
		#   - If False, it will change to the correct value on the database  (1, 2, 3, or 4)
		#   - If True, it will still with 0
		status_ok = 0
		status_attention = 0
		status_broken = 0
		status_quarantine = 0
		if request.POST['status_ok'] == '0':
			status_ok = 1
		if request.POST['status_attention'] == '0':
			status_attention = 2
		if request.POST['status_broken'] == '0':
			status_broken = 3
		if request.POST['status_quarantine'] == '0':
			status_quarantine = 4

	 	if not request.is_ajax():
			try:
				# Filtering by manufacturer, hitch_cap_req, horse_power_req, and status.
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

				# Selecting which field will be retrieved to fron-end
				for each in machine:
					beacon_gps = BeaconGPS.objects.order_by('-timestamp').filter(beacon__beacon_serial = each.beacon.beacon_serial)[:1]
					each_result['beacon_latitude'] = str(beacon_gps[0].gps.latitude)
					each_result['beacon_longitude'] = str(beacon_gps[0].gps.longitude)
					each_result['timestamp'] = str(beacon_gps[0].timestamp)
					each_result['qr_code'] = each.qr_code
					each_result['nickname'] = each.nickname
					each_result['photo'] = each.photo
					each_result['horsepower'] = each.horsepower
					each_result['asset_number'] = each.asset_number
					each_result['drawbar_category'] = each.drawbar_category
					each_result['status'] = each.status
					result.append(each_result)
					each_result = {}
				result[0] = {'success' : True}
			except Machine.DoesNotExist:
				result.append({'code' : 1}) #There is no equipment associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3}) #Request was not POST
 	return HttpResponse(json.dumps(result),content_type='application/json')

def saveEmployeeNotes(request):
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			try:
				employee = Employee.objects.get(id = request.POST['id'])
				employee.notes = str(request.POST['notes'])
				result['notes'] = employee.notes
				result['success'] = True
				employee.save()
			except DoesNotExist:
				result['code'] =  1 #There is no Implement associated with this
		else:
			result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')

def getFieldLocalization(request):
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			try:
				fieldLocalization = FieldLocalization.objects.filter(field_id = request.POST['id'])
				latitude = []
				longitude = []
				for each in fieldLocalization:
					latitude.append(each.gps.latitude)
					longitude.append(each.gps.longitude)
					result['name'] = each.field.name
				result['latitude'] = latitude
				result['longitude'] = longitude
				result['success'] = True
			except DoesNotExist:
				result['code'] =  1 #There is no Implement associated with this
		else:
			result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result), content_type='application/json')

@login_required
def getAllEmployees(request):
	each_result = {}
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			try:
				all_employee = Employee.objects.all()
				employees = []
				for each in all_employee:
					each_result['first_name'] = each.user.first_name
					each_result['last_name'] = each.user.last_name
					each_result['user_id'] = each.user.id					
					employees.append(each_result)
					each_result = {}
				result['success'] = True
				result['employees'] = employees				
			except DoesNotExist: #There is no employee registered
				result['code'] = 1
				return HttpResponse(json.dumps(result), content_type='application/json')
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	 		return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result['code'] = 3  #Request was not POST
		return HttpResponse(json.dumps(result), content_type='application/json')

	return HttpResponse(json.dumps(result), content_type='application/json')

@login_required
def employeeManagerDelete(request):
	result = {'success' : False}
	if request.method == "POST":
		if request.is_ajax():
			try:
				user_id = request.POST['user']
				emplo = Employee.objects.get(user_id = user_id)
				emplo.user.delete()
				emplo.delete()
				result['success'] = True;

				if result['success'] == True :
					#return HttpResponse(json.dumps(result),content_type='application/json') 
					return render(request, 'manager/formSuccess.html')
				else:
					return render(request, 'manager/formError.html')
			except:
					result['code'] = 1 #Employee does not exist
					return HttpResponse(json.dumps(result),content_type='application/json')
		else:
			result['code'] = 2 #Request is not Ajax
			return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		result['code'] = 3 #Request is not POST
		return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getAllImplements(request):
	each_result = {}
	result = {"success": True}
	if request.method == "POST":
		if request.is_ajax():
			try:
				all_implement = Implement.objects.all()
				implements = []
				for each in all_implement:
					each_result["nickname"] = each.nickname
					each_result["manufacturer_name"] = each.manufacturer_model.manufacturer.name
					each_result["manufacturer_model"] = each.manufacturer_model.model
					each_result["implement_id"] = each.id
					implements.append(each_result)
					each_result = {}
				result['success'] = True
				result['implements'] = implements
			except DoesNotExist:
				result['code'] = 1 # There is no shop registered
				return HttpResponse(json.dumps(result), content_type='application/json')
		else:
			result['code'] = 2 #Use ajax to perform requests
			return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result['code'] = 3 #Request was not POST
		return HttpResponse(json.dumps(result), content_type='application/json')

	return HttpResponse(json.dumps(result), content_type='application/json')	

@login_required
def implementManagerDelete(request):
	result = {'success' : False}
	if request.method == "POST":
		if request.is_ajax():
			try:
				implement_id = request.POST['implement_id']
				implement = Implement.objects.get(id = implement_id)
				implement.delete()
				result['success'] = True;

				if result['success'] == True :
					#return HttpResponse(json.dumps(result),content_type='application/json') 
					return render(request, 'manager/formSuccess.html')
				else:
					return render(request, 'manager/formError.html')
			except:
					result['code'] = 1 #Machine does not exist
					return HttpResponse(json.dumps(result),content_type='application/json')
		else:
			result['code'] = 2 #Request is not Ajax
			return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		result['code'] = 3 #Request is not POST
		return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getAllMachines(request):
	each_result = {}
	result = {"success": True}
	if request.method == "POST":
		if request.is_ajax():
			try:
				all_machine = Machine.objects.all()
				machines = []
				for each in all_machine:
					each_result["nickname"] = each.nickname
					each_result["manufacturer_name"] = each.manufacturer_model.manufacturer.name
					each_result["manufacturer_model"] = each.manufacturer_model.model
					each_result["machine_id"] = each.id
					machines.append(each_result)
					each_result = {}
				result['success'] = True
				result['machines'] = machines
			except DoesNotExist:
				result['code'] = 1 # There is no shop registered
				return HttpResponse(json.dumps(result), content_type='application/json')
		else:
			result['code'] = 2 #Use ajax to perform requests
			return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result['code'] = 3 #Request was not POST
		return HttpResponse(json.dumps(result), content_type='application/json')

	return HttpResponse(json.dumps(result), content_type='application/json')	

@login_required
def machineManagerDelete(request):
	result = {'success' : False}
	if request.method == "POST":
		if request.is_ajax():
			try:
				machine_id = request.POST['machine_id']
				machine = Machine.objects.get(id = machine_id)
				machine.delete()
				result['success'] = True;

				if result['success'] == True :
					#return HttpResponse(json.dumps(result),content_type='application/json') 
					return render(request, 'manager/formSuccess.html')
				else:
					return render(request, 'manager/formError.html')
			except:
					result['code'] = 1 #Machine does not exist
					return HttpResponse(json.dumps(result),content_type='application/json')
		else:
			result['code'] = 2 #Request is not Ajax
			return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		result['code'] = 3 #Request is not POST
		return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getAllShops(request):
	each_result = {}
	result = {"success": True}
	if request.method == "POST":
		if request.is_ajax():
			try:
				all_shop = Shop.objects.all()
				shops = []
				for each in all_shop:
					each_result["name"] = each.name
					each_result["shop_id"] = each.id
					shops.append(each_result)
					each_result = {}
				result['success'] = True
				result['shops'] = shops
			except DoesNotExist:
				result['code'] = 1
				return HttpResponse(json.dumps(result), content_type='application/json')
		else:
			result['code'] = 2
			return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result['code'] = 3
		return HttpResponse(json.dumps(result), content_type='application/json')

	return HttpResponse(json.dumps(result), content_type='application/json')

@login_required
def shopManagerDelete(request):
	result = {'success' : False}
	if request.method == "POST":
		if request.is_ajax():
			try:
				shop_id = request.POST['shop_id']
				shop = Shop.objects.get(id = shop_id)
				shop.delete()
				result['success'] = True;

				if result['success'] == True :
					#return HttpResponse(json.dumps(result),content_type='application/json') 
					return render(request, 'manager/formSuccess.html')
				else:
					return render(request, 'manager/formError.html')
			except:
					result['code'] = 1 #Machine does not exist
					return HttpResponse(json.dumps(result),content_type='application/json')
		else:
			result['code'] = 2 #Request is not Ajax
			return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		result['code'] = 3 #Request is not POST
		return HttpResponse(json.dumps(result),content_type='application/json')

@login_required
def getAllRepairShops(request):
	each_result = {}
	result = {"success": True}
	if request.method == "POST":
		if request.is_ajax():
			try:
				all_repair_shop = RepairShop.objects.all()
				repair_shops = []
				for each in all_repair_shop:
					each_result["name"] = each.name
					each_result["repair_shop_id"] = each.id
					repair_shops.append(each_result)
					each_result = {}
				result['success'] = True
				result['repair_shops'] = repair_shops
			except DoesNotExist:
				result['code'] = 1
				return HttpResponse(json.dumps(result), content_type='application/json')
		else:
			result['code'] = 2
			return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result['code'] = 3
		return HttpResponse(json.dumps(result), content_type='application/json')

	return HttpResponse(json.dumps(result), content_type='application/json')

@login_required
def repairShopManagerDelete(request):
	result = {'success' : False}
	if request.method == "POST":
		if request.is_ajax():
			try:
				repair_shop_id = request.POST['repair_shop_id']
				repair_shop = RepairShop.objects.get(id = repair_shop_id)
				repair_shop.delete()
				result['success'] = True;

				if result['success'] == True :
					#return HttpResponse(json.dumps(result),content_type='application/json') 
					return render(request, 'manager/formSuccess.html')
				else:
					return render(request, 'manager/formError.html')
			except:
					result['code'] = 1 #Machine does not exist
					return HttpResponse(json.dumps(result),content_type='application/json')
		else:
			result['code'] = 2 #Request is not Ajax
			return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		result['code'] = 3 #Request is not POST
		return HttpResponse(json.dumps(result),content_type='application/json')

#Get employees by manager
def getAllManagerEmployees(request):
	each_result = {}
	result = {'success' : False}
	if request.method == "POST":
		if request.is_ajax():
			try:
				manager = Employee.objects.get(user = request.user)
				all_manager_employee = Employee.objects.filter(manager = manager.id)
				employees = []
				for each in all_manager_employee:
					each_result['first_name'] = each.user.first_name
					each_result['last_name'] = each.user.last_name
					each_result['user_id'] = each.user.id					
					employees.append(each_result)
					each_result = {}
				result['success'] = True
				result['employees'] = employees
				print employees
			except DoesNotExist:
				result['code'] = 1
				return HttpResponse(json.dumps(result), content_type='application/json')
		else:
			result['code'] = 2
			return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result['code'] = 3
		return HttpResponse(json.dumps(result), content_type='application/json')

	return HttpResponse(json.dumps(result), content_type='application/json')



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

# Form to add a repair shop
def repairShopFormView(request):
	result = {'success': False}
	if request.method == "POST":
		repair_shop_form = repairShopForm(request.POST)
		if repair_shop_form.is_valid():
			new_repair_shop_name = repair_shop_form.cleaned_data['name']
			new_repair_shop_number = repair_shop_form.cleaned_data['number']
			new_repair_shop_address = repair_shop_form.cleaned_data['address']

			repair_shop = RepairShop(name = new_repair_shop_name, number = new_repair_shop_number, address = new_repair_shop_address)
			repair_shop.save()
			result['success'] = True

			if result['success'] == True :
				#return HttpResponse(json.dumps(result),content_type='application/json') 
				return render(request, 'manager/formSuccess.html')
			else:
				return render(request, 'manager/formError.html')
		else:
			result['code'] = 3 #this repair shop is already registered
			return render(request, 'manager/formError.html')
		return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		repair_shop_form = repairShopForm(request.POST)
	return render(request,'manager/formRepairShop.html', {'formRepairShop': repair_shop_form})
# End

#Updating Repair Shop
def repairShopUpdateView(request):
	result = {'success': False}
	if request.method == "POST":
		repairshopform = repairShopUpdateForm(request.POST)
		repair_shop_id = request.POST['repair_shop_id']
		if repairshopform.is_valid():
			try:
				repairshop = RepairShop.objects.get(id = repair_shop_id)
				new_repair_shop_name = repairshopform.cleaned_data['name']
				new_repair_shop_number = repairshopform.cleaned_data['number']
				new_repair_shop_address = repairshopform.cleaned_data['address']

				repair_shop = RepairShop(id = repair_shop_id, name = new_repair_shop_name, number = new_repair_shop_number, address = new_repair_shop_address)
				repair_shop.save()
				result['success'] = True

				return render(request, 'manager/formSuccess.html')

			except:
				result['code'] = 2 #RepairShop does not exist
				return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		try:
			repair_shop_id = request.GET.get("repair_shop_id")
			repairShopReturn = RepairShop.objects.get(id = repair_shop_id)
			if repairShopReturn != None:
				repairshop = repairShopUpdateForm(initial = {'repair_shop_id' : repair_shop_id, 'name' : repairShopReturn.name, 'number' : repairShopReturn.number, 'address' : repairShopReturn.address})
			else:
				repairshop = repairShopForm()
			return render(request,'manager/formRepairShop.html', {'formRepairShop' : repairshop})
		except:
			result['code'] = 2 #RepairShop does not exist
			return HttpResponse(json.dumps(result),content_type='application/json')

# Form to add a shop
def shopFormView(request):
	result = {'success': False}
	if request.method == "POST":
		shop_form = shopForm(request.POST)
		if shop_form.is_valid():
			new_shop_name = shop_form.cleaned_data['name']
			new_shop_number = shop_form.cleaned_data['number']
			new_shop_address = shop_form.cleaned_data['address']

			shop = Shop(name = new_shop_name, number = new_shop_number, address = new_shop_address)
			shop.save()
			result['success'] = True

			if result['success'] == True :
				#return HttpResponse(json.dumps(result),content_type='application/json') 
				return render(request, 'manager/formSuccess.html')
			else:
				return render(request, 'manager/formError.html')
		else:
			result['code'] = 3 #this shop is already registered
			return render(request, 'manager/formError.html')
		return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		shop_form = shopForm(request.POST)
	return render(request,'manager/formShop.html', {'formShop': shop_form})
# End

#Updating Shop
def shopUpdateView(request):
	result = {'success': False}
	if request.method == "POST":
		shopform = shopUpdateForm(request.POST)
		shop_id = request.POST['shop_id']
		if shopform.is_valid():
			try:
				shop = Shop.objects.get(id = shop_id)
				new_shop_name = shopform.cleaned_data['name']
				new_shop_number = shopform.cleaned_data['number']
				new_shop_address = shopform.cleaned_data['address']
				shop = Shop(id = 1, name = new_shop_name, number = new_shop_number, address = new_shop_address)
				shop.save()

				return render(request, 'manager/formSuccess.html')

			except:
				result['code'] = 2 #Shop does not exist
				return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		try:
			shop_id = request.GET.get("shop_id")
			shopReturn = Shop.objects.get(id = shop_id)
			if shopReturn != None:
				shop = shopUpdateForm(initial = {'shop_id' : shop_id, 'name' : shopReturn.name, 'number' : shopReturn.number, 'address' : shopReturn.address})
			else:
				shop = shopForm()
			return render(request,'manager/formShop.html', {'formShop' : shop})
		except:
			result['code'] = 2 #Shop does not exist
			return HttpResponse(json.dumps(result),content_type='application/json')


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

@login_required
def implementUpdateView(request):
	result = {'success' : False}
	if request.method == "POST":
		impleForm = implementUpdateForm(request.POST)
		imple_id = request.POST['implement_id']
		if impleForm.is_valid():
			try:
				imple = Implement.objects.get(id = imple_id)
				imple.manufacturer_model = impleForm.cleaned_data['manufacturer_model']
				imple.repair_shop = impleForm.cleaned_data['repair_shop']
				imple.shop = impleForm.cleaned_data['shop']
				imple.nickname = impleForm.cleaned_data['nickname']
				imple.qr_code = impleForm.cleaned_data['qr_code']
				imple.asset_number = impleForm.cleaned_data['asset_number']
				imple.serial_number = impleForm.cleaned_data['serial_number']
				imple.horse_power_req = impleForm.cleaned_data['horse_power_req']
				imple.hitch_capacity_req = impleForm.cleaned_data['hitch_capacity_req']
				imple.hitch_category = impleForm.cleaned_data['hitch_category']
				imple.drawbar_category = impleForm.cleaned_data['drawbar_category']
				imple.speed_range_min = impleForm.cleaned_data['speed_range_min']
				imple.speed_range_max = impleForm.cleaned_data['speed_range_max']
				imple.year_purchased = impleForm.cleaned_data['year_purchased']
				imple.implement_hours = impleForm.cleaned_data['implement_hours']
				imple.service_interval = impleForm.cleaned_data['service_interval']
				imple.base_cost = impleForm.cleaned_data['base_cost']
				imple.status = impleForm.cleaned_data['status']
				imple.hour_cost = impleForm.cleaned_data['hour_cost']
				imple.photo = impleForm.cleaned_data['photo']
				imple.photo1 = impleForm.cleaned_data['photo1']
				imple.photo2 = impleForm.cleaned_data['photo2']
				#imple.note = impleForm.cleaned_data['note']
				imple.beacon = impleForm.cleaned_data['beacon']
				print "test2"
				imple.save()
				return render(request, 'manager/formSuccess.html')
			except:
				result['code'] = 2 #Implement does not exist
				return HttpResponse(json.dumps(result),content_type='application/json')
		return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		try:
			implement_id = request.GET.get("implement_id")
			implementReturn = Implement.objects.get(id = implement_id)
			if implementReturn != None:
				imple = implementUpdateForm(initial = {'implement_id' : implement_id,'beacon' : implementReturn.beacon,'shop' : implementReturn.shop,'repair_shop' : implementReturn.repair_shop ,'manufacturer_model' :  implementReturn.manufacturer_model,'nickname' : implementReturn.nickname , 'asset_number' : implementReturn.asset_number , 'serial_number' : implementReturn.serial_number , 'qr_code' : implementReturn.qr_code , 'horse_power_req' : implementReturn.horse_power_req , 'hitch_capacity_req' : implementReturn.hitch_capacity_req , 'hitch_category' : implementReturn.hitch_category , 'drawbar_category' : implementReturn.drawbar_category , 'speed_range_min' : implementReturn.speed_range_min , 'speed_range_max' : implementReturn.speed_range_max , 'year_purchased' : implementReturn.year_purchased , 'implement_hours' : implementReturn.implement_hours , 'service_interval' : implementReturn.service_interval , 'base_cost' : implementReturn.base_cost, 'status' : implementReturn.status , 'hour_cost' : implementReturn.hour_cost , 'photo' : implementReturn.photo , 'photo1' : implementReturn.photo1, 'photo2' : implementReturn.photo2 })
			else:
				imple = implementForm()
			return render(request,'manager/formImplement.html', {'form' : imple})
		except:
			result['code'] = 2 #Implement does not exist
			return HttpResponse(json.dumps(result),content_type='application/json')

#Form to add implement
@login_required
def implementFormView(request):
	result = {'success' : False}
	if request.method == "POST":
		implementform = implementForm(request.POST)
		if implementform.is_valid():
			new_implement_manufacturer_model = implementform.cleaned_data['manufacturer_model']
			new_implement_repair_shop = implementform.cleaned_data['repair_shop']
			new_implement_shop = implementform.cleaned_data['shop']
			#new_machine_equipment_type = machineform.cleaned_data['equipment_type']
			new_implement_nickname = implementform.cleaned_data['nickname']
			new_implement_qr_code = implementform.cleaned_data['qr_code']
			new_implement_asset_number = implementform.cleaned_data['asset_number']
			new_implement_serial_number = implementform.cleaned_data['serial_number']
			new_implement_horsepower_req = implementform.cleaned_data['horse_power_req']
			new_implement_hitch_capacity_req = implementform.cleaned_data['hitch_capacity_req']
			new_implement_hitch_category = implementform.cleaned_data['hitch_category']
			new_implement_drawbar_category = implementform.cleaned_data['drawbar_category']
			new_implement_speed_range_min = implementform.cleaned_data['speed_range_min']
			new_implement_speed_range_max = implementform.cleaned_data['speed_range_max']
			new_implement_year_purchased = implementform.cleaned_data['year_purchased']
			new_implement_implement_hours = implementform.cleaned_data['implement_hours']
			new_implement_service_interval = implementform.cleaned_data['service_interval']
			new_implement_base_cost = implementform.cleaned_data['base_cost']
			new_implement_status = implementform.cleaned_data['status']
			new_implement_beacon = implementform.cleaned_data['beacon']
			new_implement_hour_cost = implementform.cleaned_data['hour_cost']
			new_implement_photo = implementform.cleaned_data['photo']
			new_implement_photo1 = implementform.cleaned_data['photo1']
			new_implement_photo2 = implementform.cleaned_data['photo2']
			
			implement = Implement(manufacturer_model = new_implement_manufacturer_model, repair_shop = new_implement_repair_shop, shop = new_implement_shop, nickname = new_implement_nickname, qr_code = new_implement_qr_code, asset_number = new_implement_asset_number, serial_number = new_implement_serial_number, horse_power_req = new_implement_horsepower_req, hitch_capacity_req = new_implement_hitch_capacity_req, hitch_category = new_implement_hitch_category, drawbar_category = new_implement_drawbar_category, speed_range_min = new_implement_speed_range_min, speed_range_max = new_implement_speed_range_max, year_purchased = new_implement_year_purchased, implement_hours = new_implement_implement_hours, service_interval = new_implement_service_interval, base_cost = new_implement_base_cost, status = new_implement_status, hour_cost = new_implement_hour_cost, photo = new_implement_photo, photo1 = new_implement_photo1, photo2 = new_implement_photo2, beacon = new_implement_beacon)
			implement.save()
			result['success'] = True
		
			if result['success'] == True :
				#return HttpResponse(json.dumps(result),content_type='application/json') 
				return render(request, 'manager/formSuccess.html')
			else:
				return render(request, 'manager/formError.html')
		else:
			result['code'] = 3 #this implement is already registered
			return render(request, 'manager/formError.html')
		return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		implementform = implementForm(request.POST)
	return render(request,'manager/formImplement.html', {'form': implementform})
##End

#Form to add machine
@login_required
def machineFormView(request):
	result = {'success' : False}
	if request.method == "POST":
		machineform = machineForm(request.POST)
		if machineform.is_valid():
			new_machine_manufacturer_model = machineform.cleaned_data['manufacturer_model']
			new_machine_repair_shop = machineform.cleaned_data['repair_shop']
			new_machine_shop = machineform.cleaned_data['shop']
			#new_machine_equipment_type = machineform.cleaned_data['equipment_type']
			new_machine_nickname = machineform.cleaned_data['nickname']
			new_machine_qr_code = machineform.cleaned_data['qr_code']
			new_machine_asset_number = machineform.cleaned_data['asset_number']
			new_machine_serial_number = machineform.cleaned_data['serial_number']
			new_machine_horsepower = machineform.cleaned_data['horsepower']
			new_machine_hitch_capacity = machineform.cleaned_data['hitch_capacity']
			new_machine_hitch_category = machineform.cleaned_data['hitch_category']
			new_machine_drawbar_category = machineform.cleaned_data['drawbar_category']
			new_machine_speed_range_min = machineform.cleaned_data['speed_range_min']
			new_machine_speed_range_max = machineform.cleaned_data['speed_range_max']
			new_machine_year_purchased = machineform.cleaned_data['year_purchased']
			new_machine_engine_hours = machineform.cleaned_data['engine_hours']
			new_machine_service_interval = machineform.cleaned_data['service_interval']
			new_machine_base_cost = machineform.cleaned_data['base_cost']
			new_machine_m_type = machineform.cleaned_data['m_type']
			new_machine_front_tires = machineform.cleaned_data['front_tires']
			new_machine_rear_tires = machineform.cleaned_data['rear_tires']
			new_machine_steering = machineform.cleaned_data['steering']
			new_machine_operator_station = machineform.cleaned_data['operator_station']
			new_machine_status = machineform.cleaned_data['status']
			new_machine_hour_cost = machineform.cleaned_data['hour_cost']
			new_machine_beacon = machineform.cleaned_data['beacon']
			new_machine_photo = machineform.cleaned_data['photo']
			new_machine_photo1 = machineform.cleaned_data['photo1']
			new_machine_photo2 = machineform.cleaned_data['photo2']
			
			machine = Machine(manufacturer_model = new_machine_manufacturer_model, repair_shop = new_machine_repair_shop, shop = new_machine_shop, nickname = new_machine_nickname, qr_code = new_machine_qr_code, asset_number = new_machine_asset_number, serial_number = new_machine_serial_number, horsepower = new_machine_horsepower, hitch_capacity = new_machine_hitch_capacity, hitch_category = new_machine_hitch_category, drawbar_category = new_machine_drawbar_category, speed_range_min = new_machine_speed_range_min, speed_range_max = new_machine_speed_range_max, year_purchased = new_machine_year_purchased, engine_hours = new_machine_engine_hours, service_interval = new_machine_service_interval, base_cost = new_machine_base_cost, m_type = new_machine_m_type, front_tires = new_machine_front_tires, rear_tires = new_machine_rear_tires, steering = new_machine_steering, operator_station = new_machine_operator_station, status = new_machine_status, hour_cost = new_machine_hour_cost, photo = new_machine_photo, photo1 = new_machine_photo1, photo2 = new_machine_photo2, beacon = new_machine_beacon)
			machine.save()
			result['success'] = True
		
			if result['success'] == True :
				#return HttpResponse(json.dumps(result),content_type='application/json') 
				return render(request, 'manager/formSuccess.html')
			else:
				return render(request, 'manager/formError.html')
		else:
			result['code'] = 3 #this machine is already registered
			return render(request, 'manager/formError.html')
		return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		machineform = machineForm(request.POST)
	return render(request,'manager/formMachine.html', {'formMachine': machineform})
##End

#Form to quick add machine
@login_required
def machineQuickFormAdd(request):
	result = {'success' : False}
	if request.method == "POST":		
		machineform = machineForm(request.POST)
		if machineform.is_valid():
			new_machine_manufacturer_model = machineform.cleaned_data['manufacturer_model']
			#new_machine_equipment_type = machineform.cleaned_data['equipment_type']
			new_machine_nickname = machineform.cleaned_data['nickname']
			new_machine_qr_code = machineform.cleaned_data['qr_code']
			new_machine_asset_number = machineform.cleaned_data['asset_number']
			new_machine_serial_number = machineform.cleaned_data['serial_number']
			
			machine = Machine(manufacturer_model = new_machine_manufacturer_model, nickname = new_machine_nickname, qr_code = new_machine_qr_code, asset_number = new_machine_asset_number, serial_number = new_machine_serial_number)
			machine.save()
			result['success'] = True
		
			if result['success'] == True :			
				#return HttpResponse(json.dumps(result),content_type='application/json') 
				return render(request, 'manager/formSuccess.html')
			else:				
				return render(request, 'manager/formError.html')
		else:			
			result['code'] = 3 #this form is not valid
			return render(request, 'manager/formError.html')
		return HttpResponse(json.dumps(result),content_type='application/json')
	else:		
		machineform = machineForm(request.POST)
	return render(request,'manager/templateAddEquipment.html', {'formMachine': machineform})
##End

def employeeFormView(request):
	form = employeeForm(request.POST)
	if form.is_valid():
		return redirect('formOk')
	else:
		return render(request, 'formTest.html', {'form': form})

### View To update Machine ###
@login_required
def machineUpdateView(request):
	result = {'success' : False}
	if request.method == "POST":
		machiForm = machineUpdateForm(request.POST)
		machi_id = request.POST['machine_id']
		if machiForm.is_valid():
			try:
				machi = Machine.objects.get(id = machi_id)
				machi.manufacturer_model = machiForm.cleaned_data['manufacturer_model']
				machi.repair_shop = machiForm.cleaned_data['repair_shop']
				machi.shop = machiForm.cleaned_data['shop']
				machi.nickname = machiForm.cleaned_data['nickname']
				machi.qr_code = machiForm.cleaned_data['qr_code']
				machi.asset_number = machiForm.cleaned_data['asset_number']
				machi.serial_number = machiForm.cleaned_data['serial_number']
				machi.horsepower = machiForm.cleaned_data['horsepower']
				machi.hitch_capacity = machiForm.cleaned_data['hitch_capacity']
				machi.hitch_category = machiForm.cleaned_data['hitch_category']
				machi.drawbar_category = machiForm.cleaned_data['drawbar_category']
				machi.speed_range_min = machiForm.cleaned_data['speed_range_min']
				machi.speed_range_max = machiForm.cleaned_data['speed_range_max']
				machi.year_purchased = machiForm.cleaned_data['year_purchased']
				machi.engine_hours = machiForm.cleaned_data['engine_hours']
				machi.service_interval = machiForm.cleaned_data['service_interval']
				machi.base_cost = machiForm.cleaned_data['base_cost']
				machi.m_type = machiForm.cleaned_data['m_type']
				machi.front_tires = machiForm.cleaned_data['front_tires']
				machi.rear_tires = machiForm.cleaned_data['rear_tires']
				machi.steering = machiForm.cleaned_data['steering']
				machi.operator_station = machiForm.cleaned_data['operator_station']
				machi.status = machiForm.cleaned_data['status']
				machi.hour_cost = machiForm.cleaned_data['hour_cost']
				machi.photo = machiForm.cleaned_data['photo']
				machi.photo1 = machiForm.cleaned_data['photo1']
				machi.photo2 = machiForm.cleaned_data['photo2']
				machi.note = machiForm.cleaned_data['note']
				machi.beacon = machiForm.cleaned_data['beacon']
				machi.save()
				return render(request, 'manager/formSuccess.html')
			except:
				result['code'] = 2 #Machine does not exist
				return HttpResponse(json.dumps(result),content_type='application/json')
		return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		try:
			machine_id = request.GET.get("machine_id")
			machineReturn = Machine.objects.get(id = machine_id)
			if machineReturn != None:
				machi = machineUpdateForm(initial = {'machine_id' : machine_id,'beacon' : machineReturn.beacon,'shop' : machineReturn.shop,'repair_shop' : machineReturn.repair_shop ,'manufacturer_model' :  machineReturn.manufacturer_model,'nickname' : machineReturn.nickname , 'asset_number' : machineReturn.asset_number , 'serial_number' : machineReturn.serial_number , 'qr_code' : machineReturn.qr_code , 'horsepower' : machineReturn.horsepower , 'hitch_capacity' : machineReturn.hitch_capacity , 'hitch_category' : machineReturn.hitch_category , 'drawbar_category' : machineReturn.drawbar_category , 'speed_range_min' : machineReturn.speed_range_min , 'speed_range_max' : machineReturn.speed_range_max , 'year_purchased' : machineReturn.year_purchased , 'engine_hours' : machineReturn.engine_hours , 'service_interval' : machineReturn.service_interval , 'base_cost' : machineReturn.base_cost , 'm_type' : machineReturn.m_type , 'front_tires' : machineReturn.front_tires , 'rear_tires' : machineReturn.rear_tires , 'steering' : machineReturn.steering , 'operator_station' : machineReturn.operator_station , 'status' : machineReturn.status , 'hour_cost' : machineReturn.hour_cost , 'photo' : machineReturn.photo , 'photo1' : machineReturn.photo1 ,'note' : machineReturn.note , 'photo2' : machineReturn.photo2 })
			else:
				machi = machineForm()
			return render(request,'manager/formMachine.html', {'formMachine' : machi})
		except:
			result['code'] = 2 #Machine does not exist
			return HttpResponse(json.dumps(result),content_type='application/json')



### End ###
@login_required
def employeeManagerUpdateForm(request):
	result = {'success' : False}
	if request.method == "POST":
		userform = UserFormUpdate(request.POST)
		employform = employeeUpdateForm(request.POST)
		user_id = request.POST['user']
		if userform.is_valid() and employform.is_valid():
			try:
				emplo = Employee.objects.get(user_id = user_id)
				emplo.user.first_name = userform.cleaned_data['first_name']
				emplo.user.last_name = userform.cleaned_data['last_name']
				emplo.company_id = employform.cleaned_data['company_id']
				emplo.start_date = employform.cleaned_data['start_date']
				emplo.active = employform.cleaned_data['active']
				emplo.language = employform.cleaned_data['language']
				emplo.qr_code = employform.cleaned_data['qr_code']
				emplo.hour_cost = employform.cleaned_data['hour_cost']
				emplo.contact_number = employform.cleaned_data['contact_number']
				emplo.permission_level = employform.cleaned_data['permission_level']
				emplo.photo = employform.cleaned_data['photo']
				emplo.notes = employform.cleaned_data['notes']
				emplo.manager = employform.cleaned_data['manager']

				if emplo.active == False:
					 emplo.user.is_active = False
				else:
					emplo.user.is_active = True
					
				emplo.user.save()
				emplo.save()
				return render(request, 'manager/formSuccess.html')
			except:
				result['code'] = 2 #Employee does not exist
				return HttpResponse(json.dumps(result),content_type='application/json')
		else:
			result['code'] = 3 #Form not valid
	else:
		try:
			user_id = request.GET.get('user_id')
			emplo = Employee.objects.get(user__id = user_id)
			userform = UserFormUpdate(initial = {'first_name' : emplo.user.first_name, 'last_name' : emplo.user.last_name})
			employform = employeeUpdateForm(initial = {'user' : user_id,'notes' : emplo.notes, 'photo' : emplo.photo, 'permission_level' : emplo.permission_level ,'contact_number' : emplo.contact_number ,'hour_cost' : emplo.hour_cost, 'qr_code' : emplo.qr_code ,'language' : emplo.language , 'active' : emplo.active, 'last_task' : emplo.last_task ,'start_date' : emplo.start_date,'company_id' : emplo.company_id, 'manager' : emplo.manager, 'active' : emplo.active})
			return render(request,'manager/employeeUpdate.html', {'form': userform, 'form1': employform})
		except:
			result['code'] = 2 #Employee does not exist
			return HttpResponse(json.dumps(result),content_type='application/json')
	return HttpResponse(json.dumps(result),content_type='application/json')
### End ###

### Form to add employee ###
def employeeFormadd(request):
	result = {'success' : False}
	if request.method == "POST":
		userform = UserForm(request.POST)
		employform = employeeForm(request.POST)
		if userform.is_valid() and employform.is_valid():
			new_user_username = userform.cleaned_data['username']
			new_user_password = userform.cleaned_data['password']
			new_user_first_name = userform.cleaned_data['first_name']
			new_user_last_name = userform.cleaned_data['last_name']
			new_user, created = User.objects.get_or_create(username = new_user_username, defaults = {'first_name' : new_user_first_name, 'last_name' : new_user_last_name})
			if created:
				new_user.set_password(new_user_password)
				new_user.save()
				emplo_company = employform.cleaned_data['company_id']
				emplo_language = employform.cleaned_data['language']
				emplo_qr_code = employform.cleaned_data['qr_code']
				emplo_start = employform.cleaned_data['start_date']
				emplo_cost = employform.cleaned_data['hour_cost']
				emplo_contact = employform.cleaned_data['contact_number']
				emplo_permission = employform.cleaned_data['permission_level']
				emplo_photo = employform.cleaned_data['photo']
				emplo_notes = employform.cleaned_data['notes']
				emplo_manager = employform.cleaned_data['manager']
				try:
					employee = Employee(user = new_user, language = emplo_language, permission_level = emplo_permission, active = '1', company_id = emplo_company, qr_code = emplo_qr_code, start_date = emplo_start, hour_cost = emplo_cost,contact_number = emplo_contact, notes = emplo_notes, photo = emplo_photo, manager = emplo_manager)
					employee.save()
					result['success'] = True
				except:
					User.objects.get(username = new_user_username).delete()
				if result['success'] == True :
					#return HttpResponse(json.dumps(result),content_type='application/json') 
					return render(request, 'manager/formSuccess.html')
				else:
					return render(request, 'manager/formError.html')
			else:
				result['code'] = 3 #this user is already registered as a employee
				return render(request, 'manager/formError.html')
			return HttpResponse(json.dumps(result),content_type='application/json')
	else:
		userform = UserForm(request.POST)
		employform = employeeForm(request.POST)
	employform = employeeForm(initial = {'start_date' : datetime.datetime.now()})
	return render(request,'manager/formEmployee.html', {'form': userform, 'form1': employform})
### End ###

### Password update view ###
@login_required
def employeeUpdatePasswordForm(request):
	result = {'success' : False}
	if request.method == "POST":
		userform = employeePasswordForm(request.POST)
		if userform.is_valid():
			password = userform.cleaned_data['password']
			password1 = userform.cleaned_data['password1']
			password2 = userform.cleaned_data['password2']
			if password1 == password2:
				user_password = User.objects.get(id = request.user.id)
				user_password.set_password(password1)
				user_password.save()
			else:
				result['code'] = 3 # New password does not match
		else:
			result['code'] = 4 # form not valid
	else:
		userform = employeePasswordForm()
		return render(request,'formTEST.html', {'form': userform})

### End  ###

### Form to update employee ###
@login_required
def employeeUpdateFormView(request):
	result = {'success' : False}
	if request.method == "POST":
		userform = UserFormUpdate(request.POST)
		employform = employeeForm(request.POST)
		emplo = Employee.objects.get(user_id = request.user.id)
		if userform.is_valid() and employform.is_valid():
			emplo.user.first_name = userform.cleaned_data['first_name']
			emplo.user.last_name = userform.cleaned_data['last_name']
			emplo.manager = employform.cleaned_data['manager']
			emplo.language = employform.cleaned_data['language']
			emplo.contact_number = employform.cleaned_data['contact_number']
			emplo.photo = employform.cleaned_data['photo']
			emplo.notes = employform.cleaned_data['notes']
			emplo.active = employform.cleaned_data['active']
			emplo.user.save()
			emplo.save()
			result['success'] = True
			return render(request, 'manager/formSuccess.html')
	else:
		try:
			emplo = Employee.objects.get(user_id = request.user.id)
			userform = UserFormUpdate(initial = {'first_name' : emplo.user.first_name, 'last_name' : emplo.user.last_name})
			# employform = employeeForm(initial = {'notes' : emplo.notes, 'photo' : emplo.photo, 'permission_level' : emplo.permission_level ,'contact_number' : emplo.contact_number ,'hour_cost' : emplo.hour_cost, 'qr_code' : emplo.qr_code ,'language' : emplo.language , 'active' : emplo.active, 'last_task' : emplo.last_task ,'start_date' : emplo.start_date,'company_id' : emplo.company_id})
			employform = employeeForm(initial = {'notes' : emplo.notes, 'photo' : emplo.photo, 'contact_number' : emplo.contact_number,'language' : emplo.language, 'manager' : emplo.manager, 'active' : emplo.active})
			result['success'] = True
		except:
			result['code'] = 3 # this user does not exist
			return HttpResponse(json.dumps(result),content_type='application/json')
		return render(request,'driver/employeeUpdate', {'form': userform, 'form1': employform})
### end ###

def testbase64(request):
	result = {'success' : False}
	test = MachineChecklist.objects.get(id = 48)
	test.set_data("aaa")
	test.save()
	result["depois"] = test.photo
	result["normal"] = test.get_data()
	return HttpResponse(json.dumps(result),content_type='application/json')

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
