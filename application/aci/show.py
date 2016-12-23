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

def device_all(R, M, V):
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    
    if len(R.Path) > 3: node_data = M.Node.list(role=R.Path[3], detail=True, sort='id')
    else: node_data = M.Node.list(detail=True, sort='id')
    cfrm_data = M.Class('firmwareCtrlrRunning').list(detail=True)
    sfrm_data = M.Class('firmwareRunning').list(detail=True)
    tsys_data = M.System.list(detail=True)
     
    for domain_name in M:
        table = DataTable(V('ID'), V('Type'), V('Device Name'), V('Model'), V('Serial'), V('Version'), V('INB Mgmt IP'), V('OOB Mgmt IP'), V('State'), V('Uptime'))
         
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
                        table.Record(id,
                                     'Controller',
                                     STRONG().html(node['name']),
                                     node['model'],
                                     node['serial'],
                                     firm['version'],
                                     inb,
                                     oob,
                                     state,
                                     uptime[:-5],
                                     **ATTR.click('/aci/show/device/%s/%s' % (domain_name, node['dn'])))
                        break
            elif node['role'] == 'spine':
                cnt_spne += 1
                for firm in sfrm_data[domain_name]:
                    if node['dn'] + '/' in firm['dn']:
                        table.Record(id,
                                     'Spine',
                                     STRONG().html(node['name']),
                                     node['model'],
                                     node['serial'],
                                     firm['version'],
                                     inb,
                                     oob,
                                     state,
                                     uptime[:-4],
                                     **ATTR.click('/aci/show/device/%s/%s' % (domain_name, node['dn'])))
                        break
            elif node['role'] == 'leaf':
                cnt_leaf += 1
                for firm in sfrm_data[domain_name]:
                    if node['dn'] + '/' in firm['dn']:
                        table.Record(id,
                                     'Leaf',
                                     STRONG().html(node['name']),
                                     node['model'],
                                     node['serial'],
                                     firm['version'],
                                     inb,
                                     oob,
                                     state,
                                     uptime[:-4],
                                     **ATTR.click('/aci/show/device/%s/%s' % (domain_name, node['dn'])))
                        break
        V.Page.html(HEAD(1).html('%s %s' % (domain_name, V('Domain'))))
        if len(R.Path) < 4:
            V.Page.html(
                ROW().html(
                    COL(4).html(
                        CountPanel(V('Controller'), 'map-signs', cnt_ctrl, **(ATTR.click('/aci/show/device/controller') + {'class' : 'panel-default'}))
                    )
                ).html(
                    COL(4).html(
                        CountPanel(V('Spine'), 'tree', cnt_spne, **(ATTR.click('/aci/show/device/spine') + {'class' : 'panel-default'}))
                    )
                ).html(
                    COL(4).html(
                        CountPanel(V('Leaf'), 'leaf', cnt_leaf, **(ATTR.click('/aci/show/device/leaf') + {'class' : 'panel-default'}))
                    )
                )
            )
        V.Page.html(table)
     
    if not V.Page: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))

def device_one(R, M, V):
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    
    node_data = M[domain_name](dn, detail=True)
    
    V.Page.html(HEAD(1).html(node_data['name']))
    
    if hasattr(node_data, 'System'):
        #=======================================================================
        # Health
        #=======================================================================
        hdata = M.getHealth()
        try:
            chart = Line(*hdata['_tstamp'], **(Chart.SCALE100 + Chart.NOLEGEND + Chart.RATIO_8)).Data(dn, *hdata[domain_name + '/' + dn])
            V.Page.html(ROW().html(chart))
        except: pass
        
        #=======================================================================
        # Details Tab
        #=======================================================================
        nav = Navigation()
        V.Page.html(ROW().html(COL(12).html(nav)))
        
        kv = KeyVal()
        for key in node_data.attrs(): kv.Data(key, node_data[key])
        nav.Tab(V('Details'), kv)
        
        kv = KeyVal()
        for key in node_data.System.attrs(): kv.Data(key, node_data.System[key])
        nav.Tab(V('System'), kv)
        
        physif = node_data.System.PhysIf.list(detail=True, sort='id')
        if physif:
            physif_keys = node_data.System.PhysIf.attrs()
            col = []
            for k in physif_keys: col.append('+' + k if k != 'id' else V('ID'))
            physif_table = FooTable(*col)
            for pi in physif:
                val = []
                for k in physif_keys: val.append(pi[k])
                physif_table.Record(*val)
            nav.Tab(V('Physical Interface'), physif_table)
    else:
        nav = Navigation()
        V.Page.html(ROW().html(COL(12).html(nav)))
        
        kv = KeyVal()
        for key in node_data.attrs(): kv.Data(key, node_data[key])
        nav.Tab(V('Details'), kv)
    
