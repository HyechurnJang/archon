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
import time

import pygics
import asadipy
import archon

from application import APPLICATION_CONFIGS

from models import *

#===============================================================================
# Create your manager here.
#===============================================================================

ASA_MONSEC = APPLICATION_CONFIGS['asa_health_monitor_sec']

class HealthMonitor(pygics.Task):
    
    def __init__(self, manager, mon_sec, mon_cnt):
        pygics.Task.__init__(self, tick=mon_sec)
        self.manager = manager
        self.count = mon_cnt
        self.health = {'_tstamp' : []}
        for i in reversed(range(0, mon_cnt)):
            self.health['_tstamp'].append('00:00:00')
        
    def task(self):
        now = time.strftime("%H:%M:%S", time.localtime(time.time()))
        stats = self.manager.Stat()
        health = {'_tstamp' : self.health['_tstamp'][1:]}
        health['_tstamp'].append(now)
        
        for domain_name in stats:
            dn_cpu = domain_name + '/cpu'
            dn_core = domain_name + '/core'
            dn_mem = domain_name + '/mem'
            dn_disk = domain_name + '/disk'
            
            if dn_cpu in self.health: health[dn_cpu] = self.health[dn_cpu][1:]
            else: health[dn_cpu] = [None for i in range(0, self.count - 1)]
            health[dn_cpu].append(stats[domain_name]['cpu']['total']['1min'])
            
            for i in range(0, len(stats[domain_name]['cpu']['core'])):
                dn_core_num = dn_core + '/%d' % i
                if dn_core_num in self.health: health[dn_core_num] = self.health[dn_core_num][1:]
                else: health[dn_core_num] = [None for j in range(0, self.count - 1)]
                health[dn_core_num].append(stats[domain_name]['cpu']['core'][i]['1min'])
            
            if dn_mem in self.health: health[dn_mem] = self.health[dn_mem][1:]
            else: health[dn_mem] = [None for i in range(0, self.count - 1)]
            health[dn_mem].append(stats[domain_name]['memory']['used_percent'])
            
            if dn_disk in self.health: health[dn_disk] = self.health[dn_disk][1:]
            else: health[dn_disk] = [None for i in range(0, self.count - 1)]
            health[dn_disk].append(stats[domain_name]['disk']['used_percent'])

        
        self.health = health
    
    def getHealth(self):
        return self.health

class Manager(archon.ManagerAbstraction, asadipy.MultiDomain):
    
    def __init__(self, mon_sec=ASA_MONSEC, mon_cnt=10, debug=False):
        asadipy.MultiDomain.__init__(self, conns=5, conn_max=10, debug=debug)
        self.scheduler = pygics.Scheduler(10)
        self.healthmon = HealthMonitor(self, mon_sec, mon_cnt)
        self.scheduler.register(self.healthmon)
        self.scheduler.start()
        domains = Domain.objects.all()
        for domain in domains:
            asadipy.MultiDomain.addDomain(self, domain.name, domain.ip, domain.user, domain.password)
    
    def addDomain(self, domain_name, ip, user, pwd):
        try: Domain.objects.get(name=domain_name)
        except:
            ret = asadipy.MultiDomain.addDomain(self, domain_name, ip, user, pwd)
            if ret: Domain.objects.create(name=domain_name, ip=ip, user=user, password=pwd)
            return ret
        return False
    
    def delDomain(self, domain_name):
        try: domain = Domain.objects.get(name=domain_name)
        except: return False
        asadipy.MultiDomain.delDomain(self, domain_name)
        domain.delete()
        return True

    def getHealth(self):
        return self.healthmon.getHealth()
    



