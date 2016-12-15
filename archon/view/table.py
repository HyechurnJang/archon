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

from core import *

class DataTable(VIEW):
    
    def __init__(self, *heads, **attrs):
        VIEW.setAttrs({'id' : VIEW.getUUID(), 'class' : 'table table-bordered table-hover', 'width' : '100%', 'lib' : 'datatable'}, attrs)
        VIEW.__init__(self, 'TABLE', **attrs)
        self.body = TBODY()
        tr = TR()
        for head in heads: tr.html(TH().html(head))
        self.html(THEAD().html(tr)).html(self.body)
        
    def record(self, *cols, **attrs):
        tr = TR(**attrs)
        for col in cols: tr.html(TD().html(col))
        self.body.html(tr)
        return self
    
    def __len__(self, *args, **kwargs):
        return self.body.__len__()

class FooTable(VIEW):
    
    def __init__(self, *heads, **attrs):
        VIEW.setAttrs({'id' : VIEW.getUUID(), 'class' : 'table', 'data-sorting' : 'true', 'data-show-toggle' : 'true', 'data-paging' : 'true', 'width' : '100%', 'lib' : 'footable'}, attrs)
        VIEW.__init__(self, 'TABLE', **attrs)
        self.body = TBODY()
        tr = TR()
        for head in heads:
            if '+' in head: tr.html(TH(**{'data-type' : 'html', 'data-breakpoints' : 'all', 'data-title' : head.replace('+', '')}).html(head))
            else: tr.html(TH(**{'data-type' : 'html'}).html(head))
        self.html(THEAD().html(tr)).html(self.body)
        
    def record(self, *cols, **attrs):
        tr = TR(**attrs)
        for col in cols: tr.html(TD(**{'data-type' : 'html'}).html(col))
        self.body.html(tr)
        return self
    
    def __len__(self, *args, **kwargs):
        return self.body.__len__()
