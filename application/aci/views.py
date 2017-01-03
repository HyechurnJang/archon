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
def overview(R, M, V):
    health = M.getHealth()
    
    topo_hist = Line(*health['_tstamp'], **(Chart.NOXLY100 + Chart.RATIO_2 + Chart.NOLEGEND))
    node_hist = Line(*health['_tstamp'], **(Chart.NOXLY100 + Chart.RATIO_4 + Chart.NOLEGEND))
    epgs_hist = Line(*health['_tstamp'], **(Chart.NOXLY100 + Chart.RATIO_2 + Chart.NOLEGEND))
    
    node_cur = []
    epgs_cur = []
    
    dns = health.keys()
    
    for dn in dns:
        if dn == '_tstamp': continue
        elif '/epg-' in dn:
            name = re.sub('(uni/|tn-|ap-|epg-)', '', dn)
            epgs_hist.Data(name, fill=False, *health[dn])
            epgs_cur.append((name, health[dn][-1]))
        elif '/node-' in dn:
            name = re.sub('(topology/|pod-|node-)', '', dn)
            node_hist.Data(name, fill=False, *health[dn])
            node_cur.append((name, health[dn][-1]))
        elif '/' not in dn or '/topology' in dn:
            topo_hist.Data(dn, fill=False, *health[dn])
    
    node_cols = []
    node_vals = []
    epgs_cols = []
    epgs_vals = []
    node_cur = sorted(node_cur, key=lambda node: node[1])
    epgs_cur = sorted(epgs_cur, key=lambda node: node[1])
    for nc in node_cur: node_cols.append(nc[0]); node_vals.append(nc[1])
    for ec in epgs_cur: epgs_cols.append(ec[0]); epgs_vals.append(ec[1])
    
    node_now = HealthBar(*node_cols, **(Chart.NOXLY100 + Chart.RATIO_4 + Chart.NOLEGEND)).Data(V('Current Health'), *node_vals)
    epgs_now = HealthBar(*epgs_cols, **(Chart.NOXLY100 + Chart.RATIO_2 + Chart.NOLEGEND)).Data(V('Current Health'), *epgs_vals)
    
    
    V.Page.html(
        ROW().html(
            COL(6).html(topo_hist),
            COL(6).html(
                ROW().html(
                    COL(12).html(node_hist)
                ),
                ROW().html(
                    COL(12).html(node_now)
                ),
            ),
        ),
        ROW().html(
            COL(6).html(epgs_hist),
            COL(6).html(epgs_now)
        )
    )
    
@pageview(Manager)
def host(R, M, V):
    if R.Method == 'GET':
        if len(R.Path) > 3: return host_one(R, M, V)
        else: return host_all(R, M, V)

@pageview(Manager)
def device(R, M, V):
    if R.Method == 'GET':
        plen = len(R.Path)
        if plen > 4: return device_one(R, M, V)
        elif plen > 3: return device_all(R, M, V)
        else: return device_all(R, M, V)
     
@pageview(Manager)
def tenant(R, M, V):
    if R.Method == 'GET':
        if len(R.Path) > 3: return tenant_one(R, M, V)
        else: return tenant_all(R, M, V) 

@pageview(Manager)
def epg(R, M, V):
    if R.Method == 'GET':
        if len(R.Path) > 3: return epg_one(R, M, V)
        else: return epg_all(R, M, V)
    
@pageview(Manager)
def endpoint(R, M, V):
    if R.Method == 'GET':
        if len(R.Path) > 3: return ep_one(R, M, V)
        else: return ep_all(R, M, V)

@pageview(Manager)
def contract(R, M, V):
    return 'Contract'

@pageview(Manager)
def external(R, M, V):
    return 'External Network'

@pageview(Manager)
def fault(R, M, V):
    return 'Fault'


@pageview(Manager)
def intf_util(R, M, V):
    return 'Interface Utilization'

@pageview(Manager)
def epg_util(R, M, V):
    return 'Epg Utilization'


@pageview(Manager)
def eptracker(R, M, V):
    return 'EP Tracker'

@pageview(Manager)
def ofinder(R, M, V):
    return 'Object Finder'


@pageview(Manager)
def config(R, M, V):
    
    alert = None
    
    if R.Method == 'POST':
        if M.addDomain(R.Data['domain_name'], R.Data['ip'], R.Data['user'], R.Data['password']):
            alert = Alert(V('Connection Success'),
                          V('Setting %s with %s') % (R.Data['ip'], R.Data['domain_name']),
                          **{'class' : 'alert-success'})
        else:
            alert = Alert(V('Connection Failed'),
                          V('Incorrect Setting %s') % R.Data['domain_name'],
                          **{'class' : 'alert-danger'})
        
    elif R.Method == 'DELETE':
        if M.delDomain(R.Path[2]):
            alert = Alert(V('Disconnection Success'),
                          V('Erasing %s') % R.Path[2],
                          **{'class' : 'alert-success'})
        else:
            alert = Alert(V('Disconnection Failed'),
                          V('Incorrect Erasing %s') % R.Path[2],
                          **{'class' : 'alert-danger'})
    
    V.Menu.html(
        Modal(V('Register APIC Domain'), BUTTON(**{'class' : 'btn-primary', 'style' : 'float:right;'}).html(V('Connect APIC'))).html(
            Post('/aci/conf', V('Register'), **{'class' : 'btn-primary', 'style' : 'float:right;'}
            ).Text('domain_name', Post.TopLabel(V('APIC Domain Name')), placeholder=V('Unique Name Required')
            ).Text('ip', Post.TopLabel(V('APIC Address')), placeholder='XXX.XXX.XXX.XXX'
            ).Text('user', Post.TopLabel(V('Admin ID')), placeholder='admin'
            ).Password(label=Post.TopLabel(V('Password')))
        )
    )
    
    table = FooTable(V('Domain Name'), V('+APIC IP'), V('+Administrator ID'), V('+Start Connections'), V('+Max Connections'), '')
    
    for domain_name in M:
        table.Record(domain_name,
                     M[domain_name]['ip'],
                     M[domain_name]['user'],
                     M[domain_name]['conns'],
                     M[domain_name]['conn_max'],
                     DelButton('/aci/conf/' + domain_name, V('Delete'), tail=True))
    
    if alert != None: V.Page.html(alert)
    V.Page.html(table)





