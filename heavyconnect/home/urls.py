from django.conf.urls import include, url, patterns
from . import views as main_views
from . import viewsCRUD as CRUD

# The views are divided in 2 different documents
# The views about CRUD will be on viewsCRUD and
# the views about functions will be on views
# In order to speficy which doc has to be looked for. It should put one prefix before the function main_views for views or
# CRUD. for viewsCRUD

#Example: url(r'^ /$', main_views., name = ''),

urlpatterns = [
	url(r'^$', main_views.home, name='home'),
    url(r'^login/$', main_views.login, name='login'),
    url(r'^logout/$', main_views.logout, name='logout'),
    url(r'^driver/$', main_views.driver, name='driver'),
	url(r'^taskflow/$', main_views.taskflow, name='taskflow'),

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
	url(r'^getAllImplementInfo/$', main_views.getAllImplementInfo, name = 'getAllImplementInfo'),
	url(r'^getEquipmentInfo/$', main_views.getEquipmentInfo, name = 'getEquipmentInfo'),
    url(r'^retrieveScannedMachine/$', main_views.retrieveScannedMachine, name = 'retrieveScannedMachine'),
	url(r'^getScannedImplement/$', main_views.getScannedImplement, name = 'getScannedImplement'),
    url(r'^retrievePedingTask/$', main_views.retrievePedingTask, name = 'retrievePedingTask'),
    url(r'^retrieveMachine/$', main_views.retrieveMachine, name = 'retrieveMachine'),
	url(r'^retrieveScannedEmployee/$', main_views.retrieveScannedEmployee, name = 'retrieveScannedEmployee'),
    url(r'^continueTask/$', main_views.continueTask, name = 'continueTask'),
    url(r'^pastTaskList/$', main_views.pastTaskList, name = 'pastTaskList'),
    ### End ###

    ###Insert###
    url(r'^createManufacture/$', CRUD.createManufacture, name = 'createManufacture'),
    ###End###

    ### Froms ###
    url(r'^formOk/$', main_views.formOk, name = 'formOk'),
    url(r'^manufacturerFormView/$', main_views.manufacturerFormView, name='registerManufacturer'),
    url(r'^manufacturerModelFormView/$', main_views.manufacturerModelFormView, name = 'registerManufacturerModel'),
    url(r'^repairShopFormView/$', main_views.repairShopFormView, name = 'registerRepairShop'),
    url(r'^shopFormView/$', main_views.shopFormView, name = 'registerShop'),
    url(r'^machineFormView/$', main_views.machineFormView, name = 'registerMachine'),
    url(r'^implementFormView/$', main_views.implementFormView, name = 'registerImplement'),
    url(r'^employeeFormView/$', main_views.employeeFormView, name = 'registerEmployee'),
    url(r'^employeeAttendanceFormView/$', main_views.employeeAttendanceFormView, name = 'registerEmployeeAttendance'),
    url(r'^qualificationFormView/$', main_views.qualificationFormView, name = 'registerQualification'),
    url(r'^certificationFormView/$', main_views.certificationFormView, name = 'registerCertification'),
    url(r'^employeeQualificationsFormView/$', main_views.employeeQualificationsFormView, name = 'registerEmployeeQualification'),
    url(r'^machineQualificationFormView/$', main_views.machineQualificationFormView, name = 'registerMachineQualification'),
    url(r'^implementQualificationFormView/$', main_views.implementQualificationFormView, name = 'registerImplementQualification'),
    url(r'^fieldFormView/$', main_views.fieldFormView, name = 'registerField'),
    url(r'^gpsFormView/$', main_views.gpsFormView, name = 'registerGps'),
    url(r'^employeeLocalizationFormView/$', main_views.employeeLocalizationFormView, name = 'registerEmployeeLocalization'),
    url(r'^taskFormView/$', main_views.taskFormView, name = 'registerTask'),
    url(r'^taskCategoryFormView/$', main_views.taskCategoryFormView, name = 'registerTaskCategory'),
    url(r'^employeeTaskFormView/$', main_views.employeeTaskFormView, name = 'registerEmployeeTask'),
    url(r'^taskImplementMachineFormView/$', main_views.taskImplementMachineFormView, name = 'registerTaskImplementMachine'),
    url(r'^appendixFormView/$', main_views.appendixFormView, name = 'registerAppendix'),
    url(r'^appendixTaskFormView/$', main_views.appendixTaskFormView, name = 'registerAppendixTask'),
    url(r'^serviceCategoryFormView/$', main_views.serviceCategoryFormView, name = 'registerServiceCategory'),
    url(r'^serviceFormView/$', main_views.serviceFormView, name = 'registerService'),
    url(r'^machineServiceFormView/$', main_views.machineServiceFormView, name = 'registerMachineService'),
    url(r'^implementServiceFormView/$', main_views.implementServiceFormView, name = 'registerImplementService'),
    ### End ###
]
