from django.conf.urls import include, url, patterns
from home.views import *

urlpatterns = patterns('',
	url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^driver/$', driver, name='driver'),
    
    ### Functions ###
    url(r'^employeeLocation/$', getEmployeeLocation, name = 'employeeLocation'),
    url(r'^employeeSchedule/$', getEmployeeSchedule, name = 'employeeSchedule'),
    url(r'^driverInfo/$', getDriverInformation, name = 'driverInfo'),
    url(r'^startNewTask/$', startNewTask, name = 'startNewTask'),
    url(r'^quickUserInfomation/$', getQuickUser, name = 'quickUser'),
    url(r'^updatePhoto/$', updatePhoto, name = 'updatePhoto'),
    url(r'^loadEquipmentImage/$', loadEquipmentImage, name = 'loadEquipmentImage'),
    url(r'^loadMachinesImage/$', loadMachinesImage, name = 'loadMachinesImage'),
    url(r'^loadImplementsImage/$', loadImplementsImage, name = 'loadImplementsImage'),
    url(r'^startShift/$', startShift, name = 'startShift'),
    url(r'^startStopBreak/$', startStopBreak, name = 'startStopBreak'),
    ### End ###

    ### Froms ###
    url(r'^formTEST/$', manufacturerFormView, name='registerManufacturer'),
    url(r'^formok/$', formok, name = 'formok'),
    ### End ###
)