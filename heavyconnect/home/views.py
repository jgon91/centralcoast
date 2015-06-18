from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.dateformat import DateFormat

import json

from home.forms import *


def home(request):
	if request.user.is_authenticated():
		print "user is authenticate"
	 	return redirect('driver')
	else:
		return render(request, 'index.html')

def updatedDate(request):
	dt = datetime.now()
	df = DateFormat(dt)
	result = df.format('D, F j Y - g:i A')
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

def logout(request):
	auth_logout(request)
	return redirect('home')

@login_required
def driver(request):
    return render(request, 'driver/indexDriver.html')

@login_required
def profile(request):
    return render(request, 'driver/profile.html')

@login_required
def header(request):
    return render(request, 'template/header.html')

@login_required
def headerHome(request):
    return render(request, 'template/headerHome.html')

@login_required
def footer(request):
	return render(request, 'template/footer.html')

@login_required
def task_flow(request):
	return render(request, 'driver/taskFlow.html')

@login_required
def timeKepper(request):
	return render(request, 'driver/timeKepper.html')

@login_required
def equipament(request):
    return render(request, 'driver/equipment.html')

@login_required
def schedule(request):
    return render(request, 'driver/schedule.html')

@login_required
def time_keeper(request):
    return render(request, 'driver/timeKepper.html')

@login_required
def updateStatus(request):
    return render(request, 'driver/updateStatus.html')

@login_required
def taskFlow(request):
    return render(request, 'driver/taskFlow.html')

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
def lastTasks(request):
    return render(request, 'driver/lastTasks.html')

@login_required
def startTask(request):
    return render(request, 'driver/startTask.html')

@login_required
def indexManager(request):
    return render(request, 'manager/indexManager.html')

@login_required
def fleet(request):
    return render(request, 'manager/fleet.html')

@login_required
def scanQRCode(request):
    return render(request, 'driver/scanQRCode.html')


