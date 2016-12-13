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
        
        self.app_selectors = Template(app_selectors).render(Context())
        self.page_selectors = Template(page_selectors).render(Context())
        self.pages = Template(pages).render(Context())
        self.admin = Template('<li><a href="/admin/">Admin</a></li>').render(Context())
        self.user = Template('').render(Context())

    @method_decorator(login_required)
    def sendMainPage(self, request):
        if request.user.is_superuser:
            return HttpResponse(self.mainpage.render({'app_selectors' : self.app_selectors,
                                                      'page_selectors' : self.page_selectors,
                                                      'user_menu' : self.admin,
                                                      'pages' : self.pages}))
        else:
            return HttpResponse(self.mainpage.render({'app_selectors' : self.app_selectors,
                                                      'page_selectors' : self.page_selectors,
                                                      'user_menu' : self.user,
                                                      'pages' : self.pages}))
    
mainpage = MainPage()


urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/resources/images/favicon.ico')),
    url(r'account/login/?$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'account/logout/?$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
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
        term = re.sub('[/\?+*]|(\\\[wdW])', '', urls._regex)
        ret = []
        for url in urls.urlconf_name: ret.append(parse_urls(parent + [term], url))
        return {'name' : parent_name + '-' + term, 'display' : urls.namespace, 'urls' : ret}
    elif isinstance(urls, RegexURLPattern):
        term = re.sub('[/\?+*]|(\\\[wdW])', '', urls._regex)
        return {'name' : parent_name + '-' + term, 'display' : urls.name, 'url' : parent_url + '/' + term}
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
        navbar_desc.append({'name' : name, 'display' : display, 'urls' : parse_urls([name], app_urls[0].urlpatterns)})

mainpage.setAppDesc(navbar_desc)
    
