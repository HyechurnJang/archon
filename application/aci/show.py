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

def host_all(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    host_data = M.Class('compHost').list(detail=True, sort=['type', 'dn'])
    nic_data = M.Class('compNic').list(detail=True)

    #===========================================================================
    # Logic
    #===========================================================================
    for domain_name in M:
        cnt_phy = 0
        cnt_hv = 0
        cnt_vm = 0
        
        ph_table = DataTable(V('OID'), V('Name'), V('IP'), V('MAC'), V('OS'), V('State'))
        vm_table = DataTable(V('OID'), V('Name'), V('IP'), V('MAC'), V('OS'), V('State'))
        hv_table = FooTable(V('OID'), V('Name'), V('State'), V('+Interfaces'))
        
        for host in host_data[domain_name]:
            if host.class_name in ['compPhys', 'compVm']:
                dn = host['dn']
                oid = Get('/aci/show/host/%s/%s' % (domain_name, dn)).html(host['oid'])
                ip_data = ' '
                mac_data = ' '
                dn2nic = dn + '/'
                for nic in nic_data[domain_name]:
                    if dn2nic in nic['dn']:
                        ip_data += '<p><small>' + nic['ip'] + '&nbsp;&nbsp;</small></p>'
                        mac_data += '<p><small>' + nic['mac'] + '&nbsp;&nbsp;</small></p>'
                if host.class_name == 'compPhys':
                    cnt_phy += 1
                    ph_table.Record(oid, host['name'], ip_data, mac_data, host['os'], host['state'])
                elif host.class_name == 'compVm':
                    cnt_vm += 1
                    vm_table.Record(oid, host['name'], ip_data, mac_data, host['os'], host['state'])
            elif host.class_name == 'compHv':
                cnt_hv += 1
                dn = host['dn']
                oid = Get('/aci/show/host/%s/%s' % (domain_name, dn)).html(host['oid'])
                ipmac = ' '
                dn2nic = dn + '/'
                for nic in nic_data[domain_name]:
                    if dn2nic in nic['dn']:
                        if nic.class_name == 'compHpNic':
                            ipmac += '<p>Hypervisor NIC&nbsp;:&nbsp;' + nic['mac'] + '&nbsp;:&nbsp;' + nic['ip'] + '</p>'
                        elif nic.class_name == 'compMgmtNic':
                            ipmac += '<p>Management NIC&nbsp;:&nbsp;' + nic['mac'] + '&nbsp;:&nbsp;' + nic['ip'] + '</p>'
                hv_table.Record(oid, host['name'], host['state'], ipmac)
    
    #===========================================================================
    # View
    #===========================================================================
        V.Page.html(HEAD(1).html('%s %s' % (domain_name, V('Domain'))))
        V.Page.html(
            ROW().html(
                COL(4).html(CountPanel(V('Physical'), 'server', cnt_phy, **{'class' : 'panel-default'})),
                COL(4).html(CountPanel(V('Virtual'), 'cube', cnt_vm, **{'class' : 'panel-default'})),
                COL(4).html(CountPanel(V('Hypervisor'), 'cubes', cnt_hv, **{'class' : 'panel-default'}))
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
                HEAD(3).html(V('Hypervisor Hosts')),
                hv_table
            )
    
    if not V.Page: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
        
def host_one(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    host_data = M[domain_name](dn, detail=True)

    #===========================================================================
    # Logic
    #===========================================================================
    nav = Navigation()
    
    kv = KeyVal()
    for key in host_data.attrs(): kv.Data(key, host_data[key])
    nav.Tab(V('Details'), kv)
    
    children = host_data.children(detail=True)
    if host_data.class_name == 'compPhys':
        key = M[domain_name].Class('compPpNic').attrs()
        table = FooTable(*['+' + k if k != 'name' else V('NIC Name') for k in key])
        for child in children:
            if child.class_name == 'compPpNic':
                table.Record(*[child[k] for k in key])
        nav.Tab(V('Physical Interfaces'), table)
    elif host_data.class_name == 'compVm':
        key = M[domain_name].Class('compVNic').attrs()
        table = FooTable(*['+' + k if k != 'name' else V('NIC Name') for k in key])
        for child in children:
            if child.class_name == 'compVNic':
                table.Record(*[child[k] for k in key])
        nav.Tab(V('Virtual Interfaces'), table)
    elif host_data.class_name == 'compHv':
        h_key = M[domain_name].Class('compHpNic').attrs()
        h_table = FooTable(*['+' + k if k != 'name' else V('NIC Name') for k in h_key])
        m_key = M[domain_name].Class('compMgmtNic').attrs()
        m_table = FooTable(*['+' + k if k != 'name' else V('NIC Name') for k in m_key])
        for child in children:
            if child.class_name == 'compHpNic': h_table.Record(*[child[k] for k in h_key])
            elif child.class_name == 'compMgmtNic': m_table.Record(*[child[k] for k in m_key])
        nav.Tab(V('Hypervisor Interfaces'), h_table)
        nav.Tab(V('Management Interfaces'), m_table)
    
    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(
        HEAD(1).html(host_data['oid']),
        nav
    )
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))

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
        table = DataTable(V('ID'), V('Type'), V('Device Name'), V('Model'), V('Serial'), V('Version'), V('Management IP'), V('State'), V('Fabric State'), V('Uptime'))
        
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
                        CountPanel(V('Controller'), 'map-signs', cnt_ctrl, **(ATTR.click('/aci/show/device/controller') + {'class' : 'panel-default'}))
                    ),
                    COL(4).html(
                        CountPanel(V('Spine'), 'tree', cnt_spne, **(ATTR.click('/aci/show/device/spine') + {'class' : 'panel-default'}))
                    ),
                    COL(4).html(
                        CountPanel(V('Leaf'), 'leaf', cnt_leaf, **(ATTR.click('/aci/show/device/leaf') + {'class' : 'panel-default'}))
                    )
                )
            )
        V.Page.html(table)
     
    if not V.Page: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))
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
    kv = KeyVal()
    for key in node_data.attrs(): kv.Data(key, node_data[key])
    nav.Tab(V('Details'), kv)
    if hasattr(node_data, 'System'):
        if node_data['role'] != 'controller':
            data = M.getHealth()
            try: health = Line(*data['_tstamp'], **(Chart.SCALE100 + Chart.NOLEGEND + Chart.RATIO_8)).Data(dn, *data[domain_name + '/' + dn])
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
    V.Page.html(nav)
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    
def tenant_all(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    tns = M.Tenant.list(sort='name')
    epgs = M.EPG.list(sort='name')
    bds = M.BridgeDomain.list(sort='name')
    ctxs = M.Context.list(sort='name')
    ctrs = M.Contract.list(sort='name')
    flts = M.Filter.list(sort='name')
    
    #===========================================================================
    # Logic
    #===========================================================================
    table = DataTable(V('Domain'), V('Tenant Name'), V('EPG'), V('Bridge Domain'), V('Context'), V('Contract'), V('Filter'))
    tn_cnt = 0
    for domain_name in M:
        for tn in tns[domain_name]:
            tn_cnt += 1
            name = Get('/aci/show/tenant/%s/%s' % (domain_name, tn['dn'])).html(tn['name'])
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
            table.Record(domain_name, name, epg_data, bd_data, ctx_data, ctr_data, flt_data)
    
    #===========================================================================
    # View
    #===========================================================================
    if not table: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))
    else: V.Page.html(CountPanel(V('Tenants'), 'users', tn_cnt, **{'class' : 'panel-default'})).html(table)
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))

