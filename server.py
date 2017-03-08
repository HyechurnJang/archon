#!/usr/bin/env python

'''
Created on 2017. 3. 8.

@author: Hye-Churn Jang
'''

#===============================================================================
# Import Platform Base
#===============================================================================
import re
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "archon.settings")
django.setup()

#===============================================================================
# Init Modules & Managers
#===============================================================================
import archon.urls
import archon.wsgi

#===============================================================================
# Inject Static File Resolver
#===============================================================================
from django.conf.urls import url
from django.views.static import serve
archon.urls.urlpatterns = [ url(r'^%s(?P<path>.*)$' % re.escape('/resources/'.lstrip('/')), serve, kwargs={'document_root' : 'archon/resources'}) ] + archon.urls.urlpatterns

#===============================================================================
# Run Gevent WSGI Server
#===============================================================================
from gevent.pywsgi import WSGIServer
server = WSGIServer(('0.0.0.0', 80), archon.wsgi.application, environ=os.environ)
server.serve_forever()
