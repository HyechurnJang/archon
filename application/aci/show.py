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

'''
Created on 2016. 12. 14.

@author: Hye-Churn Jang
'''

from archon import *

def device_all(R, M, V):
    
    if len(R.Path) > 3: node_data = M.Node.list(role=R.Path[3], detail=True)
    else: node_data = M.Node.list(detail=True)
    cfrm_data = M.Class('firmwareCtrlrRunning').list(detail=True)
    sfrm_data = M.Class('firmwareRunning').list(detail=True)
    tsys_data = M.System.list(detail=True)
     
    for domain_name in M:
        table = DataTable(V('ID'), V('Type'), V('Name'), V('Model'), V('Serial'), V('Version'), V('INB Mgmt IP'), V('OOB Mgmt IP'), V('State'), V('Uptime'))
         
        cnt_ctrl = 0
        cnt_spne = 0
        cnt_leaf = 0
         
        for node in node_data[domain_name]:
            for tsys in tsys_data[domain_name]:
                if node['dn'] + '/' in tsys['dn']:
                    id = tsys['id']
                    inb = tsys['inbMgmtAddr']
                    oob = tsys['oobMgmtAddr']
                    state = tsys['state']
                    uptime = tsys['systemUpTime']
                    break
            if node['role'] == 'controller':
                cnt_ctrl += 1
                for firm in cfrm_data[domain_name]:
                    if node['dn'] + '/' in firm['dn']:
                        table.record(id,
                                     'Controller',
                                     STRONG().html(node['name']),
                                     node['model'],
                                     node['serial'],
                                     firm['version'],
                                     inb,
                                     oob,
                                     state,
                                     uptime[:-5],
                                     onclick=GetOnClick('/aci/show/device/%s/%s' % (domain_name, node['dn'])))
                        break
            elif node['role'] == 'spine':
                cnt_spne += 1
                for firm in sfrm_data[domain_name]:
                    if node['dn'] + '/' in firm['dn']:
                        table.record(id,
                                     'Spine',
                                     STRONG().html(node['name']),
                                     node['model'],
                                     node['serial'],
                                     firm['version'],
                                     inb,
                                     oob,
                                     state,
                                     uptime[:-4],
                                     onclick=GetOnClick('/aci/show/device/%s/%s' % (domain_name, node['dn'])))
                        break
            elif node['role'] == 'leaf':
                cnt_leaf += 1
                for firm in sfrm_data[domain_name]:
                    if node['dn'] + '/' in firm['dn']:
                        table.record(id,
                                     'Leaf',
                                     STRONG().html(node['name']),
                                     node['model'],
                                     node['serial'],
                                     firm['version'],
                                     inb,
                                     oob,
                                     state,
                                     uptime[:-4],
                                     onclick=GetOnClick('/aci/show/device/%s/%s' % (domain_name, node['dn'])))
                        break
        V.Page.html(HEAD(1).html('%s %s' % (domain_name, V('Domain'))))
        if len(R.Path) < 4:
            V.Page.html(
                ROW().html(
                    COL(4).html(CountPanel(V('Controller'), 'map-signs', cnt_ctrl, onclick=GetOnClick('/aci/show/device/controller'), **{'class' : 'panel-primary'}))
                ).html(
                    COL(4).html(CountPanel(V('Spine'), 'tree', cnt_spne, onclick=GetOnClick('/aci/show/device/spine'), **{'class' : 'panel-primary'}))
                ).html(
                    COL(4).html(CountPanel(V('Leaf'), 'leaf', cnt_leaf, onclick=GetOnClick('/aci/show/device/leaf'), **{'class' : 'panel-primary'}))
                )
            )
        V.Page.html(table)
     
    if not V.Page: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))

