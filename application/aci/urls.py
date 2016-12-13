# -*- coding: utf-8 -*-
'''
Created on 2016. 11. 14.

@author: Hye-Churn Jang
'''

from django.conf.urls import url, include

from . import views

url_show = [
    url(r'device/?', views.device, name=u'장치'),
    url(r'tenant/?', views.tenant, name=u'테넌트'),
    url(r'epg/?', views.epg, name=u'엔드포인트그룹'),
    url(r'ep/?', views.ep, name=u'엔드포인트'),
    url(r'contract/?', views.contract, name=u'컨트랙'),
    url(r'external/?', views.external, name=u'외부네트워크'),
    url(r'fault/?', views.fault, name=u'오류')
]

url_stat = [
    url(r'intf/?', views.intf_util, name=u'인터페이스 사용율'),
    url(r'epg/?', views.epg_util, name=u'엔드포인트그룹 사용율'),
]

url_tool = [
    url(r'eptracker/?', views.eptracker, name=u'엔드포인트 추적기'),
    url(r'ofinder/?', views.ofinder, name=u'오브젝트 검색기'),
]

urlpatterns = [
    url(r'show/', include(url_show, namespace=u'점검')),
    url(r'stat/', include(url_stat, namespace=u'분석')),
    url(r'tool/', include(url_tool, namespace=u'도구')),
    url(r'conf/?', views.config, name=u'설정'),
]

