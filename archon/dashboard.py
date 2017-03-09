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

import importlib
from archon import *

from .settings import ARCHON_APPLICATIONS

class Manager(ManagerAbstraction):
    
    def __init__(self):
        pass

@pageview(Manager)
def dashboard(R, M, V):
    
    alen = len(ARCHON_APPLICATIONS)
    amod = alen % 4
    if alen <= 4:
        if amod == 0: col_size = 3
        elif amod == 1: col_size = 12
        elif amod == 2: col_size = 6
        elif amod == 3: col_size = 4
    else: col_size = 3
    
    app_jumbos = ROW()
    
    for app in ARCHON_APPLICATIONS:
        app_summary = importlib.import_module(app['src'] + '.manager').Manager.instance().getSummary(R, M, V)
        app_jumbos.html(
            COL(col_size).html(
                JUMBO(STYLE='padding:20px;').html(
                    DIV(STYLE='text-align:center;').html(
                        IMG('/resources/images/device/' + app_summary['icon'], STYLE='height:150px;'),
                        HEAD(1).html(app_summary['name'])
                    ),
                    DIV(STYLE='height:100px;text-align:center;').html(
                        PARA().html(app_summary['desc'])
                    )
                ).click(app_summary['link'])
            )
        )
    
    V.Page.html(
        ROW().html(
            COL(12).html(
                FLIPCLOCK()
            )
        ),
        app_jumbos
    )
