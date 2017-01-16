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
from common import *

def device_all(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    if len(R.Path) > 3: node_data = M.Node.list(role=R.Path[3], detail=True, sort='id')
    else: node_data = M.Node.list(detail=True, sort='id')
    tsys_data = M.System.list(detail=True)
    frm_data = M.Class('firmwareARunning').list(detail=True)
    
    #===========================================================================
    # Logic
    #===========================================================================
    for domain_name in M:
        table = DataTable(V('ID'), V('Type'), V('Name'), V('Model'), V('Serial'), V('Version'), V('Management IP'), V('State'), V('Fabric State'), V('Uptime'))
        
        cnt_ctrl = 0
        cnt_spne = 0
        cnt_leaf = 0
         
        for node in node_data[domain_name]:
            id = node['id']
            for tsys in tsys_data[domain_name]:
                if node['dn'] + '/' in tsys['dn']:
                    mgmt = '<p>' + tsys['oobMgmtAddr'] + ' <small>[' + tsys['inbMgmtAddr'] + ']</small></p>'
                    state = tsys['state']
                    uptime = tsys['systemUpTime'][:-4]
                    break
            else:
                mgmt = ' '
                state = ' '
                uptime = ' '
            
            for frm in frm_data[domain_name]:
                if node['dn'] + '/' in frm['dn']: version = frm['version']; break
            else: version = ' '
            
            if node['role'] == 'leaf':
                cnt_leaf += 1
                role = 'Leaf'
            elif node['role'] == 'spine':
                cnt_spne += 1
                role = 'Spine'
            elif node['role'] == 'controller':
                cnt_ctrl += 1
                role = 'Controller'
            
            table.Record(id,
                         role,
                         Get('/aci/show/device/%s/%s' % (domain_name, node['dn'])).html(node['name']),
                         node['model'],
                         node['serial'],
                         version,
                         mgmt,
                         state,
                         node['fabricSt'],
                         uptime)
            
    #===========================================================================
    # View
    #===========================================================================
        V.Page.html(HEAD(1).html('%s %s' % (domain_name, V('Domain'))))
        if len(R.Path) < 4:
            V.Page.html(
                ROW().html(
                    COL(4).html(
                        CountPanel(V('Controller'), 'map-signs', cnt_ctrl, **(ATTR.click('/aci/show/device/controller') + {'class' : 'panel-dgrey'}))
                    ),
                    COL(4).html(
                        CountPanel(V('Spine'), 'tree', cnt_spne, **(ATTR.click('/aci/show/device/spine') + {'class' : 'panel-dgrey'}))
                    ),
                    COL(4).html(
                        CountPanel(V('Leaf'), 'leaf', cnt_leaf, **(ATTR.click('/aci/show/device/leaf') + {'class' : 'panel-dgrey'}))
                    )
                )
            )
        V.Page.html(table)
    
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))

def device_one(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    node_data = M[domain_name](dn, detail=True)
    
    #===========================================================================
    # Logic
    #===========================================================================
    nav = Navigation()
    health = None
    
    # Detail
    kv = KeyVal()
    for key in node_data.attrs(): kv.Data(key, node_data[key])
    nav.Tab(V('Details'), kv)
    
    # Topology
    topo = Topo()
    set_topo(topo, dn, color='red', dot=True)
    nav.Tab(V('Topology'), DIV(style='text-align:center;padding-top:10px;').html(topo))
    
    if hasattr(node_data, 'System'):
        if node_data['role'] != 'controller':
            data = M.getHealth()
            try: health = HealthLine(*data['_tstamp']).Data(dn, *data[domain_name + '/' + dn])
            except: pass
        kv = KeyVal()
        for key in node_data.System.attrs(): kv.Data(key, node_data.System[key])
        nav.Tab(V('System'), kv)
        physif = node_data.System.PhysIf.list(detail=True, sort='id')
        if physif:
            key = node_data.System.PhysIf.attrs()
            table = FooTable(*['+' + k if k != 'id' else V('ID') for k in key])
            for pi in physif: table.Record(*[pi[k] for k in key])
            nav.Tab(V('Physical Interface'), table)
    
    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(HEAD(1).html(node_data['name']))
    if health != None: V.Page.html(ROW().html(health))
    V.Page.html(
        HEAD(3).html(V('Model')),
        HEAD(4).html(node_data['vendor'] + ' ' + node_data['model']),
        HEAD(4).html(node_data['serial'])
    )
    V.Page.html(nav)
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
