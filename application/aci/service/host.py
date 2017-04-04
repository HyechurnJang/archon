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

def host_all(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    host_data, nic_data = Burst(
    )(M.Class('compHost').list, detail=True, sort=['type', 'dn']
    )(M.Class('compNic').list, detail=True
    ).do()

    #===========================================================================
    # Logic
    #===========================================================================
    for domain_name in sorted(M.keys()):
        cnt_phy = 0
        cnt_hv = 0
        cnt_vm = 0
        
        ph_table = TABLE.BASIC(V('OID'), V('Name'), V('IP'), V('MAC'), V('OS'), V('State'))
        vm_table = TABLE.BASIC(V('OID'), V('Name'), V('IP'), V('MAC'), V('OS'), V('State'))
        hv_table = TABLE.FLIP(V('OID'), V('Name'), V('OS'), V('State'), V('+Interfaces'))
        
        for host in host_data[domain_name]:
            if host.class_name in ['compPhys', 'compVm']:
                dn = host['dn']
                oid = GET('/aci/show/host/%s/%s' % (domain_name, dn)).html(host['oid'])
                ip_data = ' '
                mac_data = ' '
                dn2nic = dn + '/'
                os_name, _ = get_host_os(V, host['os'], host['cfgdOs'])
                for nic in nic_data[domain_name]:
                    if dn2nic in nic['dn']:
                        ip_data += '<p><small>' + get_ip_name(nic['ip']) + ',&nbsp;</small></p>'
                        mac_data += '<p><small>' + get_mac_name(nic['mac']) + ',&nbsp;</small></p>'
                if host.class_name == 'compPhys':
                    cnt_phy += 1
                    ph_table.Record(oid, host['name'], ip_data, mac_data, os_name, host['state'])
                elif host.class_name == 'compVm':
                    cnt_vm += 1
                    vm_table.Record(oid, host['name'], ip_data, mac_data, os_name, host['state'])
            elif host.class_name == 'compHv':
                cnt_hv += 1
                dn = host['dn']
                oid = GET('/aci/show/host/%s/%s' % (domain_name, dn)).html(host['oid'])
                ipmac = ' '
                dn2nic = dn + '/'
                os_name, _ = get_host_os(V, host['dn'])
                for nic in nic_data[domain_name]:
                    if dn2nic in nic['dn']:
                        if nic.class_name == 'compHpNic':
                            ipmac += '<p>Hypervisor NIC&nbsp;:&nbsp;' + nic['mac'] + '&nbsp;:&nbsp;' + nic['ip'] + '</p>'
                        elif nic.class_name == 'compMgmtNic':
                            ipmac += '<p>Management NIC&nbsp;:&nbsp;' + nic['mac'] + '&nbsp;:&nbsp;' + nic['ip'] + '</p>'
                hv_table.Record(oid, get_ip_name(host['name']), os_name, host['state'], ipmac)
    
    #===========================================================================
    # View
    #===========================================================================
        V.Page.html(
            HEAD(1).html('%s %s' % (domain_name, V('Domain'))),
            ROW().html(
                COL(4).html(COUNTER(V('Physical Hosts'), 'server', cnt_phy, CLASS='panel-dgrey')),
                COL(4).html(COUNTER(V('Virtual Hosts'), 'cube', cnt_vm, CLASS='panel-dgrey')),
                COL(4).html(COUNTER(V('Hypervisor'), 'cubes', cnt_hv, CLASS='panel-dgrey'))
            )
        )
        if ph_table:
            V.Page.html(
                HEAD(3).html(V('Physical Hosts')),
                ph_table,
            )
        if vm_table:
            V.Page.html(
                HEAD(3).html(V('Virtual Hosts')),
                vm_table,
            )
        if hv_table:
            V.Page.html(
                HEAD(3).html(V('Hypervisor')),
                hv_table
            )
    
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))
        
