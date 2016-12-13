# -*- coding: utf-8 -*-

import json

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

def pageview(manager_class):
    
    manager = manager_class.instance()

    def wrapper(view):
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
            except Exception as e: return JsonResponse({'menu' : DIV(), 'page' : Alert(u'요청 에러', str(e), **{'class' : 'alert-danger'})})
            try:
                menu = Menu() 
                page = view(manager, request, method, path, query, data, menu)
            except Exception as e: return JsonResponse({'menu' : DIV(), 'page' : Alert(u'서버 에러', str(e), **{'class' : 'alert-danger'})})
            if isinstance(page, dict): return JsonResponse({'menu' : menu, 'page' : page})
            else: return JsonResponse({'menu' : menu, 'page' : DIV().html(page)})
        return decofunc
    return wrapper
