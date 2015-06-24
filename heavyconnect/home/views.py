from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.utils.dateformat import DateFormat

import json
import datetime

from home.forms import *
from home.models import *


def home(request):
	if request.user.is_authenticated():
	 	return redirect('driver')
	else:
		return render(request, 'index.html')

def updatedDate(request):
	dt = datetime.now()
	df = DateFormat(dt)
	result = df.format('D, F j Y - g:i A')
	return HttpResponse(json.dumps(result),content_type='application/json')

#Issue #73
@login_required
def getEmployeeLocation(request):
	result = {'success' : False}

	employee = Employee.objects.get(user_id = request.user.id)

	localization = EmployeeLocalization.objects.filter(employee_id = employee.id).order_by('-e_time').values('latitude','longitude')[0]

	result['latitude'] = localization['latitude']
	result['longitude'] = localization['longitude']

	result['success'] = True

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
	
	return HttpResponse(json.dumps(result),content_type='application/js  on')

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
	 		result['code'] = 4 #Use ajax to perform requests
	else:
		result['code'] = 5 #Request was not POST

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
If you need to test the forms change the form name.
</menezescode>

@menezescode: 	Those are the forms. At the current point 06/22/2015,
				each view does nothgin besides render the page and redirect
				to a different page if it's correct and reload the page 
				if the form was sent incorrectly


def manufacturerForm(request):
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
