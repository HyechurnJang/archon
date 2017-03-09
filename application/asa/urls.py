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
    url(r'^static_nat/?$', views.static_nat, name='Static NAT'),
    url(r'^dynamic_nat/?$', views.dynamic_nat, name='Dynamic NAT'),
    url(r'^pat_pool/?$', views.pat_pool, name='PAT Pool'),
    url(r'^graph_pat_pool/?$', views.pat_pool_graph, name='PAT Pool Graph'),
]

# url_conf = [
#     url(r'^ipuser/?', views.config_ipuser, name={'en' : 'IP User', 'ko' : u'IP 사용자 설정'}),
#     url(r'^domain/?', views.config_domain, name={'en' : 'Domain', 'ko' : u'도메인 설정'}),
# ]

urlpatterns = [
    url(r'^overview/?$', views.overview, name={'en' : 'Overview', 'ko' : u'개요'}),
    url(r'^show/', include(url_show, namespace={'en' : 'Show', 'ko' : u'점검'})),
    url(r'^conf/?$', views.config, name={'en' : 'Config', 'ko' : u'설정'}),
]
