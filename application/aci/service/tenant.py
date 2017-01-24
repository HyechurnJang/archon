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

def tenant_all(R, M, V):
#     #===========================================================================
#     # Method Work
#     #===========================================================================
#     alert = None
#     if R.Method == 'POST':
#         try: M[R.Data['domain_name']].Tenant.create(name=R.Data['tenant_name'])
#         except:
#             alert = Alert(V('Create Failed'),
#                           V('Incorrect Config Data'),
#                           **{'class' : 'alert-danger'})
#         else:
#             alert = Alert(V('Create Success'),
#                           V('Tenant %s/%s Created') % (R.Data['domain_name'], R.Data['tenant_name']),
#                           **{'class' : 'alert-success'})
#     if R.Method == 'DELETE':
#         domain_name = R.Path[3]
#         dn = '/'.join(R.Path[4:])
#         try: M[domain_name](dn).delete()
#         except:
#             alert = Alert(V('Delete Failed'),
#                           V('Incorrect Domain or Tenant Name'),
#                           **{'class' : 'alert-danger'})
#         else:
#             alert = Alert(V('Delete Success'),
#                           V('Tenant %s/%s Deleted') % (domain_name, dn),
#                           **{'class' : 'alert-success'})
            
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
    table = DataTable(V('Domain'), V('Name'), V('EPG'), V('Bridge Domain'), V('Context'), V('Contract'), V('Filter'))
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
                if tn['dn'] in epg['dn']: epg_data += '<p><small>' + re.sub('(ap-|epg-)', '', '/'.join(epg['dn'].split('/')[2:])) + ',&nbsp;</small></p>'
            for bd in bds[domain_name]:
                if tn['dn'] in bd['dn']: bd_data += '<p><small>' + bd['name'] + ',&nbsp;</small></p>'
            for ctx in ctxs[domain_name]:
                if tn['dn'] in ctx['dn']: ctx_data += '<p><small>' + ctx['name'] + ',&nbsp;</small></p>'
            for ctr in ctrs[domain_name]:
                if tn['dn'] in ctr['dn']: ctr_data += '<p><small>' + ctr['name'] + ',&nbsp;</small></p>'
            for flt in flts[domain_name]:
                if tn['dn'] in flt['dn']: flt_data += '<p><small>' + flt['name'] + ',&nbsp;</small></p>'
            table.Record(domain_name, name, epg_data, bd_data, ctx_data, ctr_data, flt_data)
    
    #===========================================================================
    # View
    #===========================================================================
