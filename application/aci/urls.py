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

from django.conf.urls import url, include
from . import views

#===============================================================================
# Link your view here.
#===============================================================================
url_show = [
    url(r'^host/?', views.host, name={'en' : 'Host', 'ko' : u'호스트'}),
    url(r'^device/?', views.device, name={'en' : 'Device', 'ko' : u'장치'}),
    url(r'^tenant/?', views.tenant, name={'en' : 'Tenant', 'ko' : u'테넌트'}),
    url(r'^epgroup/?', views.epg, name={'en' : 'EPG', 'ko' : u'엔드포인트그룹'}),
    url(r'^endpoint/?', views.endpoint, name={'en' : 'Endpoint', 'ko' : u'엔드포인트'}),
    url(r'^contract/?', views.contract, name={'en' : 'Contract', 'ko' : u'컨트랙'}),
    url(r'^external/?', views.external, name={'en' : 'External', 'ko' : u'외부네트워크'}),
    url(r'^fault/?', views.fault, name={'en' : 'Fault', 'ko' : u'오류'})
]

url_stat = [
    url(r'^epgstat/?', views.epg_util, name={'en' : 'EPG Util', 'ko' : u'엔드포인트그룹 사용율'}),
    url(r'^intfstat/?', views.intf_util, name={'en' : 'Interface Util', 'ko' : u'인터페이스 사용율'}),
    url(r'^acl_permit/?', views.acl_permit, name={'en' : 'Permit Packet', 'ko' : u'허용패킷로그'}),
    url(r'^acl_deny/?', views.acl_deny, name={'en' : 'Deny Packet', 'ko' : u'차단패킷로그'}),
]

url_tool = [
    url(r'^eptracker/?', views.eptracker, name={'en' : 'Endpoint Tracker', 'ko' : u'엔드포인트 추적기'}),
    url(r'^ofinder/?', views.ofinder, name={'en' : 'Object Finder', 'ko' : u'오브젝트 검색기'}),
]

urlpatterns = [
    url(r'^overview/?', views.overview, name={'en' : 'Overview', 'ko' : u'개요'}),
    url(r'^healthview/?', views.healthview, name={'en' : 'Health', 'ko' : u'상태'}),
    url(r'^topoview/?', views.topoview, name={'en' : 'Relation', 'ko' : u'관계도'}),
    url(r'^show/', include(url_show, namespace={'en' : 'Show', 'ko' : u'점검'})),
    url(r'^stat/', include(url_stat, namespace={'en' : 'Stat', 'ko' : u'분석'})),
    url(r'^tool/', include(url_tool, namespace={'en' : 'Tools', 'ko' : u'도구'})),
    url(r'^conf/?', views.config, name={'en' : 'Config', 'ko' : u'설정'}),
]