def tenant_one(R, M, V):
    #===========================================================================
    # GetData
    #===========================================================================
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    tenant = M[domain_name](dn, detail=True)
    
    #===========================================================================
    # Logic
    #===========================================================================
    nav = Navigation()
    
    # Health
    hdata = M.getHealth()
    health = None
    try: health = Line(*hdata['_tstamp'], **(Chart.SCALE100 + Chart.NOLEGEND + Chart.RATIO_8)).Data(dn, *hdata[domain_name + '/' + dn])
    except: pass
    
    # Details
    kv = KeyVal()
    for key in tenant.attrs(): kv.Data(key, tenant[key])
    nav.Tab(V('Details'), kv)    

    # App Profile
    datas = tenant.AppProfile.list(detail=True, sort='name')
    if datas:
        key = tenant.AppProfile.attrs()
        col = ['+' + k if k != 'name' else V('Application Profile Name') for k in key]
        col.append('+EPG')
        table = FooTable(*col)
        nav.Tab(V('Application Profile Details'), table)
        for data in datas:
            val = [data[k] for k in key]
            sub_val = DIV()
            sub_datas = data.EPG.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas: sub_val.html(PARA().html(Get('/aci/show/epgroup/%s/%s' % (domain_name, sub_data['dn'])).html(sub_data['name'])))
            val.append(sub_val)
            table.Record(*val)
    
    # Bridge Domain
    datas = tenant.BridgeDomain.list(detail=True, sort='name')
    if datas:
        key = tenant.BridgeDomain.attrs()
        col = ['+' + k if k != 'name' else V('Bridge Domain Name') for k in key]
        col.append('+Subnet')
        table = FooTable(*col)
        nav.Tab(V('Bridge Domain Details'), table)
        for data in datas:
            val = [data[k] for k in key]
            sub_val = ' '
            sub_datas = data.Subnet.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas: sub_val += '<p>' + sub_data['ip'] + '</p>'
            val.append(sub_val)
            table.Record(*val)
    
    # Context
    datas = tenant.Context.list(detail=True, sort='name')
    if datas:
        key = tenant.Context.attrs()
        table = FooTable(*['+' + k if k != 'name' else V('Context Name') for k in key])
        nav.Tab(V('Context Details'), table)
        for data in datas: table.Record(*[data[k] for k in key])

    # L3 External
    datas = tenant.L3External.list(detail=True, sort='name')
    if datas:
        key = tenant.L3External.attrs()
        table = FooTable(*['+' + k if k != 'name' else V('Context Name') for k in key])
        nav.Tab(V('L3 External Details'), table)
        for data in datas: table.Record(*[data[k] for k in key])

    # Contract
    datas = tenant.Contract.list(detail=True, sort='name')
    if datas:
        key = tenant.Contract.attrs()
        col = ['+' + k if k != 'name' else V('Contract Name') for k in key]
        col.append('+Subject')
        table = FooTable(*col)
        nav.Tab(V('Contract Details'), table)
        for data in datas:
            val = [data[k] for k in key]
            sub_val = ' '
            sub_datas = data.Subject.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas: sub_val += '<p>' + sub_data['name'] + '</p>'
            val.append(sub_val)
            table.Record(*val)
    
    # Filter
    datas = tenant.Filter.list(detail=True, sort='name')
    if datas:
        key = tenant.Filter.attrs()
        col = ['+' + k if k != 'name' else V('Filter Name') for k in key]
        col.append('+Filter Entry')
        table = FooTable(*col)
        nav.Tab(V('Filter Details'), table)
        for data in datas:
            val = [data[k] for k in key]
            sub_val = ' '
            sub_datas = data.FilterEntry.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas: sub_val += '<p>' + sub_data['name'] + '</p>' 
            val.append(sub_val)
            table.Record(*val)

    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(HEAD(1).html(tenant['name']))
    if health != None: V.Page.html(ROW().html(health))
    V.Page.html(nav)
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))

