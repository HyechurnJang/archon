# -*- coding: utf-8 -*-
'''
Created on 2016. 11. 14.

@author: Hye-Churn Jang
'''

from django.conf.urls import url, include

from . import views

url_show = [
    url(r'info/?', views.information, name=u'인포메이션'),
    url(r'doc/?', views.document, name=u'도큐먼트'),
    url(r'json/?', views.jsondata, name=u'제이슨')
]

url_l1 = [
    url(r'info/?', views.information, name='info'),
    url(r'doc/?', views.document, name='doc'),
    url(r'json/?', views.jsondata, name='json')
]

urlpatterns = [
    url(r'show/', include(url_show, namespace=u'쑈')),
    url(r'l1/', include(url_l1, namespace='L1')),
    url(r'info/?', views.information, name=u'인포메이션'),
    url(r'doc/?', views.document, name='Doc'),
    url(r'json/?', views.jsondata, name='Json')
]

