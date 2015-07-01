from django.conf.urls import include, url, patterns
from . import views as main_views
from . import viewsCRUD as CRUD

# The views are divided in 2 different documents
# The views about CRUD will be on viewsCRUD and
# the views about functions will be on views
# In order to speficy which doc has to be looked for. It should put one prefix before the function main_views for views or
# CRUD. for viewsCRUD

urlpatterns = patterns('',
	url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^driver/$', driver, name='driver'),
    url(r'^equipment/$', equipament, name='equipment'),
    url(r'^schedule/$', schedule, name='schedule'),
    url(r'^headerDriver/$', headerDriver, name='headerDriver'),
    url(r'^headerHome/$', headerHome, name='headerHome'),
    url(r'^footer/$', footer, name='footer'),
    url(r'^taskFlow/$', taskFlow, name='taskFlow'),
    url(r'^serverDate/$', updatedDate, name='updated_date'),
    url(r'^time_keeper/$', time_keeper, name='time_keeper'),
    url(r'^updateStatus/$', updateStatus, name='updateStatus'),
    url(r'^checklist/$', checklist, name='checklist'),
    url(r'^fleet/$', fleet, name='fleet'),
    url(r'^headerManager/$', headerManager, name='headerManager'),
    url(r'^pastTasks/$', pastTasks, name='pastTasks'),
    url(r'^createTask/$', createTask, name='createTask'),
    url(r'^startTask/$', startTask, name='startTask'),
    url(r'^scanQRCode/$', scanQRCode, name='scanQRCode'),
    url(r'^indexManager/$', indexManager, name='indexManager'),
    url(r'^equipmentManager/$', equipmentManager, name='equipmentManager'),
    url(r'^profileManager/$', profileManager, name='profileManager'),
    url(r'^getEmployeeLocation/$', getEmployeeLocation, name = 'getEmployeeLocation'),
    url(r'^formTEST/$', manufacturerForm, name='registerManufacturer'),


    
    ### Functions ###
    url(r'^employeeLocation/$', main_views.getEmployeeLocation, name = 'employeeLocation'),
    url(r'^employeeSchedule/$', main_views.getEmployeeSchedule, name = 'employeeSchedule'),
    url(r'^driverInfo/$', main_views.getDriverInformation, name = 'driverInfo'),
    url(r'^startNewTask/$', main_views.startNewTask, name = 'startNewTask'),
    url(r'^quickUserInfomation/$', main_views.getQuickUser, name = 'quickUser'),
    url(r'^updatePhoto/$', main_views.updatePhoto, name = 'updatePhoto'),
    url(r'^loadEquipmentImage/$', main_views.loadEquipmentImage, name = 'loadEquipmentImage'),
    url(r'^loadMachinesImage/$', main_views.loadMachinesImage, name = 'loadMachinesImage'),
    url(r'^loadImplementsImage/$', main_views.loadImplementsImage, name = 'loadImplementsImage'),
    url(r'^startShift/$', main_views.startShift, name = 'startShift'),
    url(r'^equipmentStatus/$', main_views.getEquipmentStatus, name = 'equipmentStatus'),
    url(r'^startStopBreak/$', main_views.startStopBreak, name = 'startStopBreak'),
	url(r'^getImplementInfo/$', main_views.getImplementInfo, name = 'getImplementInfo'),
    url(r'^retrieveScannedMachine/$', main_views.retrieveScannedMachine, name = 'retrieveScannedMachine'),
    url(r'^retrievePedingTask/$', main_views.retrievePedingTask, name = 'retrievePedingTask'),
    url(r'^retrieveMachine/$', main_views.retrieveMachine, name = 'retrieveMachine'),
	url(r'^retrieveScannedEmployee', main_views.retrieveScannedEmployee, name = 'retrieveScannedEmployee')
    ### End ###

    ###Insert###
    url(r'^createManufacture/$', CRUD.createManufacture, name = 'createManufacture'),
    ###End###

    ### Froms ###
    url(r'^formTEST/$', main_views.manufacturerFormView, name='registerManufacturer'),
    url(r'^formok/$', main_views.formok, name = 'formok'),

    ### End ###
)
