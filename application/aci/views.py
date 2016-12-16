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

from archon import *
from manager import Manager

from show import *
#===============================================================================
# Create your views here.
#===============================================================================

@pageview(Manager)
def device(Req, Man, View):
    if Req.Method == 'GET':
        plen = len(Req.Path)
        if plen > 4: return device_one(Req, Man, View)
        elif plen > 3: return device_all(Req, Man, View)
        else: return device_all(Req, Man, View)
     
@pageview(Manager)
def tenant(Req, Man, View):
    if Req.Method == 'GET':
        if len(Req.Path) > 3: return tenant_one(Req, Man, View)
        else: return tenant_all(Req, Man, View) 

@pageview(Manager)
def epg(Req, Man, View):
    return 'Endpoint Group'

@pageview(Manager)
def ep(Req, Man, View):
    return 'Endpoint'

@pageview(Manager)
def contract(Req, Man, View):
    return 'Contract'

@pageview(Manager)
def external(Req, Man, View):
    return 'External Network'

@pageview(Manager)
def fault(Req, Man, View):
    return 'Fault'


@pageview(Manager)
def intf_util(Req, Man, View):
    return 'Interface Utilization'

@pageview(Manager)
def epg_util(Req, Man, View):
    return 'Epg Utilization'


@pageview(Manager)
def eptracker(Req, Man, View):
    return 'EP Tracker'

@pageview(Manager)
def ofinder(Req, Man, View):
    return 'Object Finder'


@pageview(Manager)
def config(Req, Man, View):
    
    alert = None
    
    if Req.Method == 'POST':
        if Man.addDomain(Req.Data['domain_name'], Req.Data['ip'], Req.Data['user'], Req.Data['passwd']):
            alert = Alert(View('Connection Success'),
                          View('Setting %s with %s') % (Req.Data['ip'], Req.Data['domain_name']),
                          **{'class' : 'alert-success'})
        else:
            alert = Alert(View('Connection Failed'),
                          View('Incorrect Setting %s') % Req.Data['domain_name'],
                          **{'class' : 'alert-danger'})
        
    elif Req.Method == 'DELETE':
        if Man.delDomain(Req.Path[2]):
            alert = Alert(View('Disconnection Success'),
                          View('Erasing %s') % Req.Path[2],
                          **{'class' : 'alert-success'})
        else:
            alert = Alert(View('Disconnection Failed'),
                          View('Incorrect Erasing %s') % Req.Path[2],
                          **{'class' : 'alert-danger'})
    
    View.Menu.html(
        Modal(View('Register APIC Domain'), BUTTON(**{'class' : 'btn-primary', 'style' : 'float:right;'}).html(View('Connect APIC'))).html(
            Post('/aci/conf', View('Register'), **{'class' : 'btn-primary', 'style' : 'float:right;'}
            ).Text('domain_name', Post.TopLabel(View('APIC Domain Name')), placeholder=View('Unique Name Required')
            ).Text('ip', Post.TopLabel(View('APIC Address')), placeholder='XXX.XXX.XXX.XXX'
            ).Text('user', Post.TopLabel(View('Admin ID')), placeholder='admin'
            ).Password(label=Post.TopLabel(View('Password')))
        )
    )
    
    table = FooTable(View('Domain Name'), View('+APIC IP'), View('+Administrator ID'), View('+Start Connections'), View('+Max Connections'), '')
    
    for domain_name in Man:
        table.record(domain_name,
                     Man[domain_name]['ip'],
                     Man[domain_name]['user'],
                     Man[domain_name]['conns'],
                     Man[domain_name]['conn_max'],
                     DelButton('/aci/conf/' + domain_name, View('Delete'), tail=True))
    
    if alert != None: View.Page.html(alert)
    View.Page.html(table)





