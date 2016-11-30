# -*- coding: utf-8 -*-
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
import json

from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.utils.decorators import method_decorator
from django.template import loader, Template, Context
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .settings import INSTALLED_APPS

class MainPage:
    
    def __init__(self):
        self.mainpage = loader.get_template('mainpage.html')
        
    def parseUrlToHtml(self, desc):
        if 'urls' in desc:
            ret = '<li class="dropdown">'
            ret += '<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">%s<span class="caret"></span></a>' % desc['display']
            ret += '<ul class="dropdown-menu" role="menu">'
            for url in desc['urls']: ret += self.parseUrlToHtml(url)
            ret += '</ul></li>'
            return ret
        elif 'url' in desc:
            return '<li><a href="%s">%s</a></li>' % (desc['url'], desc['display'])
        return ''
        
    def setNavbar(self, desc):
        applications = ''
        navigations = ''
        for app in desc:
            applications += '<a class="app-selector" href="#" app="#%s">%s</a>' % (app['name'], app['display'])
            navigations += '<ul class="nav navbar-nav app" id="%s">' % app['name']
            for url in app['urls']:
                navigations += self.parseUrlToHtml(url)
            navigations += '</ul>'
        applications = Template(applications).render(Context())
        navigations = Template(navigations).render(Context())
        self.mainpage = self.mainpage.render({'applications' : applications, 'navigations' : navigations})

    @method_decorator(login_required)
    def sendMainPage(self, request):
        return HttpResponse(self.mainpage)
    
    
mainpage = MainPage()

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/resources/images/favicon.ico')),
    url(r'account/login/?$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'account/logout/?$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^', mainpage.sendMainPage),
]

def parse_urls(base_url, urls):
    if isinstance(urls, list):
        ret = []
        for url in urls: ret.append(parse_urls(base_url, url))
        return ret
    elif isinstance(urls, RegexURLResolver):
        term = re.sub('[/\?+*]|(\\\[wdW])', '', urls._regex)
        ret = []
        for url in urls.urlconf_name: ret.append(parse_urls(base_url + '/' + term, url))
        return {'name' : term, 'display' : urls.namespace, 'urls' : ret}
    elif isinstance(urls, RegexURLPattern):
        term = re.sub('[/\?+*]|(\\\[wdW])', '', urls._regex)
        return {'name' : term, 'display' : urls.name, 'url' : base_url + '/' + term}
    return None

application_names = __import__('application').APPLICATION_NAMES

navbar_desc = []
for app in INSTALLED_APPS:
    if 'application.' in app:
        name = app.split('application.')[1]
        if name in application_names: display = application_names[name]
        else: display = name.upper()
        app_urls = include(app + '.urls')
        urlpatterns = [ url(r'^%s/' % name, app_urls) ] + urlpatterns
        navbar_desc.append({'name' : name, 'display' : display, 'urls' : parse_urls(name, app_urls[0].urlpatterns)})

# print json.dumps(navbar_desc, indent=2)
mainpage.setNavbar(navbar_desc)
    
