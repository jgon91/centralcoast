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
			except DoesNotExist:
				result['code'] ==  1 #There is no users associated with this
		else:
			result['code'] == 4 #Use ajax to perform requests
	else:
		result['code'] == 5 #Request was not POST
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
			except DoesNotExist:
				result['code'] = 1 #There is no users associated with this 
		else:
	 		result['code'] = 4 #Use ajax to perform requests
	else:
		result['code'] = 5 #Request was not POST

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
				print employee.company_id
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

#This function gives back the picture of the refered QrCode
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

def getEmployee(request):
	result = {'success' : False}
	stop = False

	if request.method == 'POST':
		if request.is_ajax():
			qrc = request.GET['qr_code']

			employee = Employee.objects.get(qr_code = qrc)

			#creating the data range for the day, generating the 00:00:00 and the 23:59:59 of the current day
			now = datetime.datetime.now()
			start_date = datetime.datetime.combine(now, datetime.time.min)
			end_date = datetime.datetime.combine(now, datetime.time.max)
			try:
				attendance = EmployeeAttendance.objects.get(employee_id = employee.id, date__range = (start_date, end_date))
			except EmployeeAttendance.DoesNotExist:
				result['code'] = 1 #There is no shift records for this employee
				stop = True

			if not stop:
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
		else:
	 		result['code'] = 2 #Use ajax to perform requests
	else: 
	 	result['code'] = 3 #Request was not POST

	return HttpResponse(json.dumps(result),content_type='application/json')

def logout(request):
	auth_logout(request)
	return redirect('home')

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

'''
def manufacturerForm(request):
	form = manufacturerForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})
'''
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