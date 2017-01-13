# -*- coding: utf-8 -*-
################################################################################
#        _____ _                  _____           _                            #
#       / ____(_)                / ____|         | |                           #
#      | |     _ ___  ___ ___   | (___  _   _ ___| |_ ___ _ __ ___  ___        #
#      | |    | / __|/ __/ _ \   \___ \| | | / __| __/ _ \ '_ ` _ \/ __|       #
#      | |____| \__ \ (_| (_) |  ____) | |_| \__ \ ||  __/ | | | | \__ \       #
#       \_____|_|___/\___\___/  |_____/ \__, |___/\__\___|_| |_| |_|___/       #
#                                        __/ |                                 #
#                                       |___/                                  #
#           _  __                       _____       _  _____ ______            #
#          | |/ /                      / ____|     | |/ ____|  ____|           #
#          | ' / ___  _ __ ___  __ _  | (___   ___ | | (___ | |__              #
#          |  < / _ \| '__/ _ \/ _` |  \___ \ / _ \| |\___ \|  __|             #
#          | . \ (_) | | |  __/ (_| |  ____) | (_) | |____) | |____            #
#          |_|\_\___/|_|  \___|\__,_| |_____/ \___/|_|_____/|______|           #
#                                                                              #
################################################################################
#                                                                              #
# Copyright (c) 2016 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
# Licensed under the Apache License, Version 2.0 (the "License"); you may      #
# not use this file except in compliance with the License. You may obtain      #
# a copy of the License at                                                     #
#                                                                              #
# http://www.apache.org/licenses/LICENSE-2.0                                   #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################

import re
import json

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from archon.settings import SESSION_COOKIE_AGE
from archon.common import *
from archon.view import *

ARCHON_DEBUG = False

class ManagerAbstraction:
    
    __MANAGER__ = None
    
    @classmethod
    def instance(cls, *argv, **kargs):
        if cls.__MANAGER__ == None: cls.__MANAGER__ = cls(*argv, **kargs)
        return cls.__MANAGER__

class ArchonView:
        
    def __init__(self, app, lang):
        self.Menu = DIV()
        self.Page = DIV()
        self._app = app
        self._lang = lang
        
    def __call__(self, key):
        glb_locale = archon_locales['GLOBAL']
        if self._app in archon_locales:
            app_locale = archon_locales[self._app]
            if key in app_locale:
                key_locale = app_locale[key]
                for lang in self._lang:
                    if lang in key_locale: return key_locale[lang]
        if key in glb_locale:
            key_locale = glb_locale[key]
            for lang in self._lang:
                if lang in key_locale: return key_locale[lang]
        return key
        
    def __render__(self):
        return {'menu' : self.Menu, 'page' : self.Page}
    
    @classmethod
    def __error__(cls, title, msg):
        return {'menu' : DIV(), 'page' : Alert(title, msg, **{'class' : 'alert-danger'})}

def pageview(manager_class):
    
    class Req:
    
        def __init__(self, request, method, path, query, data):
            self.Request = request
            self.Method = method
            self.Path = path
            self.Query = query
            self.Data = data
        
    def wrapper(view):
        
        @login_required
        def decofunc(request):
            request.session.set_expiry(SESSION_COOKIE_AGE)
            
            method = request.method
            path = filter(None, request.path.split('/'))
            lang = filter(None, re.split(';|,|q=0.\d', request.META['HTTP_ACCEPT_LANGUAGE']))
            app = view.__module__.split('.')[1]
            
            v = ArchonView(app, lang)
            
            try:
                if method == 'GET': query = request.GET; data = {}
                elif method == 'POST': query = request.POST; data = json.loads(request.body)
                elif method == 'PUT': query = request.PUT; data = json.loads(request.body)
                elif method == 'DELETE': query = {}; data = {}
                else: query = {}; data = {}
            except Exception as e: return JsonResponse(ArchonView.__error__(v('request error'), str(e)))
            
            try: m = manager_class.instance()
            except Exception as e: return JsonResponse(ArchonView.__error__(v('manager allocation error'), str(e)))

            r = Req(request, method, path, query, data)
            try: view(r, m, v)
            except Exception as e: return JsonResponse(ArchonView.__error__(v('application error'), str(e)))
            return JsonResponse(v.__render__())
        
        def decofunc_debug(request):
            method = request.method
            path = filter(None, request.path.split('/'))
            lang = filter(None, re.split(';|,|q=0.\d', request.META['HTTP_ACCEPT_LANGUAGE']))
            app = view.__module__.split('.')[1]
            
            print method
            print path
            
            v = ArchonView(app, lang)
            
            if method == 'GET': query = request.GET; data = {}
            elif method == 'POST': query = request.POST; data = json.loads(request.body)
            elif method == 'PUT': query = request.PUT; data = json.loads(request.body)
            elif method == 'DELETE': query = {}; data = {}
            else: query = {}; data = {}
            
            m = manager_class.instance()

            r = Req(request, method, path, query, data)
            view(r, m, v)
            return JsonResponse(v.__render__())
        
        if ARCHON_DEBUG: return decofunc_debug
        else: return decofunc
    
    return wrapper

def modelview(model):
    admin.site.register(model, admin.ModelAdmin)
