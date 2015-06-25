from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

import json
import datetime

from home.forms import *
from home.models import *


def test(request):
	result = {'success' : False}
	return HttpResponse(json.dumps(result),content_type='application/json')

#Insert Manufacture
def createManufacture(request):
	result = {'success' : False}
	if request.method == 'POST':
		if request.is_ajax():
			newName = request.POST['name']
			manu = Manufacturer(name = newName)
			manu.save()
			result['success'] = True
		else:
			result['code'] = 2 #Use ajax to perform requests
	else:
		result['code'] = 3 #Request was not POST
	return HttpResponse(json.dumps(result),content_type='application/json')