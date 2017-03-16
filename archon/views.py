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

import shutil
import settings

from archon import *
from settings import BASE_DIR, STATIC_DIR
from .manager import Manager

@pageview(Manager)
def mapping(R, M, V):
    if R.Method == 'POST' and 'mapper' in R.Data:
        with open(BASE_DIR + '/' + STATIC_DIR + '/files/macip.xlsx', 'wb+') as fd:
            fd.write(R.Data['mapper'].read())
        M.INV.reloadMACIP()
    
    mac_table = TABLE.BASIC(V('MAC'), V('Name'))
    ip_table = TABLE.BASIC(V('IP'), V('Name'))
    nav = NAV(STYLE='margin-top:10px;')
    nav.Tab('MAC Mapper', DIV(STYLE='margin-top:5px;').html(mac_table))
    nav.Tab('IP Mapper', DIV(STYLE='margin-top:5px;').html(ip_table))
    
    for mac, name in M.INV.MAC.items(): mac_table.Record(mac, name)
    for ip, name in M.INV.IP.items(): ip_table.Record(ip, name)
    
    V.Page.html(
        UPLOAD('/archon/mapping', 'mapper', V('Select MAC & IP File'), V('Upload')),
        ANCH(CLASS='btn btn-success', href='/resources/files/macip.xlsx', STYLE='width:100%;').html(
            ICON('arrow-circle-down'), ' ', 'Download'
        ),
        nav
    )
    