def epg_all(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    epgs = M.EPG.list(detail=True, sort='dn')
    
    #===========================================================================
    # Logic
    #===========================================================================
    table = DataTable(V('Domain'), V('EPG Name'), V('Bridge Domain'), V('Provided Contracts'), V('Consumed Contracts'), V('Binding Path'))
    epg_cnt = 0
    for domain_name in M:
        for epg in epgs[domain_name]:
            epg_cnt += 1
            raw = re.sub('(uni/|tn-|ap-|epg-)', '', epg['dn']).split('/')
            path_raw = '/'.join(raw[:2])
            name_raw = raw[2]
            name = PARA().html(SMALL().html(path_raw + '/')).html(Get('/aci/show/epgroup/%s/%s' % (domain_name, epg['dn'])).html(name_raw))
            bd_data = ' '
            prov_data = ' '
            cons_data = ' '
            path_data = ' '
            children = epg.children(detail=True)
            for child in children:
                if child.class_name == 'fvRsBd':
                    bd_data += '<p><small>' + child['tDn'].split('/BD-')[1] + '&nbsp;&nbsp;</small></p>'
                elif child.class_name == 'fvRsProv':
                    prov_data += '<p><small>' + child['tDn'].split('/brc-')[1] + '&nbsp;&nbsp;</small></p>'
                elif child.class_name == 'fvRsCons':
                    cons_data += '<p><small>' + child['tDn'].split('/brc-')[1] + '&nbsp;&nbsp;</small></p>'
                elif child.class_name == 'fvRsPathAtt':
                    path_data += '<p><small>' + re.sub('(topology/|pod-|protpaths-|paths-|pathep-|\[|\])', '', child['tDn']) + '&nbsp;(%s)&nbsp;</small></p>' % child['encap']
            table.Record(domain_name, name, bd_data, prov_data, cons_data, path_data)
    
    #===========================================================================
    # View
    #===========================================================================
    if not table: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))
    else: V.Page.html(CountPanel(V('EPG'), 'object-group', epg_cnt, **{'class' : 'panel-default'})).html(table)
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))

