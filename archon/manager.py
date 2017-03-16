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

import re
import archon

from openpyxl import load_workbook
from .settings import BASE_DIR, STATIC_DIR
from archon import *

#===============================================================================
# Create your manager here.
#===============================================================================

class Inventory(dict):
    
    class InvDict(dict):
        def __init__(self): dict.__init__(self)
        def Get(self, key):
            if key in self: return self[key]
            return None
    
    def __init__(self):
        dict.__init__(self)
        self.initMACIP()
        
    def initMACIP(self):
        self._macip_file_path = BASE_DIR + '/' + STATIC_DIR + '/files/macip.xlsx'
        self['MAC'] = None
        self['IP'] = None
        self.reloadMACIP()
        
    def reloadMACIP(self):
        mac = Inventory.InvDict()
        ip = Inventory.InvDict()
        wb = load_workbook(filename=self._macip_file_path)
        sheet = wb['address']
        sheet_macip = sheet['A']
        sheet_name = sheet['B']
        idx = 1
        for macip in sheet_macip[1:]:
            mi = macip.value
            if re.search('\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', mi):
                key = re.sub('\s', '', mi).upper()
                name = sheet_name[idx].value
                mac[key] = name
            elif re.search('\d+\.\d+\.\d+\.\d+', mi):
                key = re.sub('\s', '', mi)
                name = sheet_name[idx].value
                ip[key] = name
            idx += 1
        self['MAC'] = mac
        self['IP'] = ip
    
    @property
    def MAC(self): return self['MAC']
    
    @property
    def IP(self): return self['IP']

class Manager(archon.ManagerAbstraction):
    
    def __init__(self):
        self.INV = Inventory()
