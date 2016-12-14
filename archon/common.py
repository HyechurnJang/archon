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

import time
import threading
try: from Queue import Queue
except: from queue import Queue

class ArchonThread(threading.Thread):
    
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

class ArchonTask:
    def __init__(self, tick):
        self.schedtask_tick = tick
        self.schedtask_cur = 0
        
    def __sched_wrapper__(self, sched_tick):
        self.schedtask_cur += sched_tick
        if self.schedtask_cur >= self.schedtask_tick:
            self.schedtask_cur = 0
            self.sched()
            
    def sched(self): pass

class Scheduler(ArchonThread):
    
    def __init__(self, tick):
        ArchonThread.__init__(self)
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
