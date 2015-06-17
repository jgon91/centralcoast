from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

import json

from home.forms import *


def home(request):
	if request.user.is_authenticated():
	 	return redirect('driver')
	else:
		return render(request, 'home.html')

@login_required
def driver(request):
	return render(request, 'driver.html')

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
If you need to test the forms change the form name.
</menezescode>
'''

def registerManufacturer(request):
	form = implementServiceForm(request.POST)
	if form.is_valid():
		return redirect('formok')
	else:
		return render(request, 'formTEST.html', {'form': form})