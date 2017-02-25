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
from ..models import FaultMessage

@TABLE.ASYNC.pageview()
def fault_async(R, M, V):
    domain_name = R.Path[4]
    
#     flt_cnt, faults = Burster(
#     )(M[domain_name].Fault.count
#     )(M[domain_name].Fault.list, page=(R.Page,R.Length), detail=True, sort='created|desc'
#     ).run()
    flt_cnt = M[domain_name].Fault.count()
    faults = M[domain_name].Fault.list(page=(R.Page,R.Length), detail=True, sort='created|desc')
    
    table = TABLE.ASYNCDATA(R.Draw, flt_cnt, flt_cnt)
    for fault in faults:
        table.Record(GET('/aci/show/fault/%s/%s' % (domain_name, fault['dn'])).html(fault['subject']),
                     fault['severity'],
                     STRWRAP(400).html(SMALL().html(fault['descr'])),
                     SMALL().html(fault['created'][:-10]))
    return table

def fault_all(R, M, V):
    
#     cri_cnt, maj_cnt, min_cnt, war_cnt = Burster(
#     )(M.Fault.count, severity='critical'
#     )(M.Fault.count, severity='major'
#     )(M.Fault.count, severity='minor'
#     )(M.Fault.count, severity='warning'
#     ).run()
    cri_cnt = M.Fault.count(severity='critical')
    maj_cnt = M.Fault.count(severity='major')
    min_cnt = M.Fault.count(severity='minor')
    war_cnt = M.Fault.count(severity='warning')
    
    cri_num = 0
    maj_num = 0
    min_num = 0
    war_num = 0
    
    nav = NAV()
    
    for domain_name in M:
        cri_num += cri_cnt[domain_name]
        maj_num += maj_cnt[domain_name]
        min_num += min_cnt[domain_name]
        war_num += war_cnt[domain_name]
        nav.Tab(
            domain_name,
            DIV(STYLE='padding-top:10px;').html(TABLE.ASYNC('aci/show/fault/fault_async/%s' % domain_name, V('Subjects'), V('Type'), V('Description'), V('Time Stamp')))
        )
    
    V.Page.html(
        ROW().html(
            COL(3).html(COUNTER(V('Critical'), 'bolt', cri_num, CLASS='panel-red').click('/aci/show/fault/critical')),
            COL(3).html(COUNTER(V('Major'), 'exclamation-triangle', maj_num, CLASS='panel-danger').click('/aci/show/fault/major')),
            COL(3).html(COUNTER(V('Minor'), 'exclamation-circle', min_num, CLASS='panel-yellow').click('/aci/show/fault/minor')),
            COL(3).html(COUNTER(V('Warning'), 'exclamation', war_num, CLASS='panel-warning').click('/aci/show/fault/warning'))
        ),
        nav
    )
    
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))

def fault_one(R, M, V):
    #===========================================================================
    # Get Data
    #===========================================================================
    domain_name = R.Path[3]
    dn = '/'.join(R.Path[4:])
    fault = M[domain_name](dn, detail=True)
    
    #===========================================================================
    # Logic
    #===========================================================================
    nav = NAV()
    occur = V('From Instance') if fault.class_name == 'faultInst' else V('Delegated')
    title = '%s %s : %s' % (fault['type'].upper(), fault['severity'].upper(), fault['subject'])
    desc = fault['descr']
    
    # Guide
    try: guide = FaultMessage.objects.get(code=fault['code'])
    except: pass
    else:
        kv = KEYVAL()
        kv.Data('Title', guide.title)
        kv.Data('Code', guide.code)
        kv.Data('Syslog', guide.syslog)
        kv.Data('Explanation', guide.explan)
        actions = guide.actions.split('\n')
        act = ''
        for i in range(0, len(actions)): act += ('<p><strong>Step%d</strong> : ' % (i + 1)) + actions[i] + '</p>'
        kv.Data('Actions', act)
        nav.Tab(V('Guide'), kv)
    
    # Details
    kv = KEYVAL()
    for key in fault.keys(): kv.Data(key, fault[key])
    nav.Tab(V('Details'), kv)
    
    # Object
    if fault.class_name == 'faultInst': obj_dn = fault['dn'].split('/fault-')[0]
    elif fault.class_name == 'faultDelegate': obj_dn = fault['dn'].split('/fd-')[0]
    else: obj_dn = None
    if obj_dn != None:
        try: obj = M[domain_name](obj_dn, detail=True)
        except: pass
        else:
            kv = KEYVAL()
            for key in obj.keys(): kv.Data(key, obj[key])
            nav.Tab(V('Object'), kv)
    
    #===========================================================================
    # View
    #===========================================================================
    V.Page.html(HEAD(1).html(title))
    if fault.class_name == 'faultInst':
        V.Page.html(
            HEAD(3).html('%s %s' % (fault['cause'], occur)),
            HEAD(4).html(obj_dn)
        )
    elif fault.class_name == 'faultDelegate':
        V.Page.html(
            HEAD(3).html('%s %s' % (fault['cause'], occur)),
            HEAD(4).html(fault['affected'])
        )
    V.Page.html(
        HEAD(3).html(V('Description')),
        HEAD(4).html(desc),
        nav
    )
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))