def epg_one(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    epg = M[domain_name](dn, detail=True)
    
    #===========================================================================
    # Logic
    #===========================================================================
    nav = Navigation()
    
    # Health
    hdata = M.getHealth()
    health = None
    try: health = Line(*hdata['_tstamp'], **(Chart.SCALE100 + Chart.NOLEGEND + Chart.RATIO_8)).Data(dn, *hdata[domain_name + '/' + dn])
    except: pass
    
    # Details
    kv = KeyVal()
    for key in epg.attrs(): kv.Data(key, epg[key])
    nav.Tab(V('Details'), kv)
    
    # BD Relation
    act = epg.Class('fvRsBd')
    datas = act.list(detail=True)
    if datas:
        data = datas[0]
        kv = KeyVal()
        for key in data.attrs(): kv.Data(key, data[key])
        nav.Tab(V('Bridge Domain Relations'), kv)
        
    # Path Attach
    act = epg.Class('fvRsPathAtt')
    datas = act.list(detail=True)
    if datas:
        key = act.attrs()
        key.remove('encap')
        key.append('encap')
        col = []
        for k in key:
            if k == 'tDn' : col.append(V('Path Name'))
            elif k == 'encap' : col.append(V('Encap'))
            else: col.append('+' + k)
        table = FooTable(*col)
        nav.Tab(V('Path Attachments'), table)
        for data in datas:
            val = []
            for k in key:
                if k == 'tDn': val.append(re.sub('(topology/|pod-|protpaths-|paths-|pathep-|\[|\])', '', data['tDn']))
                else: val.append(data[k])
            table.Record(*val)
        
    # Provider
    act = epg.Class('fvRsProv')
    datas = act.list(detail=True)
    if datas:
        key = act.attrs()
        table = FooTable(*['+' + k if k != 'tnVzBrCPName' else V('Contract Name') for k in key])
        nav.Tab(V('Provided Contracts'), table)
        for data in datas: table.Record(*[data[k] for k in key])
    
    # Consumer
    act = epg.Class('fvRsCons')
    datas = act.list(detail=True)
    if datas:
        key = act.attrs()
        table = FooTable(*['+' + k if k != 'tnVzBrCPName' else V('Contract Name') for k in key])
        nav.Tab(V('Consumed Contracts'), table)
        for data in datas: table.Record(*[data[k] for k in key])

    # Endpoint
    datas = epg.Endpoint.list(detail=True)
    if datas:
        key = epg.Endpoint.attrs()
        col = []
        for k in key:
            if k == 'name': col.append(V('MAC'))
            elif k == 'ip' : col.append(V('IP'))
            elif k == 'encap' : col.append(V('Encap'))
            else: col.append('+' + k)
        table = FooTable(*col)
        nav.Tab(V('Endpoint'), table)
        for data in datas:
            val = []
            for k in key:
                if k == 'name': val.append(Get('/aci/show/endpoint/%s/%s' % (domain_name, data['dn'])).html(data[k]))
                else: val.append(data[k])
            table.Record(*val)

    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(HEAD(1).html(epg['name']))
    if health != None: V.Page.html(ROW().html(health))
    V.Page.html(nav)
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))

