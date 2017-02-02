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
    active_intf = None
    
    # Detail
    kv = KeyVal()
    for key in node_data.keys(): kv.Data(key, node_data[key])
    nav.Tab(V('Details'), kv)
    
    # Topology
    topo = Topo()
    set_topo(topo, dn, color='red', dot=True)
    nav.Tab(V('Topology'), DIV(style='text-align:center;padding-top:10px;').html(topo))
    
    if hasattr(node_data, 'System'):
        if node_data['role'] != 'controller':
            data = M.getHealth()
            try: health = Chart.Line(*data['_tstamp'], **Chart.THEME_HEALTH).Data(dn, *data[domain_name + '/' + dn])
            except: pass
        kv = KeyVal()
        for key in node_data.System.keys(): kv.Data(key, node_data.System[key])
        nav.Tab(V('System'), kv)
        physif = node_data.System.PhysIf.list(detail=True, sort='id')
        if physif:
            phys_health = node_data.System.PhysIf.health()
            active_intf = ROW(style='margin-bottom:20px;')
            sort_phys_health = {}
            key = node_data.System.PhysIf.keys()
            table = FooTable(*['+' + k if k != 'id' else V('ID') for k in key])
            for pi in physif:
                table.Record(*[pi[k] for k in key])
                sort_phys_health[pi['id']] = None
            nav.Tab(V('Physical Interface'), table)
            for ph in phys_health: sort_phys_health[ph['name']] = ph['score']        
            for ph_name in sorted(sort_phys_health, key=lambda name: int(name.split('/')[1])):
                ph_val = sort_phys_health[ph_name]
                if ph_val != None:
                    if ph_val > 50:
                        active_intf.html(
                            COL(2, style='padding:0px 5px 0px 5px').html(
                                DIV(style='float:left;').html(Figure.Donut(ph_val, 100 - ph_val, height=20, **Figure.THEME_HEALTH)),
                                DIV(style='padding-left:22px;').html(ph_name)
                            )
                        )
                    else:
                        active_intf.html(
                            COL(2, style='padding:0px 5px 0px 5px').html(
                                DIV(style='float:left;').html(Figure.Donut(100 - ph_val, ph_val, height=20, **Figure.THEME_UTIL)),
                                DIV(style='padding-left:22px;').html(ph_name)
                            )
                        )
                else:
                    active_intf.html(
                        COL(2, style='padding:0px 5px 0px 5px').html(
                            DIV(style='float:left;').html(Figure.Donut(0, 100, height=20, **Figure.THEME_HEALTH)),
                            DIV(style='padding-left:22px;').html(ph_name)
                        )
                    )
    
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
    if active_intf != None:
        V.Page.html(
            HEAD(3).html(V('Active Interfaces')),
            active_intf
        )
    V.Page.html(nav)
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
