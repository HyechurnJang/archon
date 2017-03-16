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

"""archon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import re
import sys
import shutil
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.utils.decorators import method_decorator
from django.template import loader, Template, Context
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .settings import ARCHON_APPLICATIONS, ARCHON_LANGUAGE, BASE_DIR, STATIC_DIR
import dashboard
import views

class MainPage:
    
    def __init__(self):
        self.mainpage = loader.get_template('mainpage.html')
        self.logopage = loader.get_template('logopage.html').render({})
        
    def setAppDesc(self, desc):
        
        def parseUrlToHtml(desc):
            if 'urls' in desc:
                pages = []
                selector = '<li class="dropdown">\n'
                selector += '<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">%s<span class="caret"></span></a>\n' % desc['display']
                selector += '<ul class="dropdown-menu" role="menu">\n'
                for url in desc['urls']:
                    csel, cpage = parseUrlToHtml(url)
                    selector += csel
                    pages = pages + cpage
                selector += '</ul></li>\n'
                return selector, pages
            elif 'url' in desc:
                selector = '<li><a class="page-selector" page="#page-%s" view="%s">%s</a></li>\n' % (desc['name'], desc['url'], desc['display'])
                page = 'page-' + desc['name']
                return selector, [page]
            return None, None
        
        app_selectors = ''
        page_selectors = ''
        pages = ''
        page_names = []
        for app in desc:
            app_selectors += '<a class="app-selector" app="#%s">%s</a>\n' % (app['name'], app['display'])
            page_selectors += '<ul class="nav navbar-nav app" id="%s">\n' % app['name']
            for url in app['urls']:
                csel, cpage = parseUrlToHtml(url)
                page_selectors += csel
                page_names = page_names + cpage 
            page_selectors += '</ul>\n'
        for page_name in page_names: pages += '<div id="%s" class="container-fluid page dynpage collapse">%s</div>\n' % (page_name, page_name)
        
        admin_selectors = [
            '<li><a class="admin-selector" view="/archon/mapping">MAC & IP</a></li>',
            '<li class="divider"></li>'
            '<li><a href="/admin/">Database Tool</a></li>',
            '<li><a href="/archon/logo">Logo Uploader</a></li>',
            '<li class="divider"></li>'
        ]
        
        self.app_selectors = Template(app_selectors).render(Context())
        self.page_selectors = Template(page_selectors).render(Context())
        self.pages = Template(pages).render(Context())
        self.admin = Template(''.join(admin_selectors)).render(Context())
        self.user = Template('').render(Context())

    @method_decorator(login_required)
    def sendMainPage(self, request):
        if request.user.is_superuser:
            return HttpResponse(self.mainpage.render({'app_selectors' : self.app_selectors,
                                                      'page_selectors' : self.page_selectors,
                                                      'user_name' : request.user.username,
                                                      'user_menu' : self.admin,
                                                      'pages' : self.pages}))
        else:
            return HttpResponse(self.mainpage.render({'app_selectors' : self.app_selectors,
                                                      'page_selectors' : self.page_selectors,
                                                      'user_name' : request.user.username,
                                                      'user_menu' : self.user,
                                                      'pages' : self.pages}))
    
    @method_decorator(login_required)
    def sendLogoPage(self, request):
        logo_dir = BASE_DIR + '/' + STATIC_DIR + '/images/'
        if request.method == 'POST' and 'logo' in request.FILES:
            logo = request.FILES['logo']
            with open(logo_dir + 'logo.png', 'wb+') as fd: fd.write(logo.read())
        elif request.method == 'POST':
            shutil.copyfile(logo_dir + 'cisco_logo.png', logo_dir + 'logo.png')
        return HttpResponse(self.logopage)
    
mainpage = MainPage()

urlpatterns = [
    url(r'^dashboard/?', dashboard.dashboard),
    url(r'^account/login/?', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^account/logout/?', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^archon/logo/?', mainpage.sendLogoPage),
    url(r'^archon/mapping/?', views.mapping),
    url(r'^admin/?', admin.site.urls),
    url(r'^favicon\.ico', RedirectView.as_view(url='/resources/images/favicon.ico')),
    url(r'^', mainpage.sendMainPage),
]

def parse_urls(parent, urls):
    parent_url = '/' + '/'.join(parent)
    parent_name = '-'.join(parent)
    if isinstance(urls, list):
        ret = []
        for url in urls: ret.append(parse_urls(parent, url))
        return ret
    elif isinstance(urls, RegexURLResolver):
        term = re.sub('[\^/\?+*\$]|(\\\[wdW])', '', urls._regex)
        ret = []
        for url in urls.urlconf_name: ret.append(parse_urls(parent + [term], url))
        try: urls.namespace = urls.namespace[ARCHON_LANGUAGE]
        except: pass
        return {'name' : parent_name + '-' + term, 'display' : urls.namespace, 'urls' : ret}
    elif isinstance(urls, RegexURLPattern):
        term = re.sub('[\^/\?+*\$]|(\\\[wdW])', '', urls._regex)
        try: urls.name = urls.name[ARCHON_LANGUAGE]
        except: pass
        return {'name' : parent_name + '-' + term, 'display' : urls.name, 'url' : parent_url + '/' + term}
    return None

navbar_desc = []
print('1. Loading applications')
for app in ARCHON_APPLICATIONS:
    name = app['name']
    display = app['display']     
    path = 'application.' + name
    sys.stdout.write('%-40s =====> ' % ('%s : %s' % (display, path)))
    urls = include(path + '.urls')
    urlpatterns = [ url(r'^%s/' % name, urls) ] + urlpatterns
    navbar_desc.append({'name' : name, 'display' : display, 'urls' : parse_urls([name], urls[0].urlpatterns)})
    print('[ OK ]')
mainpage.setAppDesc(navbar_desc)
