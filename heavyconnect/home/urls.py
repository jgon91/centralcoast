from django.conf.urls import include, url, patterns
from home.views import *

urlpatterns = patterns('',
    url(r'^hello/$', hello),
)