def tenant_all(R, M, V):
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    
    tns = M.Tenant.list(sort='name')
    epgs = M.EPG.list(sort='name')
    bds = M.BridgeDomain.list(sort='name')
    ctxs = M.Context.list(sort='name')
    ctrs = M.Contract.list(sort='name')
    flts = M.Filter.list(sort='name')
    
    table = DataTable(V('Domain'), V('Tenant Name'), V('EPG'), V('Bridge Domain'), V('Context'), V('Contract'), V('Filter'))
    
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
            
            table.Record(domain_name, STRONG().html(name), epg_data, bd_data, ctx_data, ctr_data, flt_data,
                         **ATTR.click('/aci/show/tenant/%s/%s' % (domain_name, tn['dn'])))
            
    if not table: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))
    else:
        V.Page.html(CountPanel(V('Tenants'), 'users', tn_cnt, **{'class' : 'panel-default'})).html(table)

def tenant_one(R, M, V):
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    
    tenant = M[domain_name](dn, detail=True)
    
    V.Page.html(HEAD(1).html(tenant['name']))
    
    hdata = M.getHealth()
    try:
        chart = Line(*hdata['_tstamp'], **(Chart.SCALE100 + Chart.NOLEGEND + Chart.RATIO_8)).Data(dn, *hdata[domain_name + '/' + dn])
        V.Page.html(ROW().html(chart))
    except: pass
    
    nav = Navigation()
    V.Page.html(ROW().html(COL(12).html(nav)))
    
    #===========================================================================
    # Details
    #===========================================================================
    kv = KeyVal()
    for key in tenant.attrs(): kv.Data(key, tenant[key])
    nav.Tab(V('Details'), kv)    

    #===========================================================================
    # App Profile
    #===========================================================================
    datas = tenant.AppProfile.list(detail=True, sort='name')
    if datas:
        key = tenant.AppProfile.attrs()
        col = []
        for k in key: col.append('+' + k if k != 'name' else V('Application Profile Name'))
        col.append('+EPG')
        table = FooTable(*col)
        nav.Tab(V('Application Profile Details'), table)
        for data in datas:
            val = []
            for k in key: val.append(data[k])
            sub_val = DIV()
            sub_datas = data.EPG.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas:
                    sub_val.html(PARA().html(Get('/aci/show/epg/%s/%s' % (domain_name, sub_data['dn'])).html(sub_data['name'])))
            val.append(sub_val)
            table.Record(*val)
    
    #===========================================================================
    # Bridge Domain
    #===========================================================================
    datas = tenant.BridgeDomain.list(detail=True, sort='name')
    if datas:
        key = tenant.BridgeDomain.attrs()
        col = []
        for k in key: col.append('+' + k if k != 'name' else V('Bridge Domain Name'))
        col.append('+Subnet')
        table = FooTable(*col)
        nav.Tab(V('Bridge Domain Details'), table)
        for data in datas:
            val = []
            for k in key: val.append(data[k])
            sub_val = DIV()
            sub_datas = data.Subnet.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas:
                    sub_val.html(PARA().html(sub_data['ip']))
            val.append(sub_val)
            table.Record(*val)
    
    #===========================================================================
    # Context
    #===========================================================================
    datas = tenant.Context.list(detail=True, sort='name')
    if datas:
        key = tenant.Context.attrs()
        col = []
        for k in key: col.append('+' + k if k != 'name' else V('Context Name'))
        table = FooTable(*col)
        nav.Tab(V('Context Details'), table)
        for data in datas:
            val = []
            for k in key: val.append(data[k])
            table.Record(*val)

    #===========================================================================
    # L3 External
    #===========================================================================
    datas = tenant.L3External.list(detail=True, sort='name')
    if datas:
        key = tenant.L3External.attrs()
        col = []
        for k in key: col.append('+' + k if k != 'name' else V('L3 External Name'))
        table = FooTable(*col)
        nav.Tab(V('L3 External Details'), table)
        for data in datas:
            val = []
            for k in key: val.append(data[k])
            table.Record(*val)

    #===========================================================================
    # Contract
    #===========================================================================
    datas = tenant.Contract.list(detail=True, sort='name')
    if datas:
        key = tenant.Contract.attrs()
        col = []
        for k in key: col.append('+' + k if k != 'name' else V('Contract Name'))
        col.append('+Subject')
        table = FooTable(*col)
        nav.Tab(V('Contract Details'), table)
        for data in datas:
            val = []
            for k in key: val.append(data[k])
            sub_val = DIV()
            sub_datas = data.Subject.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas:
                    sub_val.html(PARA().html(sub_data['name']))
            val.append(sub_val)
            table.Record(*val)
    
    #===========================================================================
    # Filter
    #===========================================================================
    datas = tenant.Filter.list(detail=True, sort='name')
    if datas:
        key = tenant.Filter.attrs()
        col = []
        for k in key: col.append('+' + k if k != 'name' else V('Filter Name'))
        col.append('+Filter Entry')
        table = FooTable(*col)
        nav.Tab(V('Filter Details'), table)
        for data in datas:
            val = []
            for k in key: val.append(data[k])
            sub_val = DIV()
            sub_datas = data.FilterEntry.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas:
                    sub_val.html(PARA().html(sub_data['name']))
            val.append(sub_val)
            table.Record(*val)

