from django.conf.urls import include, url, patterns
from home.views import *

urlpatterns = patterns('',
	url(r'^$', home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^driver/$', driver, name='driver'),
    url(r'^equipment/$', equipament, name='equipment'),
    url(r'^header/$', header, name='header'),
    url(r'^footer/$', footer, name='footer'),
    url(r'^taskFlow/$', task_flow, name='task_flow'),
    url(r'^menuLeft/$', menu_left, name='menu_left'),
    url(r'^serverDate/$', updatedDate, name='updated_date'),
    url(r'^time_keeper/$', time_keeper, name='time_keeper'),
)