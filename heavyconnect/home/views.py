from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

import json
import datetime

from home.forms import *
from home.models import *


def home(request):
	if request.user.is_authenticated():
	 	return redirect('driver')
	else:
		return render(request, 'home.html')

@login_required
def driver(request):
	return render(request, 'driver.html')

@login_required
def taskflow(request):
	return render(request, 'taskflow.html')

@login_required
def startNewTask(request):
	result = {'success' : False}

	if request.method == 'POST':
		if request.is_ajax():
			try:
				employee = Employee.objects.get(user_id = request.user.id)
				# if employee.permission_level = 2:
				# 	render start task page
				# else:
				# 	user does not have permission
			except Employee.DoesNotExist:
				result['code'] =  1 #There is no users associated with this
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
						return redirect('driver')
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


#Get equipment status, which can be a machine or a implement
# Remember the Fron-End guys that Status is mapped as:
# 1 = OK, 2 = Attention, 3 = Broken, 4 = Quarantine
@login_required
def getEquipmentStatus(request):
	result = {'success' : False}
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				machine = Machine.objects.get(qr_code = request.POST('qr_code'))
				result['status'] = machine.status
				result['success'] = True
			except Machine.DoesNotExist:
				try:
					implement = Implement.objects.get(qr_code = request.POST('qr_code'))
					result['status'] = implement.status
					result['success'] = True
				except Implement.DoesNotExist:
			 		result['code'] = 1 #There is no equipment for this qr_code
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
		 		machine = Machine.objects.get(qr_code = request.POST('qr_code')	)
	 			models = ManufacturerModel.objects.get(manufacturer_id = machine.manufacturer_model_id.id)
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



# It will return (some) information of all implements on database.
# Maybe later it will be need to filter some information based on size, capacity, etc
def getImplementInfo(request):
	each_result = {'success' : False}
	result = []
	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				implements = Implement.objects.filter()
				for each in implements:
					each_result['qr_code'] = each.qr_code
					each_result['year_purchased'] = each.year_purchased
					each_result['photo'] = each.photo
					each_result['manufacturer_model_id'] = each.manufacturer_model_id.manufacturer_id.name
					each_result['asset_number'] = each.asset_number
			 		each_result['horse_power_req'] = each.horse_power_req
					each_result['hitch_capacity_req'] = each.hitch_capacity_req
					each_result['status'] = each.status
					each_result['speed_range_max'] = each.speed_range_max
					result.append(each_result)
				result.append({'success' : True})
			except Machine.DoesNotExist:
				result.append({'code' : 1}) #There is no machine associated with this
		else:
	 		result.append({'code' : 2}) #Use ajax to perform requests
	else:
	 	result.append({'code' : 3}) #result[0]['code'] = 3 #Request was not POST

	# On the ELSE, the answer will be in result[0]
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
def retrievePedingTask(request):
	result = []
	result.append({'success' : False})
	date1 = datetime.timedelta(days = 1) #it will work as increment to the current day
	date2 =  datetime.datetime.now() + date1
	if request.method == 'POST':
		qrCode = request.POST['qr_code']
	 	if request.is_ajax():
			try:
				flag = 0
				aux = {}
				n = request.POST['N']
				emploTask = EmployeeTask.objects.filter(employee_id_id = request.user.id, task_init__lte =  date2)
				for item in emploTask:
					if not item.task_id.accomplished:
						aux['category'] = item.task_id.description
						aux['field'] = item.task_id.field_id.name
						aux['date'] = str(item.task_id.date)
						result.append(aux)
						aux = {}
						flag = flag + 1
						if flag >= n:
						 	break
				result[0] = {'success' : True}
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

def logout(request):
	auth_logout(request)
	return redirect('home')

def retrieveScannedEmployee(request):
	result = {'success' : False}
  	if request.method == 'POST':
	 	if request.is_ajax():
			try:
				employee = Employee.objects.get(qr_code = request.POST('qr_code'))
				employee = Employee.objects.get(user_id = request.user.id)
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














# @menezescode: Page only to show the form was correctly sended.
def formok(request):
	return render(request, 'formok.html')

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
				to a different page (formok) if it's correct and reload the page
				if the form was sent incorrectly

def manufacturerFormView(request):
	form = manufacturerForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def manufacturerModelForm(request):
	form = manufacturerModelForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def repairShopForm(request):
	form = repairShopForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def shopForm(request):
	form = shopForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def machineForm(request):
	form = machineForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def implementForm(request):
	form = implementForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})
def employeeForm(request):
	form = employeeForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def employeeAttendanceForm(request):
	form = employeeAttendanceForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def qualificationForm(request):
	form = qualificationForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def certificationForm(request):
	form = certificationForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def employeeQualificationsForm(request):
	form = employeeQualificationsForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def machineQualificationForm(request):
	form = machineQualificationForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})
def implementQualificationForm(request):
	form = implementQualificationForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def fieldForm(request):
	form = fieldForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def gpsForm(request):
	form = gpsForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def employeeLocalizationForm(request):
	form = employeeLocalizationForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def taskForm(request):
	form = taskForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def taskCategoryForm(request):
	form = taskCategoryForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})
def employeeTaskForm(request):
	form = employeeTaskForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def taskImplementMachineForm(request):
	form = taskImplementMachineForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def appendixForm(request):
	form = appendixForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def appendixTaskForm(request):
	form = appendixTaskForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def serviceCategoryForm(request):
	form = serviceCategoryForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def serviceForm(request):
	form = serviceForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def machineServiceForm(request):
	form = machineServiceForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})

def implementServiceForm(request):
	form = implementServiceForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})
'''
