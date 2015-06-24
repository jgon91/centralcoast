from django.conf.urls import include, url, patterns
from home.views import *

urlpatterns = patterns('',
	url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^driver/$', driver, name='driver'),
    
    ### Functions ###
    url(r'^employeeLocation/$', getEmployeeLocation, name = 'employeeLocation'),
    url(r'^driverInfo/$', getDriverInformation, name = 'driverInfo'),
    url(r'^startNewTask/$', startNewTask, name = 'startNewTask'),
    url(r'^quickUserInfomation/$', getQuickUser, name = 'quickUser'),
    url(r'^updatePhoto/$', updatePhoto, name = 'updatePhoto'),
    ### End ###

    ### Froms ###
    url(r'^formTEST/$', manufacturerForm, name='registerManufacturer'),
    url(r'^formok/$', formok, name = 'formok'),
    ### End ###
)