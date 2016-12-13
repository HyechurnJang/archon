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

import json

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from archon.settings import SESSION_COOKIE_AGE
from archon.view import *

class Manager:
    
    __MANAGER__ = None
    
    @classmethod
    def instance(cls, *argv, **kargs):
        if cls.__MANAGER__ == None: cls.__MANAGER__ = cls(*argv, **kargs)
        return cls.__MANAGER__
    
class View:
    
    @classmethod
    def Error(cls, title, msg):
        return {'menu' : DIV(), 'page' : Alert(title, msg, **{'class' : 'alert-danger'})}
    
    def __init__(self):
        self.Menu = DIV()
        self.Page = DIV()
        
def pageview(manager_class):
    
    def pageview_wrapper(view):
        @login_required
        def decofunc(request):
            request.session.set_expiry(SESSION_COOKIE_AGE)
            method = request.method
            path = filter(None, request.path.split('/'))
            try:
                if method == 'GET':
                    query = request.GET
                    data = {}
                elif method == 'POST':
                    query = request.POST
                    data = json.loads(request.body)
                elif method == 'PUT':
                    query = request.PUT
                    data = json.loads(request.body)
                elif method == 'DELETE':
                    query = {}
                    data = {}
                else:
                    query = {}
                    data = {}
            except Exception as e: return JsonResponse(View.Error(u'요청 에러', str(e)))
            try:
                v = View()
                manager = manager_class.instance() 
                view(request, method, path, query, data, manager, v)
                v = {'menu' : v.Menu, 'page' : v.Page}
            except Exception as e: return JsonResponse(View.Error(u'서버 에러', str(e)))
            return JsonResponse(v)
        return decofunc
    return pageview_wrapper

def modelview(model):
    admin.site.register(model, admin.ModelAdmin)