def ep_all(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    eps = M.Endpoint.list(detail=True, sort='dn')
    
    #===========================================================================
    # Logic
    #===========================================================================
    table = DataTable(V('Domain'), V('MAC'), V('EPG'), V('Interface'), V('Encap'), V('IP'), V('Nic Type'))
    ep_cnt = 0
    dcv_cnt = 0
    mng_cnt = 0
    phy_cnt = 0
    hyp_cnt = 0
    vir_cnt = 0
    
    for domain_name in M:
        
        paths = M[domain_name].Class('fvRsCEpToPathEp').list()
        nics = M[domain_name].Class('compNic').list(detail=True)
        
        for ep in eps[domain_name]:
            ep_cnt += 1
            dn = ep['dn']
            mac = ep['mac']
            if 'epg-' in dn:
                epg_name = '<small>%s</small>' % re.sub('(uni/|tn-|ap-|epg-|/cep-[a-zA-Z0-9:]+)', '', dn)
                nic_type = ' '
                for nic in nics:
                    if mac == nic['mac']:
                        if nic.class_name == 'compDNic':
                            dcv_cnt += 1
                            nic_type += '<p><small>Discovered</small></p>'
                        elif nic.class_name == 'compMgmtNic':
                            mng_cnt += 1
                            nic_type += '<p><small>Management : ' + re.sub('(comp/|prov-|ctrlr-|hv-|mgmtnic-|\[|\])', '', nic['dn']) + '</small></p>'
                        elif nic.class_name == 'compHpNic':
                            hyp_cnt += 1
                            nic_type += '<p><small>Hypervisor : ' + re.sub('(comp/|prov-|ctrlr-|hv-|hpnic-|\[|\])', '', nic['dn']) + '</small></p>'
                        elif nic.class_name == 'compPpNic':
                            phy_cnt += 1
                            nic_type += '<p><small>Physical</small></p>'
                        elif nic.class_name == 'compVNic':
                            vir_cnt += 1
                            nic_type += '<p><small>Virtual : ' + re.sub('(comp/|prov-|ctrlr-|vm-|/vnic-[a-zA-Z0-9:]+|\[|\])', '', nic['dn']) + '</small></p>'
            else:
                epg_name = ' '
                nic_type = 'Logical Device'
            ip = ep['ip']
            encap = ep['encap']
            
            intf = ' '
            for path in paths:
                if dn in path['dn']:
                    intf = path['dn'].split(dn + '/rscEpToPathEp-')[1]
                    intf = re.sub('(topology/|pod-|protpaths-|paths-|pathep-|\[|\])', '', intf)
            
            table.Record(domain_name,
                         Get('/aci/show/endpoint/%s/%s' % (domain_name, dn)).html(mac),
                         epg_name, intf, encap, ip, nic_type)
    
    #===========================================================================
    # View
    #===========================================================================
    if not table: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))
    else:
        V.Page.html(
            ROW().html(
                COL(2).html(CountPanel(V('Endpoints'), 'plug', ep_cnt, **{'class' : 'panel-default'})),
                COL(2).html(CountPanel(V('Discovered'), 'flag-checkered', dcv_cnt, **{'class' : 'panel-default'})),
                COL(2).html(CountPanel(V('Management'), 'cog', mng_cnt, **{'class' : 'panel-default'})),
                COL(2).html(CountPanel(V('Physical'), 'server', phy_cnt, **{'class' : 'panel-default'})),
                COL(2).html(CountPanel(V('Hypervisor'), 'cubes', hyp_cnt, **{'class' : 'panel-default'})),
                COL(2).html(CountPanel(V('Virtual'), 'cube', vir_cnt, **{'class' : 'panel-default'}))
            )
        ).html(table)
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))

