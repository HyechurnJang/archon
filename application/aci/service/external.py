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

def external_all(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    extns, ctxts, subns, provs, conss = Burst(
    )(M.L3Profile.list, detail=True, sort='dn'
    )(M.Context.list, detail=True, sort='dn'
    )(M.Class('l3extSubnet').list, detail=True, sort='dn'
    )(M.Class('fvRsProv').list, detail=True, sort='dn'
    )(M.Class('fvRsCons').list, detail=True, sort='dn'
    ).do()
    
    #===========================================================================
    # Logic
    #===========================================================================
    table = TABLE.BASIC(V('Domain'), V('Name'), V('Contexts'), V('Subnets'), V('Provided Contracts'), V('Consumed Contracts'))
    extn_cnt = 0
    
    for domain_name in sorted(M.keys()):
        for extn in extns[domain_name]:
            extn_cnt += 1
            dn = extn['dn']
            path, _, rn = extn.rn()
            path = re.sub('(uni/|tn-|out-)', '', path)
            name = PARA().html(SMALL().html(path + '/')).html(GET('/aci/show/external/%s/%s' % (domain_name, dn)).html(rn))
            scope = extn['scope']
            
            extn_ctxt = ' '
            extn_subn = ' '
            extn_prov = ' '
            extn_cons = ' '
            for ctxt in ctxts[domain_name]:
                if scope == ctxt['scope']: extn_ctxt += '<p><small>' + ctxt['name'] + ',&nbsp;</small></p>'
            for subn in subns[domain_name]:
                if dn in subn['dn']: extn_subn += '<p><small>' + subn['ip'] + ',&nbsp;</small></p>'
            for prov in provs[domain_name]:
                if dn in prov['dn']: extn_prov += '<p><small>' + re.sub('/\w+-', '/', prov['tDn']).replace('uni/', '') + ',&nbsp;</small></p>'
            for cons in conss[domain_name]:
                if dn in cons['dn']: extn_cons += '<p><small>' + re.sub('/\w+-', '/', cons['tDn']).replace('uni/', '') + ',&nbsp;</small></p>'
            table.Record(domain_name, name, extn_ctxt, extn_subn, extn_prov, extn_cons)
    
    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(
        ROW().html(
            COL(12).html(COUNTER(V('External Networks'), 'cloud', extn_cnt, CLASS='panel-dgrey'))
        ),
        table
    )
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))

def external_one(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    extn = M[domain_name](dn, detail=True)
    outn = extn.parent(detail=True)
    
    #===========================================================================
    # Logic
    #===========================================================================
    nav = NAV()
    
    # Detail
    kv = KEYVAL()
    for key in extn.keys(): kv.Data(key, extn[key])
    nav.Tab(V('Details'), kv)
    
    # Topology
    topo = TOPO()
    set_topo(topo, dn, color='red', path_color='orange', dot=True)
    set_topo(topo, outn['dn'])
    nav.Tab(V('Topology'), DIV(STYLE='text-align:center;padding-top:10px;').html(topo))
    
    # Out Network
    kv = KEYVAL()
    for key in outn.keys(): kv.Data(key, outn[key])
    nav.Tab(V('Outside Network'), kv)
    
    fold = None
    fold_key = None
    prov = None
    prov_key = None
    cons = None
    cons_key = None
    
    children = extn.children(detail=True)
    for child in children:
        if child.class_name == 'vnsFolderInst':
            if fold == None:
                fold_key = M[domain_name].Class('vnsFolderInst').keys()
                fold = TABLE.FLIP(*['+' + k if k != 'name' else V('Name') for k in fold_key])
            fold.Record(*[child[k] for k in fold_key])
            set_topo(topo, child['dn'])
        elif child.class_name == 'fvRsProv':
            if prov == None:
                prov_key = M[domain_name].Class('fvRsProv').keys()
                prov = TABLE.FLIP(*['+' + k if k != 'tRn' else V('Name') for k in prov_key])
            prov.Record(*[child[k] for k in prov_key])
            set_topo(topo, child['tDn'], color='pink')
            topo.Edge(dn, child['tDn'])
        elif child.class_name == 'fvRsCons':
            if cons == None:
                cons_key = M[domain_name].Class('fvRsCons').keys()
                cons = TABLE.FLIP(*['+' + k if k != 'tRn' else V('Name') for k in cons_key])
            cons.Record(*[child[k] for k in cons_key])
            set_topo(topo, child['tDn'], color='cyan')
            topo.Edge(dn, child['tDn'])
    
    #===========================================================================
    # View
    #===========================================================================
    if fold != None: nav.Tab(V('Folders'), fold)
    if prov != None: nav.Tab(V('Provided Contracts'), prov)
    if cons != None: nav.Tab(V('Consumed Contracts'), cons)
    V.Page.html(
        HEAD(1).html(extn['name']),
        nav
    )
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))