def device_one(R, M, V):
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    
    node_data = M[domain_name](dn, detail=True)
    
    V.Page.html(HEAD(1).html(node_data['name']))
    
    lo_detail = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
    for key in node_data: lo_detail.html(KeyVal(key, node_data[key]))
    
    if hasattr(node_data, 'System'):
        lo_system = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
        for key in node_data.System: lo_system.html(KeyVal(key, node_data.System[key]))
        V.Page.html(COL(6).html(HEAD(3).html(V('Details'))).html(lo_detail))
        V.Page.html(COL(6).html(HEAD(3).html(V('System'))).html(lo_system))
        
        physif = node_data.System.PhysIf.list(detail=True)
        if physif:
            key = physif[0].keys()
            col = []
            for k in key: col.append('+' + k if k != 'id' else V('ID'))
            
            physif_table = FooTable(*col)
            lo_physif = DIV(**{'style' : 'padding:0px 0px 0px 40px;'}).html(physif_table)
            V.Page.html(COL(12).html(HEAD(3).html(V('Physical Interface'))).html(lo_physif))
            
            for pi in physif:
                val = []
                for k in key: val.append(pi[k])
                physif_table.record(*val)
    else:
        V.Page.html(COL(12).html(HEAD(3).html(V('Details'))).html(lo_detail))
    
def tenant_all(R, M, V):
    tns = M.Tenant.list()
    epgs = M.EPG.list()
    bds = M.BridgeDomain.list()
    ctxs = M.Context.list()
    ctrs = M.Contract.list()
    flts = M.Filter.list()
    
    table = DataTable(V('Domain'), V('Name'), V('EPG'), V('Bridge Domain'), V('Context'), V('Contract'), V('Filter'))
    
    tn_cnt = 0
    
    for domain_name in M:
        
        for tn in tns[domain_name]:
            tn_cnt += 1
            name = tn['name']
            
            epg_data = ' '
            bd_data = ' '
            ctx_data = ' '
            ctr_data = ' '
            flt_data = ' '
            
            for epg in epgs[domain_name]:
                if tn['dn'] in epg['dn']: epg_data += '<p><small>' + re.sub('(ap-|epg-)', '', '/'.join(epg['dn'].split('/')[2:])) + '&nbsp;&nbsp;</small></p>'
            for bd in bds[domain_name]:
                if tn['dn'] in bd['dn']: bd_data += '<p><small>' + bd['name'] + '&nbsp;&nbsp;</small></p>'
            for ctx in ctxs[domain_name]:
                if tn['dn'] in ctx['dn']: ctx_data += '<p><small>' + ctx['name'] + '&nbsp;&nbsp;</small></p>'
            for ctr in ctrs[domain_name]:
                if tn['dn'] in ctr['dn']: ctr_data += '<p><small>' + ctr['name'] + '&nbsp;&nbsp;</small></p>'
            for flt in flts[domain_name]:
                if tn['dn'] in flt['dn']: flt_data += '<p><small>' + flt['name'] + '&nbsp;&nbsp;</small></p>'
            
            table.record(domain_name, STRONG().html(name), epg_data, bd_data, ctx_data, ctr_data, flt_data,
                         onclick=GetOnClick('/aci/show/tenant/%s/%s' % (domain_name, tn['dn'])))
            
    if not table: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))
    else:
        V.Page.html(CountPanel(V('Tenants'), 'users', tn_cnt, **{'class' : 'panel-primary'})).html(table)

def tenant_one(R, M, V):
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    
    tenant = M[domain_name](dn, detail=True)
    
    V.Page.html(HEAD(1).html(tenant['name']))
    
    lo_detail = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
    V.Page.html(
        COL(12).html(
            HEAD(3).html(
                V('Details')
            )
        )
    ).html(
        COL(12).html(
            lo_detail
        )
    )
    for key in tenant: lo_detail.html(KeyVal(key, tenant[key]))

    approf = tenant.AppProfile.list(detail=True)
    if approf:
        akey = approf[0].keys()
        acol = []
        for k in akey: acol.append('+' + k if k != 'name' else V('Application Profile Name'))    
        lo_apepg = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
        V.Page.html(
            COL(12).html(
                HEAD(3).html(
                    V('Application Profile')
                )
            )
        ).html(
            COL(12).html(
                lo_apepg
            )
        )
        for ap in approf:
            val = []
            for k in akey: val.append(ap[k])
            lo_apepg.html(FooTable(*acol).record(*val))
            
            epgs = ap.EPG.list(detail=True)
            if epgs:
                ekey = epgs[0].keys()
                ecol = []
                for k in ekey: ecol.append('+' + k if k != 'name' else V('EPG Name'))
                 
                epg_table = FooTable(*ecol)
                lo_epg = DIV(**{'style' : 'padding:0px 0px 0px 40px;'}).html(epg_table)
                lo_apepg.html(lo_epg)
                 
                for epg in epgs:
                    val = []
                    for k in ekey: val.append(epg[k])
                    epg_table.record(*val)