def ep_one(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    ep = M[domain_name](dn, detail=True)
    
    #===========================================================================
    # Logic    
    #===========================================================================
    nav = Navigation()
    
    # Details
    kv = KeyVal()
    for key in ep.attrs(): kv.Data(key, ep[key])
    nav.Tab(V('Details'), kv)
    
    # EPG
    epg = ep.parent(detail=True)
    if epg and epg.class_name == 'fvAEPg':
        kv = KeyVal()
        for key in epg.attrs(): kv.Data(key, epg[key])
        nav.Tab(V('Endpoint Group'), kv)
        
    # Path
    children = ep.children(detail=True)
    for child in children:
        if child.class_name == 'fvRsCEpToPathEp':
            kv = KeyVal()
            for key in child.attrs(): kv.Data(key, child[key])
            nav.Tab(V('Path Relation'), kv)
            break
    
    # Interface & Host
    hosts = []
    nics = M[domain_name].Class('compNic').list(mac=ep['mac'], detail=True)
    if nics:
        nicdiv = DIV()
        hstdiv = DIV()
        nav.Tab(V('Network Interface'), nicdiv)
        nav.Tab(V('Host Detail'), hstdiv)
        
        phy_nic = None
        vm_nic = None
        hv_nic = None
        mg_nic = None
        
        phy_host = None
        vm_host = None
        hv_host = None
        
        for nic in nics:
            key = nic.attrs()
            host = nic.parent(detail=True)
            if nic.class_name == 'compPpNic':
                if phy_nic == None: phy_nic = FooTable(*['+' + k if k != 'name' else V('Physical NIC') for k in key])
                phy_nic.Record(*[nic[k] for k in key])
                if host and host['dn'] not in hosts:
                    hosts.append(host['dn'])
                    key = host.attrs()
                    if phy_host == None: phy_host = FooTable(*['+' + k if k != 'name' else V('Physical Hosts') for k in key])
                    phy_host.Record(*[host[k] for k in key])
            elif nic.class_name == 'compVNic':
                if vm_nic == None: vm_nic = FooTable(*['+' + k if k != 'name' else V('Virtual NIC') for k in key])
                vm_nic.Record(*[nic[k] for k in key])
                if host and host['dn'] not in hosts:
                    hosts.append(host['dn'])
                    key = host.attrs()
                    if vm_host == None: vm_host = FooTable(*['+' + k if k != 'name' else V('Virtual Hosts') for k in key])
                    vm_host.Record(*[host[k] for k in key])
            elif nic.class_name == 'compHpNic':
                if hv_nic == None: hv_nic = FooTable(*['+' + k if k != 'name' else V('Hypervisor NIC') for k in key])
                hv_nic.Record(*[nic[k] for k in key])
                if host and host['dn'] not in hosts:
                    hosts.append(host['dn'])
                    key = host.attrs()
                    if hv_host == None: hv_host = FooTable(*['+' + k if k != 'name' else V('Hypervisor Hosts') for k in key])
                    hv_host.Record(*[host[k] for k in key])
            elif nic.class_name == 'compMgmtNic':
                if mg_nic == None: mg_nic = FooTable(*['+' + k if k != 'name' else V('Management NIC') for k in key])
                mg_nic.Record(*[nic[k] for k in key])
                if host and host['dn'] not in hosts:
                    hosts.append(host['dn'])
                    key = host.attrs()
                    if hv_host == None: hv_host = FooTable(*['+' + k if k != 'name' else V('Hypervisor Hosts') for k in key])
                    hv_host.Record(*[host[k] for k in key])
        
    #===========================================================================
    # View
    #===========================================================================
        if phy_nic != None: nicdiv.html(phy_nic)
        if vm_nic != None: nicdiv.html(vm_nic)
        if hv_nic != None: nicdiv.html(hv_nic)
        if mg_nic != None: nicdiv.html(mg_nic)
        if phy_host != None: hstdiv.html(phy_host)
        if vm_host != None: hstdiv.html(vm_host)
        if hv_host != None: hstdiv.html(hv_host)
    
    V.Page.html(HEAD(1).html(ep['name']))
    V.Page.html(nav)
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    