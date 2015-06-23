from django.conf.urls import include, url, patterns
from home.views import *

urlpatterns = patterns('',
	url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^driver/$', driver, name='driver'),
    url(r'^equipment/$', equipament, name='equipment'),
    url(r'^schedule/$', schedule, name='schedule'),
    url(r'^header/$', header, name='header'),
    url(r'^headerHome/$', headerHome, name='headerHome'),
    url(r'^footer/$', footer, name='footer'),
    url(r'^taskFlow/$', task_flow, name='task_flow'),
    url(r'^serverDate/$', updatedDate, name='updated_date'),
    url(r'^time_keeper/$', time_keeper, name='time_keeper'),
    url(r'^updateStatus/$', updateStatus, name='updateStatus'),
    url(r'^taskFlow/$', taskFlow, name='taskFlow'),
    url(r'^checklist/$', checklist, name='checklist'),
    url(r'^fleet/$', fleet, name='fleet'),
    url(r'^headerManager/$', headerManager, name='headerManager'),
    url(r'^lastTasks/$', lastTasks, name='lastTasks'),
    url(r'^createTask/$', createTask, name='createTask'),
    url(r'^startTask/$', startTask, name='startTask'),
    url(r'^scanQRCode/$', scanQRCode, name='scanQRCode'),
    url(r'^indexManager/$', indexManager, name='indexManager'),
    url(r'^equipmentManager/$', equipmentManager, name='equipmentManager'),
    url(r'^getEmployeeLocation/$', getEmployeeLocation, name = 'getEmployeeLocation'),
    url(r'^formTEST/$', manufacturerForm, name='registerManufacturer'),
    url(r'^formok/$', formok, name = 'formok'),
    url(r'^test/$', getDriverInformation, name = 'driverInfo'),
)