def epg_all(R, M, V):
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    
    epgs = M.EPG.list(detail=True, sort='dn')
    table = DataTable(V('Domain'), V('EPG Name'), V('Bridge Domain'), V('Provided Contracts'), V('Consumed Contracts'), V('Binding Path'))
    epg_cnt = 0
    for domain_name in M:
        
        for epg in epgs[domain_name]:
            epg_cnt += 1
            raw = re.sub('(uni/|tn-|ap-|epg-)', '', epg['dn']).split('/')
            path_raw = '/'.join(raw[:2])
            name_raw = raw[2]
            name = '<small>' + path_raw + '/</small><strong>' + name_raw + '</strong>' 
            
            bd_data = ' '
            prov_data = ' '
            cons_data = ' '
            path_data = ' '
            encap_data = ' '
            
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
            
            table.Record(domain_name, name, bd_data, prov_data, cons_data, path_data,
                         **ATTR.click('/aci/show/epgroup/%s/%s' % (domain_name, epg['dn'])))
            
    if not table: V.Page.html(Alert(V('Info'), V('Non-exist APIC Connection'), **{'class' : 'alert-info'}))
    else:
        V.Page.html(CountPanel(V('EPG'), 'object-group', epg_cnt, **{'class' : 'panel-default'})).html(table)

