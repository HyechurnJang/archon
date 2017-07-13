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

import time
from archon import *
from common import *

def epg_all(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    epgs = M.EPG.list(detail=True, sort='dn')
    
    #===========================================================================
    # Logic
    #===========================================================================
    table = TABLE.BASIC(V('Domain'), V('Name'), V('Bridge Domain'), V('Provided Contracts'), V('Consumed Contracts'), V('Binding Path'))
    epg_cnt = 0
    for domain_name in sorted(M.keys()):
        for epg in epgs[domain_name]:
            epg_cnt += 1
            raw = re.sub('(uni/|tn-|ap-|epg-)', '', epg['dn']).split('/')
            path_raw = '/'.join(raw[:2])
            name_raw = raw[2]
            name = PARA().html(SMALL().html(path_raw + '/'), GET('/aci/show/epgroup/%s/%s' % (domain_name, epg['dn'])).html(name_raw))
            bd_data = ' '
            prov_data = ' '
            cons_data = ' '
            path_data = ' '
            children = epg.children(detail=True)
            for child in children:
                if child.class_name == 'fvRsBd' and child['state'] == 'formed':
                    bd_data += '<p><small>' + child['tDn'].split('/BD-')[1] + ',&nbsp;</small></p>'
                elif child.class_name == 'fvRsProv' and child['state'] == 'formed':
                    prov_data += '<p><small>' + child['tDn'].split('/brc-')[1] + ',&nbsp;</small></p>'
                elif child.class_name == 'fvRsCons' and child['state'] == 'formed':
                    cons_data += '<p><small>' + child['tDn'].split('/brc-')[1] + ',&nbsp;</small></p>'
                elif child.class_name == 'fvRsPathAtt' and child['state'] == 'formed':
                    path_data += '<p><small>' + re.sub('(topology/|pod-|protpaths-|paths-|pathep-|\[|\])', '', child['tDn']) + '(%s),&nbsp;</small></p>' % child['encap']
            table.Record(domain_name, name, bd_data, prov_data, cons_data, path_data)
    
    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(
        ROW().html(
            COL(12).html(COUNTER(V('EPG'), 'object-group', epg_cnt, CLASS='panel-dgrey'))
        ),
        table
    )
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))

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
    nav = NAV()
    active_ep = None
    
    # Health
    hdata = M.getHealth()
    health = None
    try: health = CHART.LINE(*hdata['_tstamp'], **CHART.THEME_HEALTH).Data(dn, *hdata[domain_name + '/' + dn])
    except: pass
    
    # Details
    kv = KEYVAL()
    for key in epg.keys(): kv.Data(key, epg[key])
    nav.Tab(V('Details'), kv)
    
    # Topology
    topo = TOPO()
    set_topo(topo, dn, color='red', path_color='orange', dot=True)
    nav.Tab(V('Topology'), DIV(STYLE='text-align:center;padding-top:10px;').html(topo))
    
    # BD Relation
    act = epg.Class('fvRsBd')
    datas = act.list(detail=True)
    if datas:
        data = datas[0]
        kv = KEYVAL()
        for key in data.keys(): kv.Data(key, data[key])
        set_topo(topo, data['tDn'], color='orange')
        topo.Edge(dn, data['tDn'])
        nav.Tab(V('Bridge Domains'), kv)
        
    # Path Attach
    act = epg.Class('fvRsPathAtt')
    datas = act.list(detail=True)
    if datas:
        key = act.keys()
        key.remove('encap')
        key.append('encap')
        col = []
        for k in key:
            if k == 'tDn' : col.append(V('Name'))
            elif k == 'encap' : col.append(V('Encap'))
            else: col.append('+' + k)
        table = TABLE.FLIP(*col)
        nav.Tab(V('Path Attachments'), table)
        for data in datas:
            val = []
            for k in key:
                if k == 'tDn': val.append(re.sub('(topology/|pod-|protpaths-|paths-|pathep-|\[|\])', '', data['tDn']))
                else: val.append(data[k])
            table.Record(*val)
            set_topo(topo, data['tDn'])
            topo.Edge(dn, data['tDn'])
        
    # Provider
    act = epg.Class('fvRsProv')
    datas = act.list(detail=True)
    if datas:
        key = act.keys()
        table = TABLE.FLIP(*['+' + k if k != 'tnVzBrCPName' else V('Name') for k in key])
        nav.Tab(V('Provided Contracts'), table)
        for data in datas: table.Record(*[data[k] for k in key])
    
    # Consumer
    act = epg.Class('fvRsCons')
    datas = act.list(detail=True)
    if datas:
        key = act.keys()
        table = TABLE.FLIP(*['+' + k if k != 'tnVzBrCPName' else V('Name') for k in key])
        nav.Tab(V('Consumed Contracts'), table)
        for data in datas: table.Record(*[data[k] for k in key])

    # Endpoint
    datas = epg.Endpoint.list(detail=True)
    if datas:
        active_ep = ROW(STYLE='margin-bottom:20px;')
        key = epg.Endpoint.keys()
        col = []
        for k in key:
            if k == 'name': col.append(V('Name'))
            elif k == 'ip' : col.append(V('IP'))
            elif k == 'encap' : col.append(V('Encap'))
            else: col.append('+' + k)
        table = TABLE.FLIP(*col)
        nav.Tab(V('Endpoint'), table)
        for data in datas:
            val = []
            for k in key:
                if k == 'name': val.append(GET('/aci/show/endpoint/%s/%s' % (domain_name, data['dn'])).html(data[k]))
                else: val.append(data[k])
            table.Record(*val)
            set_topo(topo, data['dn'], color='black')
            active_ep.html(
                COL(2, STYLE='padding:0px 5px 0px 5px').html(
                    DIV(STYLE='float:left;').html(IMG('/resources/images/tool/nic.png', width='20px')),
                    DIV(STYLE='padding-left:22px;').html(data['name'])
                )
            )
    if epg['isAttrBasedEPg'] == 'yes':
        
        crtrn = epg.Class('fvCrtrn').list()[0]
        
        if R.Method == 'POST':
            ips = get_ip_range(R.Data['ip_stt'], R.Data['ip_end'])
            idx = 0
            uip_name_base = str(int(time.time()))
            uip_descs = get_comma_to_list(R.Data['desc'])
            uip_desc_len = len(uip_descs)
            if uip_descs[-1] == '' and uip_desc_len > 1:
                uip_desc_def = uip_descs[-2]
                uip_desc_len -= 1
            else: uip_desc_def = ''
            
            for ip in ips:
                uip = crtrn.Class('fvIpAttr')
                uip.class_pkey = 'name'
                uip.class_ident = '/ipattr-%s'
                uip_name = '%s%d' % (uip_name_base, idx)
                if uip_desc_len > idx: uip_desc = uip_descs[idx]
                else: uip_desc = uip_desc_def
                idx += 1
                try: uip.create(name=uip_name, ip='%s/32' % ip, usefvSubnet='no', descr=uip_desc)
                except: pass
                else:
                    if uip_desc != '': set_ip_name(ip, uip_desc)
        
        uepg_view = DIV()
        nav.Tab(V('IP Mobility'), uepg_view)
        
        uepg_in = POST('/aci/show/epgroup/%s/%s' % (domain_name, dn), CLASS='btn-primary', STYLE='float:right;')
        uepg_in.Text('ip_stt', POST.LABEL_INLINE(V('IP Start'), STYLE='width:100px;'))
        uepg_in.Text('ip_end', POST.LABEL_INLINE(V('IP End'), STYLE='width:100px;'))
        uepg_in.Text('desc', POST.LABEL_INLINE(V('Department/User'), STYLE='width:100px;'))
        uepg_view.html(
            HEAD(4).html(V('Register IPs')),
            DIV(STYLE='padding-top:5px;').html(uepg_in)
        )
        
        table = TABLE.BASIC(V('IP'), V('Department/User'), V('Use EPG Subnet'))
        uepg_view.html(
            HEAD(4).html(V('Mobility IPs')),
            DIV(STYLE='padding-top:5px;').html(table)
        )
        
        datas = crtrn.Class('fvIpAttr').list(detail=True)
        for data in datas:
            uip_desc = data['descr'].decode('unicode_escape')
            uip_ip = data['ip'].split('/')[0]
            table.Record(uip_ip, uip_desc, data['usefvSubnet'])
            if uip_desc != '' and get_ip_name(uip_ip) != uip_desc: set_ip_name(uip_ip, uip_desc)

    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(HEAD(1).html(epg['name']))
    if health != None: V.Page.html(ROW().html(health))
    if active_ep != None:
        V.Page.html(
            HEAD(3).html(V('Active Endpoints')),
            active_ep
        )
    V.Page.html(nav)
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))
