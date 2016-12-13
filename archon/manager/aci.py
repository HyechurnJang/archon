'''
Created on 2016. 12. 6.

@author: Hye-Churn Jang
'''

import re
import time
import threading
try: from Queue import Queue
except: from queue import Queue

import acidipy
import archon

from application.aci.models import *

class SystemThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self._tb_sw = False
        
    def start(self):
        if not self._tb_sw:
            self._tb_sw = True
            threading.Thread.start(self)
    
    def stop(self):
        if self._tb_sw:
            self._tb_sw = False
            try: self._Thread__stop()
            except:
                try: self._stop()
                except:
                    try: self.__stop()
                    except: pass
            self.join()
        
    def run(self):
        while self._tb_sw: self.thread()
            
    def thread(self): pass

class SchedTask:
    def __init__(self, tick):
        self.schedtask_tick = tick
        self.schedtask_cur = 0
        
    def __sched_wrapper__(self, sched_tick):
        self.schedtask_cur += sched_tick
        if self.schedtask_cur >= self.schedtask_tick:
            self.schedtask_cur = 0
            self.sched()
            
    def sched(self): pass

class Scheduler(SystemThread):
    
    def __init__(self, tick):
        SystemThread.__init__(self)
        self.tick = tick
        self.queue = []
        self.regreq = Queue()
    
    def thread(self):
        start_time = time.time()
        while not self.regreq.empty():
            task = self.regreq.get()
            self.queue.append(task)
        for task in self.queue:
            try: task.__sched_wrapper__(self.tick)
            except: continue
        end_time = time.time()
        sleep_time = self.tick - (end_time - start_time)
        if sleep_time > 0: time.sleep(sleep_time)
        
            
    def register(self, task):
        self.regreq.put(task)
        
    def unregister(self, task):
        sw_stat = self._tb_sw
        if sw_stat: self.stop()
        if task in self.queue: self.queue.remove(task)
        if sw_stat: self.start()

class HealthMonitor(SchedTask):
    
    def __init__(self, manager, mon_sec, mon_cnt):
        SchedTask.__init__(self, tick=mon_sec)
        self.manager = manager
        self.count = mon_cnt
        self.health = {'_tstamp' : []}
        init_time = time.time()
        for i in reversed(range(0, mon_cnt)):
            self.health['_tstamp'].append(time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(init_time - (mon_sec * (i + 1)))))
        
    def getNewHealthHist(self, dn, score):
        if dn in self.health:
            ret = self.health[dn][1:]
            ret.append(score)
            return ret
        else:
            ret = []
            for i in range(0, self.count - 1): ret.append(None)
            ret.append(score)
            return ret
        
    def getHealth(self):
        return self.health
    
    def sched(self):
        now = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))
        
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
        epcs = ep.children()
        if_dn = []
        for epc in epcs:
            if 'tDn' in epc: if_dn.append(re.sub('(topology/|pod-|protpaths-|paths-|pathep-|\[|\])', '', epc['tDn']))
        return if_dn
    
    def getInitData(self):
        ep_list = self.manager[self.domain_name].Endpoint.list(detail=True)
        for ep in ep_list:
            sdn = ep['dn'].split('/')
            EPTracker.objects.create(mac=ep['mac'],
                                         ip=ep['ip'],
                                         domain=self.domain_name,
                                         tenant=sdn[1].replace('tn-', ''),
                                         app=sdn[2].replace('ap-', ''),
                                         epg=sdn[3].replace('epg-', ''),
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
                                     intf=', '.join(self.getIfName(obj)),
                                     start=self.convertTstamp(obj['modTs']),
                                     stop='0000-00-00 00:00:00')
        

class ACIManager(archon.Manager, acidipy.MultiDomain):
    
    def __init__(self, mon_sec=5, mon_cnt=10, debug=False):
        acidipy.MultiDomain.__init__(self, conns=5, conn_max=10, debug=debug)
        EndpointTracker.initDatabase()
        self.scheduler = Scheduler(2)
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