def host_one(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    host_data = M[domain_name](dn, detail=True)
    children = host_data.children(detail=True)

    #===========================================================================
    # Logic
    #===========================================================================
    nav = NAV()
    
    name = '[%s] %s <small>%s</small>' % (host_data['oid'].upper(), host_data['name'], get_host_type(V, host_data['type']))
    desc = host_data['descr']
    pw_stat, pw_img = get_power_stat(V, host_data['state'])
    
    # Detail
    kv = KEYVAL()
    for key in host_data.keys(): kv.Data(key, host_data[key])
    nav.Tab(V('Details'), kv)
    
    # Topology
    topo = TOPO()
    set_topo(topo, dn, color='red', path_color='green', dot=True)
    nav.Tab(V('Topology'), DIV(STYLE='text-align:center;padding-top:10px;').html(topo))
    
    nics = []
    
    if host_data.class_name == 'compPhys':
        os_name, os_img = get_host_os(V, host_data['os'])
        
        key = M[domain_name].Class('compPpNic').keys()
        table = TABLE.FLIP(*['+' + k if k != 'name' else V('NIC Name') for k in key])
        for child in children:
            if child.class_name == 'compPpNic':
                table.Record(*[child[k] for k in key])
                nics.append((child['name'], child['mac'], child['ip']))
                set_topo(topo, child['dn'], color='black')
                ceps = M[domain_name].Class('fvCEp').list(mac=child['mac'])
                for cep in ceps:
                    cep_path, _, _ = cep.rn()
                    set_topo(topo, cep_path, color='orange', path_color='orange')
                    topo.Edge(child['dn'], cep_path)
                    paths = cep.Class('fvRsCEpToPathEp').list()
                    for path in paths:
                        set_topo(topo, path['tDn'])
                        topo.Edge(child['dn'], path['tDn'])
        nav.Tab(V('Physical Interfaces'), table)
        
    elif host_data.class_name == 'compVm':
        os_name, os_img = get_host_os(V, host_data['os'], host_data['cfgdOs'])
        hv_name, hv_img = get_host_os(V, host_data['dn'])
        key = M[domain_name].Class('compVNic').keys()
        table = TABLE.FLIP(*['+' + k if k != 'name' else V('NIC Name') for k in key])
        for child in children:
            if child.class_name == 'compVNic':
                table.Record(*[child[k] for k in key])
                nics.append((child['name'], child['mac'], child['ip']))
                set_topo(topo, child['dn'], color='black')
                ceps = M[domain_name].Class('fvCEp').list(mac=child['mac'])
                for cep in ceps:
                    cep_path, _, _ = cep.rn()
                    set_topo(topo, cep_path, color='orange', path_color='orange')
                    topo.Edge(child['dn'], cep_path)
                    paths = cep.Class('fvRsCEpToPathEp').list()
                    for path in paths:
                        set_topo(topo, path['tDn'])
                        topo.Edge(child['dn'], path['tDn'])
        nav.Tab(V('Virtual Interfaces'), table)
        
    elif host_data.class_name == 'compHv':
        os_name, os_img = get_host_os(V, host_data['dn'])
        h_key = M[domain_name].Class('compHpNic').keys()
        h_table = TABLE.FLIP(*['+' + k if k != 'name' else V('NIC Name') for k in h_key])
        m_key = M[domain_name].Class('compMgmtNic').keys()
        m_table = TABLE.FLIP(*['+' + k if k != 'name' else V('NIC Name') for k in m_key])
        for child in children:
            if child.class_name == 'compHpNic':
                h_table.Record(*[child[k] for k in h_key])
                nics.append((child['name'], child['mac'], child['ip']))
                set_topo(topo, child['dn'], color='black')
                ceps = M[domain_name].Class('fvCEp').list(mac=child['mac'])
                for cep in ceps:
                    cep_path, _, _ = cep.rn()
                    set_topo(topo, cep_path, color='orange', path_color='orange')
                    topo.Edge(child['dn'], cep_path)
                    paths = cep.Class('fvRsCEpToPathEp').list()
                    for path in paths:
                        set_topo(topo, path['tDn'])
                        topo.Edge(child['dn'], path['tDn'])
            elif child.class_name == 'compMgmtNic':
                m_table.Record(*[child[k] for k in m_key])
                nics.append((child['name'], child['mac'], child['ip']))
                set_topo(topo, child['dn'], color='black')
                ceps = M[domain_name].Class('fvCEp').list(mac=child['mac'])
                for cep in ceps:
                    cep_path, _, _ = cep.rn()
                    set_topo(topo, cep_path, color='orange', path_color='orange')
                    topo.Edge(child['dn'], cep_path)
                    paths = cep.Class('fvRsCEpToPathEp').list()
                    for path in paths:
                        set_topo(topo, path['tDn'])
                        topo.Edge(child['dn'], path['tDn'])
        nav.Tab(V('Hypervisor Interfaces'), h_table)
        nav.Tab(V('Management Interfaces'), m_table)
    
    else:
        os_name = V('Unknown')
        os_img = '/resources/images/vendor/color/question.png'
    
    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(HEAD(1).html(name))
    if desc: V.Page.html(HEAD(3).html(V('Description'))).html(HEAD(4).html(desc))
    if host_data.class_name == 'compVm':
        V.Page.html(
            ROW().html(
                COL(4, 'sm', STYLE='text-align:center;').html(HEAD(3).html(V('OS'))).html(HEAD(4).html(os_name)).html(IMG(os_img, width='100px')),
                COL(4, 'sm', STYLE='text-align:center;').html(HEAD(3).html(V('Hypervisor'))).html(HEAD(4).html(hv_name)).html(IMG(hv_img, width='100px')),
                COL(4, 'sm', STYLE='text-align:center;').html(HEAD(3).html(V('Power State'))).html(HEAD(4).html(pw_stat)).html(IMG(pw_img, width='100px'))
            )
        )
    else:
        V.Page.html(
            ROW().html(
                COL(6, 'sm', STYLE='text-align:center;').html(HEAD(3).html(V('OS'))).html(HEAD(4).html(os_name)).html(IMG(os_img, width='128px')),
                COL(6, 'sm', STYLE='text-align:center;').html(HEAD(3).html(V('Power State'))).html(HEAD(4).html(pw_stat)).html(IMG(pw_img, width='128px'))
            )
        )
    if nics:
        nics = sorted(nics, key=lambda nic: nic[0])
        nic_table = TABLE(STYLE='margin:auto;')
        for nic in nics:
            nic_table.html(
                TR().html(
                    TD(STYLE='padding:0px 5px 0px 5px;').html(IMG('/resources/images/tool/nic.png', width='36px')),
                    TD(STYLE='padding:0px 5px 0px 5px;').html(HEAD(4).html(nic[0])),
                    TD(STYLE='padding:0px 5px 0px 5px;').html(HEAD(4).html(nic[1])),
                    TD(STYLE='padding:0px 5px 0px 5px;').html(HEAD(4).html(nic[2]))
                )
            )
        V.Page.html(
            ROW().html(
                COL(12, STYLE='text-align:center;').html(
                    HEAD(3).html(V('Network Interfaces')),
                    nic_table
                )
            )
        )
    V.Page.html(nav)
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))