def epg_one(R, M, V):
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    
    epg = M[domain_name](dn, detail=True)
    
    V.Page.html(HEAD(1).html(epg['name']))
    
    hdata = M.getHealth()
    try:
        chart = Line(*hdata['_tstamp'], **(Chart.SCALE100 + Chart.NOLEGEND + Chart.RATIO_8)).Data(dn, *hdata[domain_name + '/' + dn])
        V.Page.html(ROW().html(chart))
    except: pass
    
    nav = Navigation()
    V.Page.html(ROW().html(COL(12).html(nav)))
    
    #===========================================================================
    # Details
    #===========================================================================
    kv = KeyVal()
    for key in epg.attrs(): kv.Data(key, epg[key])
    nav.Tab(V('Details'), kv)
    
    #===========================================================================
    # BD Relation
    #===========================================================================
    act = epg.Class('fvRsBd')
    datas = act.list(detail=True)
    if datas:
        data = datas[0]
        kv = KeyVal()
        for key in data.attrs(): kv.Data(key, data[key])
        nav.Tab(V('Bridge Domain Relations'), kv)
        
    #===========================================================================
    # Path Attach
    #===========================================================================
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
        
    #===========================================================================
    # Provider
    #===========================================================================
    act = epg.Class('fvRsProv')
    datas = act.list(detail=True)
    if datas:
        key = act.attrs()
        col = []
        for k in key: col.append('+' + k if k != 'tnVzBrCPName' else V('Contract Name'))
        table = FooTable(*col)
        nav.Tab(V('Provided Contracts'), table)
        for data in datas:
            val = []
            for k in key: val.append(data[k])
            table.Record(*val)
    
    #===========================================================================
    # Consumer
    #===========================================================================
    act = epg.Class('fvRsCons')
    datas = act.list(detail=True)
    if datas:
        key = act.attrs()
        col = []
        for k in key: col.append('+' + k if k != 'tnVzBrCPName' else V('Contract Name'))
        table = FooTable(*col)
        nav.Tab(V('Consumed Contracts'), table)
        for data in datas:
            val = []
            for k in key: val.append(data[k])
            table.Record(*val)

    #===========================================================================
    # Endpoint
    #===========================================================================
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
    

def ep_all(R, M, V):
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    
    eps = M.Endpoint.list(detail=True, sort='dn')
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
            
            table.Record(domain_name, STRONG().html(mac), epg_name, intf, encap, ip, nic_type,
                         **ATTR.click('/aci/show/endpoint/%s/%s' % (domain_name, dn)))
            
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
        )
        V.Page.html(COL(12).html(table))

def ep_one(R, M, V):
    V.Menu.html(BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')))
    
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    
    ep = M[domain_name](dn, detail=True)
    
    V.Page.html(HEAD(1).html(ep['name']))
    
    nav = Navigation()
    V.Page.html(ROW().html(COL(12).html(nav)))
    
    #===========================================================================
    # Details
    #===========================================================================
    kv = KeyVal()
    for key in ep.attrs(): kv.Data(key, ep[key])
    nav.Tab(V('Details'), kv)
    
    #===========================================================================
    # EPG
    #===========================================================================
    epg = ep.parent(detail=True)
    if epg and epg.class_name == 'fvAEPg':
        kv = KeyVal()
        for key in epg.attrs(): kv.Data(key, epg[key])
        nav.Tab(V('Endpoint Group'), kv)
        
        #=======================================================================
        # Interface
        #=======================================================================
        children = ep.children(detail=True)
        for child in children:
            if child.class_name == 'fvRsCEpToPathEp':
                kv = KeyVal()
                for key in child.attrs(): kv.Data(key, child[key])
                nav.Tab(V('Path Relation'), kv)
                break
        
        hosts = []
        nics = M[domain_name].Class('compNic').list(mac=ep['mac'], detail=True)
        if nics:
            nicdiv = DIV()
            hstdiv = DIV()
            nav.Tab(V('Network Interface'), nicdiv)
            nav.Tab(V('Host Detail'), hstdiv)
            for nic in nics:
                key = nic.attrs()
                col = []
                val = []
                for k in key: col.append('+' + k if k != 'name' else V('NIC Name'))
                for k in key: val.append(nic[k])
                nicdiv.html(FooTable(*col).Record(*val))
                
                host = nic.parent(detail=True)
                if host and host['dn'] not in hosts:
                    hosts.append(host['dn'])
                    key = host.attrs()
                    col = []
                    val = []
                    for k in key: col.append('+' + k if k != 'name' else V('Host Name'))
                    for k in key: val.append(host[k])
                    hstdiv.html(FooTable(*col).Record(*val))
    
    
    