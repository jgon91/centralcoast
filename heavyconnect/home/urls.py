from django.conf.urls import include, url, patterns
from home.views import *

urlpatterns = patterns('',
	url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^driver/$', driver, name='driver'),
    url(r'^header/$', header, name='header'),
    url(r'^taskFlow/$', header, name='task_flow'),
    url(r'^timeKeeper/$', header, name='time_keeper'),
    url(r'^serverDate/$', updatedDate, name='updated_date'),
)