#     if alert != None: V.Page.html(alert)
    V.Page.html(
        ROW().html(
            COL(12).html(CountPanel(V('Tenants'), 'users', tn_cnt, **{'class' : 'panel-dgrey'}))
        ),
        table
    )

    V.Menu.html(
        BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')),
#         Modal(V('Create New Tenant'), BUTTON(**{'class' : 'btn-primary'}).html(V('Create'))).html(
#             Post('/aci/show/tenant', V('Register'), **{'class' : 'btn-primary', 'style' : 'float:right;'}
#             ).Text('domain_name', Post.TopLabel(V('Domain Name')), placeholder=V('Unique Name Required')
#             ).Text('tenant_name', Post.TopLabel(V('Tenant Name')), placeholder=V('Unique Name Required'))
#         )
    )

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
    try: health = HealthLine(*hdata['_tstamp']).Data(dn, *hdata[domain_name + '/' + dn])
    except: pass
    
    # Details
    kv = KeyVal()
    for key in tenant.keys(): kv.Data(key, tenant[key])
    nav.Tab(V('Details'), kv)
    
    # Topology
    topo = Topo()
    set_topo(topo, dn, color='red', path_color='orange', dot=True)
    nav.Tab(V('Topology'), DIV(style='text-align:center;padding-top:10px;').html(topo))

    # App Profile
    datas = tenant.AppProfile.list(detail=True, sort='name')
    if datas:
        key = tenant.AppProfile.keys()
        col = ['+' + k if k != 'name' else V('Name') for k in key]
        col.append(V('+EPG'))
        table = FooTable(*col)
        nav.Tab(V('Application Profiles'), table)
        for data in datas:
            val = [data[k] for k in key]
            sub_val = DIV()
            sub_datas = data.EPG.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas: sub_val.html(PARA().html(Get('/aci/show/epgroup/%s/%s' % (domain_name, sub_data['dn'])).html(sub_data['name'])))
            val.append(sub_val)
            table.Record(*val)
            set_topo(topo, data['dn'], color='orange', path_color='orange')
    
    # Bridge Domain
    datas = tenant.BridgeDomain.list(detail=True, sort='name')
    if datas:
        key = tenant.BridgeDomain.keys()
        col = ['+' + k if k != 'name' else V('Name') for k in key]
        col.append(V('+Subnet'))
        table = FooTable(*col)
        nav.Tab(V('Bridge Domains'), table)
        for data in datas:
            val = [data[k] for k in key]
            sub_val = ' '
            sub_datas = data.Subnet.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas: sub_val += '<p>' + sub_data['ip'] + '</p>'
            val.append(sub_val)
            table.Record(*val)
            set_topo(topo, data['dn'], color='orange', path_color='orange')
    
    # Context
    datas = tenant.Context.list(detail=True, sort='name')
    if datas:
        key = tenant.Context.keys()
        table = FooTable(*['+' + k if k != 'name' else V('Name') for k in key])
        nav.Tab(V('Contexts'), table)
        for data in datas: table.Record(*[data[k] for k in key])
        set_topo(topo, data['dn'], color='orange', path_color='orange')

    # L3 External
    datas = tenant.L3Out.list(detail=True, sort='name')
    if datas:
        key = tenant.L3Out.keys()
        table = FooTable(*['+' + k if k != 'name' else V('Name') for k in key])
        nav.Tab(V('L3 Externals'), table)
        for data in datas: table.Record(*[data[k] for k in key])
        set_topo(topo, data['dn'], color='orange', path_color='orange')

    # Contract
    datas = tenant.Contract.list(detail=True, sort='name')
    if datas:
        key = tenant.Contract.keys()
        col = ['+' + k if k != 'name' else V('Name') for k in key]
        col.append(V('+Subject'))
        table = FooTable(*col)
        nav.Tab(V('Contracts'), table)
        for data in datas:
            val = [data[k] for k in key]
            sub_val = ' '
            sub_datas = data.Subject.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas: sub_val += '<p>' + sub_data['name'] + '</p>'
            val.append(sub_val)
            table.Record(*val)
            set_topo(topo, data['dn'], color='orange', path_color='orange')
    
    # Filter
    datas = tenant.Filter.list(detail=True, sort='name')
    if datas:
        key = tenant.Filter.keys()
        col = ['+' + k if k != 'name' else V('Name') for k in key]
        col.append(V('+Filter Entry'))
        table = FooTable(*col)
        nav.Tab(V('Filters'), table)
        for data in datas:
            val = [data[k] for k in key]
            sub_val = ' '
            sub_datas = data.FilterEntry.list(sort='name')
            if sub_datas:
                for sub_data in sub_datas: sub_val += '<p>' + sub_data['name'] + '</p>' 
            val.append(sub_val)
            table.Record(*val)
            set_topo(topo, data['dn'], color='orange', path_color='orange')

    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(HEAD(1).html(tenant['name']))
    if health != None: V.Page.html(ROW().html(health))
    V.Page.html(nav)
    V.Menu.html(
        BUTTON(**(ATTR.click('/'.join(R.Path)) + {'class' : 'btn-primary'})).html(V('Refresh')),
#         Modal(V('Delete Tenant'), BUTTON(**{'class' : 'btn-danger'}).html(V('Delete'))).html(
#             HEAD(3).html(V('Is Right ?'), DelButton('/aci/show/tenant/%s/%s' % (domain_name, dn), tail=True))
#         )
    )
