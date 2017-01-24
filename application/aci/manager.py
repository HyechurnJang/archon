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

import acidipy
import archon
import pygics

from models import *

#===============================================================================
# Create your manager here.
#===============================================================================

APIC_MONSEC = 5

class HealthMonitor(pygics.Task):
    
    def __init__(self, manager, mon_sec, mon_cnt):
        pygics.Task.__init__(self, tick=mon_sec)
        self.manager = manager
        self.count = mon_cnt
        self.health = {'_tstamp' : []}
        init_time = time.time()
        for i in reversed(range(0, mon_cnt)):
            self.health['_tstamp'].append('00:00:00')
        
    def getNewHealthHist(self, dn, score):
        if dn in self.health:
            ret = self.health[dn][1:]
            ret.append(score)
            return ret
        else:
            ret = []
            for i in range(0, self.count - 1): ret.append(0)
            ret.append(score)
            return ret
        
    def getHealth(self):
        return self.health
    
    def task(self):
        now = time.strftime("%H:%M:%S", time.localtime(time.time()))
        
        total = self.manager.health()
        pod = self.manager.Pod.health()
        node = self.manager.Node.health()        
        tenant = self.manager.Tenant.health()
        appprof = self.manager.AppProfile.health()
        epg = self.manager.EPG.health()
        
        health = {'_tstamp' : self.health['_tstamp'][1:]}
        health['_tstamp'].append(now)
        
        for dom_name in total: health[dom_name] = self.getNewHealthHist(dom_name, total[dom_name]['score'])
        for dom_name in pod:
            for dp in pod[dom_name]:
                dn = dom_name + '/' + dp['dn']
                health[dn] = self.getNewHealthHist(dn, dp['score'])
        for dom_name in node:
            for dp in node[dom_name]:
                dn = dom_name + '/' + dp['dn']
                health[dn] = self.getNewHealthHist(dn, dp['score'])
        for dom_name in tenant:
            for dp in tenant[dom_name]:
                dn = dom_name + '/' + dp['dn']
                health[dn] = self.getNewHealthHist(dn, dp['score'])
        for dom_name in appprof:
            for dp in appprof[dom_name]:
                dn = dom_name + '/' + dp['dn']
                health[dn] = self.getNewHealthHist(dn, dp['score'])
        for dom_name in epg:
            for dp in epg[dom_name]:
                dn = dom_name + '/' + dp['dn']
                health[dn] = self.getNewHealthHist(dn, dp['score'])
        
        
        self.health = health
    
class EndpointTracker(acidipy.SubscribeHandler):
    
    @classmethod
    def initDatabase(cls):
        EPTracker.objects.all().delete()
        pass
    
    def __init__(self, manager, domain_name):
        self.manager = manager
        self.domain_name = domain_name
        self.getInitData()
        
    def convertTstamp(self, tstamp):
        (resp_ts, remaining) = tstamp.split('T')
        resp_ts += ' '
        resp_ts = resp_ts + remaining.split('+')[0].split('.')[0]
        return resp_ts
    
    def getIfName(self, ep):
        epcs = ep.Class('fvRsCEpToPathEp').list(sort='dn')
        if_dn = []
        for epc in epcs:
            if_dn.append(re.sub('(topology/|pod-|protpaths-|paths-|pathep-|\[|\])', '', epc['tDn']))
        return if_dn
    
    def getInitData(self):
        ep_list = self.manager[self.domain_name].Endpoint.list(detail=True)
        for ep in ep_list:
            sdn = ep['dn'].split('/')
            try:
                ept = EPTracker.objects.get(domain=self.domain_name,
                                            dn=ep['dn'],
                                            start=self.convertTstamp(ep['modTs']),
                                            stop='0000-00-00 00:00:00')
            except:
                EPTracker.objects.create(mac=ep['mac'],
                                         ip=ep['ip'],
                                         domain=self.domain_name,
                                         tenant=sdn[1].replace('tn-', ''),
                                         app=sdn[2].replace('ap-', ''),
                                         epg=sdn[3].replace('epg-', ''),
                                         dn=ep['dn'],
                                         intf=','.join(self.getIfName(ep)),
                                         start=self.convertTstamp(ep['modTs']),
                                         stop='0000-00-00 00:00:00')
            
    def subscribe(self, status, obj):
        
        sdn = obj['dn'].split('/')
        tenant = sdn[1].replace('tn-', '')
        app = sdn[2].replace('ap-', '')
        epg = sdn[3].replace('epg-', '')
        mac = obj['mac']
        ip = obj['ip']

        try:        
            ept = EPTracker.objects.get(mac=mac,
                                        domain=self.domain_name,
                                        tenant=tenant,
                                        app=app,
                                        epg=epg,
                                        stop='0000-00-00 00:00:00')
            ept.update(stop=self.convertTstamp(obj['modTs']))
        except: pass
        
        EPTracker.objects.create(mac=mac,
                                 ip=ip,
                                 domain=self.domain_name,
                                 tenant=sdn[1].replace('tn-', ''),
                                 app=sdn[2].replace('ap-', ''),
                                 epg=sdn[3].replace('epg-', ''),
                                 dn=obj['dn'],
                                 intf=', '.join(self.getIfName(obj)),
                                 start=self.convertTstamp(obj['modTs']),
                                 stop='0000-00-00 00:00:00')
        

class Manager(archon.ManagerAbstraction, acidipy.MultiDomain):
    
    def __init__(self, mon_sec=APIC_MONSEC, mon_cnt=10, debug=False):
        acidipy.MultiDomain.__init__(self, conns=5, conn_max=10, debug=debug)
        self.scheduler = pygics.Scheduler(10)
        self.healthmon = HealthMonitor(self, mon_sec, mon_cnt)
        self.scheduler.register(self.healthmon)
        self.scheduler.start()
        domains = Domain.objects.all()
        for domain in domains:
            ret = acidipy.MultiDomain.addDomain(self, domain.name, domain.controllers, domain.user, domain.password)
            if ret:
                self[domain.name].eptracker = EndpointTracker(self, domain.name)
                self[domain.name].Endpoint.subscribe(self[domain.name].eptracker)
    
    def addDomain(self, domain_name, ip, user, pwd):
        try: Domain.objects.get(name=domain_name)
        except:
            ret = acidipy.MultiDomain.addDomain(self, domain_name, ip, user, pwd)
            if ret:
                Domain.objects.create(name=domain_name, controllers=ip, user=user, password=pwd)
                self[domain_name].eptracker = EndpointTracker(self, domain_name)
                self[domain_name].Endpoint.subscribe(self[domain_name].eptracker)
            return ret
        return False
    
    def delDomain(self, domain_name):
        try: domain = Domain.objects.get(name=domain_name)
        except: return False
        acidipy.MultiDomain.delDomain(self, domain_name)
        domain.delete()
        return True

    def getHealth(self):
        return self.healthmon.getHealth()
    
    def initEndpoint(self):
        EndpointTracker.initDatabase()
        for domain_name in self: self[domain_name].eptracker.getInitData()