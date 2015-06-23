from django.conf.urls import include, url, patterns
from home.views import *

urlpatterns = patterns('',
	url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^driver/$', driver, name='driver'),
    #url(r'^formTEST/$', registerManufacturer, name='registerManufacturer'),
    url(r'^formok/$', formok, name = 'formok'),
    url(r'^getEmployeeLocation/$', getEmployeeLocation, name = 'getEmployeeLocation'),
)