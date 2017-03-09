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
from manager import Manager

#===============================================================================
# Create your views here.
#===============================================================================
@pageview(Manager)
def overview(R, M, V):
    if not M: V.Page.html(ALERT(V('Info'), V('Non-exist ASA Connection'), CLASS='alert-info')); return
    
    health, nat_count, conn_count = Burst(
    )(M.getHealth
    )(M.NAT.count
    )(M.Conn.count
    ).do()
    
    chart_hist = CHART.LINE(height=145, min=0, max=100, *health['_tstamp'])
    chart_curr_row = ROW()
    chart_conn_tran = DIV()
    
    for domain_name in sorted(M.keys()):
        chart_curr = CHART.BAR('CPU', 'Memory', 'Disk', height=145, **CHART.THEME_UTIL)
        cpu_curr = 0
        mem_curr = 0
        disk_curr = 0
        for dn in health:
            if domain_name + '/cpu' in dn:
                chart_hist.Data(domain_name + '/CPU', *health[dn])
                cpu_curr = health[dn][-1]
            elif domain_name + '/mem' in dn:
                chart_hist.Data(domain_name + '/Memory', *health[dn])
                mem_curr = health[dn][-1]
            elif domain_name + '/disk' in dn:
                chart_hist.Data(domain_name + '/Disk', *health[dn])
                disk_curr = health[dn][-1]
        chart_curr.Data('Current', cpu_curr, mem_curr, disk_curr)
        chart_curr_row.html(
            COL(2).html(chart_curr, HEAD(4, STYLE='margin:0px;text-align:center;').html(domain_name))
        )
        
        chart_conn = CHART.BAR('Max', 'Current',
                               height=40, margin=['65px', '0px', '20px', '20px'],
                               pivot=True, tooltip=False,
                               color=['rgba(128,177,211,0.8)', 'rgba(255,0,0,0.8)']
        ).Data(
            'Connections', conn_count[domain_name]['most_used'], conn_count[domain_name]['in_use'], 
        )
        
        chart_tran = CHART.BAR('Max', 'Current',
                               height=40, margin=['65px', '0px', '20px', '20px'],
                               pivot=True, tooltip=False,
                               color=['rgba(128,177,211,0.8)', 'rgba(255,0,0,0.8)']
        ).Data(
            'NATs', nat_count[domain_name]['most_used'], nat_count[domain_name]['in_use']
        )
        chart_conn_tran.html(
            ROW().html(
                COL(1, STYLE='padding:10px 0px 0px 0px;').html(HEAD(3).html(domain_name)),
                COL(11, STYLE='padding:0px;').html(
                    ROW().html(
                        COL(2, STYLE='padding:5px 0px 0px 0px;').html(HEAD(4, STYLE='margin:0px;text-align:right;').html('Connections')),
                        COL(10, STYLE='padding:0px;').html(chart_conn)
                    ),
                    ROW().html(
                        COL(2, STYLE='padding:5px 0px 0px 0px;').html(HEAD(4, STYLE='margin:0px;text-align:right;').html('Translations')),
                        COL(10, STYLE='padding:0px;').html(chart_tran)
                    )
                )
            )
        )
        
    V.Page.html(
        PANEL(CLASS='panel-dgrey').Head(STRONG().html('Utilization')).Body(
            HEAD(3, STYLE='margin:0px;').html('System Utilization History'),
            chart_hist,
            HEAD(3, STYLE='margin:0px;').html('System Current'),
            chart_curr_row
        ),
        PANEL(CLASS='panel-dgrey').Head(STRONG().html('Counts')).Body(
            chart_conn_tran
        )
    )
    
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))

@pageview(Manager)
def static_nat(R, M, V):
    if not M: V.Page.html(ALERT(V('Info'), V('Non-exist ASA Connection'), CLASS='alert-info')); return
    
    nats, objs = Burst(
    )(M.NAT.list
    )(M.Object
    ).do()
    
    table = TABLE.BASIC('Domain', 'Original', 'Translated')
    
    nat_cnt_cnf = 0
    
    counters = ROW()
    
    for domain_name in sorted(M.keys()):
        if domain_name not in objs: continue
        if domain_name not in nats: continue
        
        dom_objs = objs[domain_name]
        
        dom_cnt_cnf = 0
         
        for nat in nats[domain_name]:
            if nat['mode'] == 'static':
                osrc = nat['oSource']
                tsrc = nat['tSource']
                oip = dom_objs[osrc] if osrc in dom_objs else osrc
                tip = dom_objs[tsrc] if tsrc in dom_objs else tsrc
                
                table.Record(domain_name,
                             '<small>%s:%s:</small><strong>%s</strong>' % (nat['oInterface'], osrc, oip),
                             '<small>%s:%s:</small><strong>%s</strong>' % (nat['tInterface'], tsrc, tip))
                dom_cnt_cnf += 1
        
        nat_cnt_cnf += dom_cnt_cnf
        
        counters.html(
            COL(2).html(
                PANEL(CLASS='panel-lgrey', STYLE='text-align:center;'
                ).Head(
                    HEAD(4, STYLE='margin:0px;').html(domain_name)
                ).Body(
                    HEAD(3, STYLE='margin:0px;').html(str(dom_cnt_cnf))
                )
            )
        )
    
    V.Page.html(
        COUNTER(V('Static NAT Configs'), 'list', nat_cnt_cnf, CLASS='panel-dgrey'),
        counters,
        table
    )
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))

@pageview(Manager)
def dynamic_nat(R, M, V):
    if not M: V.Page.html(ALERT(V('Info'), V('Non-exist ASA Connection'), CLASS='alert-info')); return
    
    def calc_addr_count(addr_range):
        try:
            addr_range = addr_range.split('-')
            s = addr_range[0].split('.')
            e = addr_range[1].split('.')
            if s[0] == e[0]:
                if s[1] == e[1]:
                    if s[2] == e[2]:
                        return int(e[3]) - int(s[3]) + 1
                    return ((int(e[2]) - int(s[2])) * 256) + (int(e[3]) - int(s[3]) + 1)
                return ((int(e[1]) - int(s[1])) * 65536) + ((int(e[2]) - int(s[2])) * 255) + (int(e[3]) - int(s[3]) + 1)
            return -1
        except: pass
        return 0
    
    def rec_color(val):
        if val >= 70: return 'danger'
        elif val >= 40: return 'warning'
        else: return 'success'
     
    def panel_color(val):
        if val >= 70: return 'panel-red'
        elif val >= 40: return 'panel-yellow'
        else: return 'panel-green'
    
    objs, ogs, nats, nps = Burst(
    )(M.Object
    )(M.ObjectGroup
    )(M.NAT.list
    )(M.NAT.NATPool.list
    ).do()
    
    table = TABLE.BASIC('Domain', 'Original', 'Translated', 'Address Range', 'Allocated', 'Utilization<0->')
    records = []
    
    nat_cnt_cnf = 0
    nat_cnt_ips = 0
    nat_cnt_alloc = 0
    
    counters = ROW()
    
    for domain_name in sorted(M.keys()):
        
        if domain_name not in nats: continue
        if domain_name not in objs: continue
        if domain_name not in ogs: continue
        
        dom_objs = objs[domain_name]
        dom_ogs = ogs[domain_name]
        dom_nps = nps[domain_name]
        
        dom_cnt_cnf = 0
        dom_cnt_ips = 0
        dom_cnt_alloc = 0
        
        for nat in nats[domain_name]:
            if nat['mode'] == 'dynamic' and nat['patPool'] == False:
                osrc = nat['oSource']
                tsrc = nat['tSource']
                
                if tsrc in dom_objs:
                    addr_range = dom_objs[tsrc]
                    if '-' in addr_range:
                        for np in dom_nps:
                            if addr_range == np['range']:
                                alloc = np['allocated']
                                addr_count = calc_addr_count(addr_range)
                                
                                records.append([domain_name, osrc, tsrc, addr_range, addr_count, alloc])
                                 
                                dom_cnt_cnf += 1
                                dom_cnt_ips += addr_count
                                dom_cnt_alloc += alloc
                                break
                        
                elif tsrc in dom_ogs:
                    for obj_name in dom_ogs[tsrc]:
                        addr_range = dom_objs[obj_name]
                        if '-' in addr_range:
                            for np in dom_nps:
                                if addr_range == np['range']:
                                    alloc = np['allocated']
                                    addr_count = calc_addr_count(addr_range)
                                    
                                    records.append([domain_name, osrc, tsrc, addr_range, addr_count, alloc])
                                     
                                    dom_cnt_cnf += 1
                                    dom_cnt_ips += addr_count
                                    dom_cnt_alloc += alloc
                                    break
        
        nat_cnt_cnf += dom_cnt_cnf
        nat_cnt_ips += dom_cnt_ips
        nat_cnt_alloc += dom_cnt_alloc
        
        dom_usage = ((dom_cnt_alloc * 100.0) / dom_cnt_ips) if dom_cnt_alloc > 0 else 0.0
        
        counters.html(
            COL(2).html(
                PANEL(CLASS=panel_color(dom_usage), STYLE='height:105px;text-align:center;'
                ).Head(
                    HEAD(4, STYLE='margin:0px;').html(domain_name)
                ).Body(
                    HEAD(3, STYLE='margin:0px;').html('%.2f<small> %%</small>' % dom_usage),
                    '<strong>%d</strong><small> / %d</small>' % (dom_cnt_alloc, dom_cnt_ips)
                )
            )
        )
        
    
    records = sorted(records, reverse=True, key=lambda r: r[5])
    for r in records:
        pct = ((r[5] * 100.0) / r[4]) if r[5] > 0 else 0.0
        table.Record(r[0], r[1], r[2], r[3], '<strong>%d</strong> / %d' % (r[5], r[4]), '<strong>%.2f</strong> %%' % pct, CLASS=rec_color(pct))
    
    V.Page.html(
        ROW().html(
            COL(4).html(COUNTER(V('Dynamic NAT Configs'), 'list', nat_cnt_cnf, CLASS='panel-dgrey')),
            COL(4).html(COUNTER(V('Dynamic NAT IPs'), 'hashtag', nat_cnt_ips, CLASS='panel-dgrey')),
            COL(4).html(COUNTER(V('Dynamic NAT Allocated'), 'crosshairs', nat_cnt_alloc, CLASS='panel-dgrey')),
        ),
        counters,
        table
    )
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))

@pageview(Manager)
def pat_pool(R, M, V):
    if not M: V.Page.html(ALERT(V('Info'), V('Non-exist ASA Connection'), CLASS='alert-info')); return
    
    def rec_color(val):
        if val >= 70: return 'danger'
        elif val >= 40: return 'warning'
        else: return 'success'
     
    def panel_color(val):
        if val >= 70: return 'panel-red'
        elif val >= 40: return 'panel-yellow'
        else: return 'panel-green'
    
    objs, ogs, nats, pps = Burst(
    )(M.Object
    )(M.ObjectGroup
    )(M.NAT.list
    )(M.NAT.PATPool.list
    ).do()
    
    table = TABLE.BASIC('Domain', 'Original', 'Translated', 'Address', 'Protocol', 'Allocated', 'Utilization<0->')
    records = []
    
    nat_cnt_cnf = 0
    nat_cnt_pool_tcp = 0
    nat_cnt_pool_udp = 0
    nat_cnt_alloc_tcp = 0
    nat_cnt_alloc_udp = 0
    
    counters = ROW()
    
    for domain_name in sorted(M.keys()):
        
        if domain_name not in nats: continue
        if domain_name not in objs: continue
        if domain_name not in ogs: continue
        
        dom_objs = objs[domain_name]
        dom_ogs = ogs[domain_name]
        dom_pps = pps[domain_name]
        
        dom_cnt_cnf = 0
        dom_cnt_pool_tcp = 0
        dom_cnt_pool_udp = 0
        dom_cnt_alloc_tcp = 0
        dom_cnt_alloc_udp = 0
        
        for nat in nats[domain_name]:
            if nat['mode'] == 'dynamic':
                osrc = nat['oSource']
                tsrc = nat['tSource']
                
                if tsrc in dom_objs:
                    addr = dom_objs[tsrc]
                    if '-' not in addr:
                        tcp_alloc = 0
                        udp_alloc = 0
                        for pp in dom_pps:
                            if addr == pp['address']:
                                if pp['protocol'] == 'TCP': tcp_alloc += pp['allocated']
                                elif pp['protocol'] == 'UDP' : udp_alloc += pp['allocated']
                        records.append([domain_name, osrc, tsrc, addr, 'TCP', tcp_alloc])
                        records.append([domain_name, osrc, tsrc, addr, 'UDP', udp_alloc])
                        dom_cnt_cnf += 2
                        dom_cnt_pool_tcp += 65535
                        dom_cnt_alloc_tcp += tcp_alloc
                        dom_cnt_pool_udp += 65535
                        dom_cnt_alloc_udp += udp_alloc
                        
                elif tsrc in dom_ogs:
                    for obj_name in dom_ogs[tsrc]:
                        addr = dom_objs[obj_name]
                        if '-' not in addr:
                            tcp_alloc = 0
                            udp_alloc = 0
                            for pp in dom_pps:
                                if addr == pp['address']:
                                    if pp['protocol'] == 'TCP': tcp_alloc += pp['allocated']
                                    elif pp['protocol'] == 'UDP' : udp_alloc += pp['allocated']
                            records.append([domain_name, osrc, tsrc, addr, 'TCP', tcp_alloc])
                            records.append([domain_name, osrc, tsrc, addr, 'UDP', udp_alloc])
                            dom_cnt_cnf += 2
                            dom_cnt_pool_tcp += 65535
                            dom_cnt_alloc_tcp += tcp_alloc
                            dom_cnt_pool_udp += 65535
                            dom_cnt_alloc_udp += udp_alloc
        
        nat_cnt_cnf += dom_cnt_cnf
        nat_cnt_pool_tcp += dom_cnt_pool_tcp
        nat_cnt_pool_udp += dom_cnt_pool_udp
        nat_cnt_alloc_tcp += dom_cnt_alloc_tcp
        nat_cnt_alloc_udp += dom_cnt_alloc_udp
        
        dom_usage_tcp = ((dom_cnt_alloc_tcp * 100.0) / dom_cnt_pool_tcp) if dom_cnt_alloc_tcp > 0 else 0.0
        dom_usage_udp = ((dom_cnt_alloc_udp * 100.0) / dom_cnt_pool_udp) if dom_cnt_alloc_udp > 0 else 0.0
        
        dom_usage_big = dom_usage_tcp if dom_usage_tcp > dom_usage_udp else dom_usage_udp
        
        counters.html(
            COL(2).html(
                PANEL(CLASS=panel_color(dom_usage_big), STYLE='text-align:center;'
                ).Head(
                    HEAD(4, STYLE='margin:0px;').html(domain_name)
                ).Body(
                    ROW().html(
                        COL(6, STYLE='padding:0px;').html(
                            '<strong>TCP</strong>',
                            HEAD(4, STYLE='margin:0px;').html('%.2f<small> %%</small>' % dom_usage_tcp),
                            '<strong>%d</strong>' % dom_cnt_alloc_tcp
                        ),
                        COL(6, STYLE='padding:0px;').html(
                            '<strong>UDP</strong>',
                            HEAD(4, STYLE='margin:0px;').html('%.2f<small> %%</small>' % dom_usage_udp),
                            '<strong>%d</strong>' % dom_cnt_alloc_udp
                        )
                    )
                )
            )
        )
    
    records = sorted(records, reverse=True, key=lambda r: r[5])
    for r in records:
        pct = ((r[5] * 100.0) / 65535) if r[5] > 0 else 0.0
        table.Record(r[0], r[1], r[2], r[3], r[4], '<strong>%d</strong>' % r[5], '<strong>%.2f</strong> %%' % pct, CLASS=rec_color(pct))
    
    V.Page.html(
        ROW().html(
            COL(4).html(COUNTER(V('PAT Pool Configs'), 'list', nat_cnt_cnf, CLASS='panel-dgrey')),
            COL(4).html(COUNTER(V('PAT TCP Pool Allocated'), 'exchange', nat_cnt_alloc_tcp, CLASS='panel-dgrey')),
            COL(4).html(COUNTER(V('PAT UDP Pool Allocated'), 'long-arrow-right', nat_cnt_alloc_udp, CLASS='panel-dgrey'))
        ),
        counters,
        table
    )
    V.Menu.html(BUTTON(CLASS='btn-primary').click('/'.join(R.Path)).html(V('Refresh')))
    
@pageview(Manager)
def pat_pool_graph(R, M, V):
    if not M: V.Page.html(ALERT(V('Info'), V('Non-exist ASA Connection'), CLASS='alert-info')); return
    
    pools = M.NAT.PATPool.list()
    
    pool_list = ROW()
    
    for domain_name in sorted(M.keys()):
        pats = {}
         
        for pool in pools[domain_name]:
            addr = '%s/%s' % (pool['address'], pool['protocol'])
            if addr not in pats: pats[addr] = {'range' : [], 'count' : [], 'alloc' : [], 'total_count' : 0, 'total_alloc' : 0}
            rsplit = pool['range'].split('-')
            rstart = int(rsplit[0])
            rend = int(rsplit[1])
            count = rend - rstart + 1
            alloc = pool['allocated']
            pats[addr]['range'].append(pool['range'])
            pats[addr]['count'].append(count)
            pats[addr]['alloc'].append(alloc)
            pats[addr]['total_count'] += count
            pats[addr]['total_alloc'] += alloc
         
        for addr in sorted(pats.keys()):
            pat = pats[addr]
            total_free = pat['total_count'] - pat['total_alloc']
            percent = (pat['total_alloc'] * 100.0) / pat['total_count']
             
            rfreg = DIV(STYLE='text-align:center;width:200px;')
            for i in range(0, len(pat['range'])):
                rfreg.html(
                    SPAN(STYLE='margin:0px 2px 0px 2px;').html(
                        FIGURE.PIE(pat['alloc'][i], pat['count'][i] - pat['alloc'][i], width=40, height=40, **FIGURE.THEME_UTIL),
                    ),
                    SPAN(STYLE='position:absolute;transform:translateX(-42px);padding-top:14px;width:40px;text-align:center;').html(
                        STRONG().html('Seg%d' % (i + 1))
                    )
                )
             
            pool_list.html(
                COL(2, scr='sm', STYLE='padding:0px 5px 0px 5px;').html(
                    DIV(STYLE='width:200px;margin:auto;').html(
                        DIV(STYLE='text-align:center;').html(
                            DIV(STYLE='position:absolute;width:200px;height:200px;text-align:center;').html(
                                DIV(STYLE='padding-top:20px;').html(
                                    STRONG(STYLE='font-size:50px;').html('%.1f' % percent),
                                    SPAN(STYLE='font-size:14px;font-weight:bold;').html('%')
                                ),
                                STRONG(STYLE='font-size:16px;').html(addr),
                                rfreg,
                                STRONG().html(str(pat['total_alloc']) + ' '),
                                SMALL().html(V('counts'))
                            ),
                            FIGURE.DONUT(pat['total_alloc'], total_free, width=200, height=200, hole=80, **FIGURE.THEME_UTIL),
                        )
                    )
                )
            )
    
    V.Page.html(pool_list)

@pageview(Manager)
def config_ipuser(R, M, V):
    if not M: V.Page.html(ALERT(V('Info'), V('Non-exist ASA Connection'), CLASS='alert-info')); return
    
    alert = None
    if R.Method == 'POST':
        if M.addIpUser(R.Data['domain'], R.Data['ip'], R.Data['user']):
            alert = ALERT(V('Register Success'), V('%s/%s to %s') % (R.Data['domain'], R.Data['ip'], R.Data['user']), CLASS='alert-success')
        else:
            alert = ALERT(V('Register Failed'), V('Incorrect Setting %s/%s to %s') % (R.Data['domain'], R.Data['ip'], R.Data['user']), CLASS='alert-danger')
    
    elif R.Method == 'DELETE':
        if M.delIpUser(R.Path[3], R.Path[4]):
            alert = ALERT(V('Delete Success'), V('Erasing %s/%s') % (R.Path[3], R.Path[4]), CLASS='alert-success')
        else:
            alert = ALERT(V('Delete Failed'), V('Incorrect Erasing %s/%s') % (R.Path[3], R.Path[4]), CLASS='alert-danger')
    
    if alert != None: V.Page.html(alert)
    
    V.Page.html(
        POST('/asa/conf/ipuser', V('Register'), CLASS='btn-primary', STYLE='float:right;'
        ).Select('domain', POST.LABEL_TOP(V('ASA Domain Name')), *M.keys()
        ).Text('ip', POST.LABEL_TOP(V('IP')), placeholder=V('XXX.XXX.XXX.XXX')
        ).Text('user', POST.LABEL_TOP(V('User Name')), placeholder=V('Good User'))
    )
    
    table = TABLE.BASIC(V('Domain'), V('IP'), V('User'))
    for _, ipuser in M.ipusers.items():
        table.Record(ipuser['domain'],
                     ipuser['ip'],
                     DIV().html(ipuser['user'], DELETE.CLICK('/asa/conf/ipuser/%s/%s' % (ipuser['domain'], ipuser['ip']), tail=True)))
    
    V.Page.html(table)

@pageview(Manager)
def config(R, M, V):
    alert = None
    if R.Method == 'POST':
        if M.addDomain(R.Data['domain_name'], R.Data['ip'], R.Data['user'], R.Data['password']):
            alert = ALERT(V('Connection Success'), V('Setting %s with %s') % (R.Data['ip'], R.Data['domain_name']), CLASS='alert-success')
        else:
            alert = ALERT(V('Connection Failed'), V('Incorrect Setting %s') % R.Data['domain_name'], CLASS='alert-danger')
        
    elif R.Method == 'DELETE':
        if M.delDomain(R.Path[3]):
            alert = ALERT(V('Disconnection Success'), V('Erasing %s') % R.Path[3], CLASS='alert-success')
        else:
            alert = ALERT(V('Disconnection Failed'), V('Incorrect Erasing %s') % R.Path[3], CLASS='alert-danger')
    
    V.Menu.html(
        MODAL(V('Register ASA Domain'), BUTTON(CLASS='btn-primary', STYLE='float:right;').html(V('Connect ASA'))).html(
            POST('/asa/conf/domain', V('Register'), CLASS='btn-primary', STYLE='float:right;'
            ).Text('domain_name', POST.LABEL_TOP(V('ASA Domain Name')), placeholder=V('Unique Name Required')
            ).Text('ip', POST.LABEL_TOP(V('ASA Address')), placeholder='XXX.XXX.XXX.XXX'
            ).Text('user', POST.LABEL_TOP(V('Admin ID')), placeholder='admin'
            ).Password(label=POST.LABEL_TOP(V('Password')))
        )
    )
    
    table = TABLE.FLIP(V('Domain Name'), V('+ASA IP'), V('+Administrator ID'), V('+Start Connections'), V('+Max Connections'), '')
    
    for domain_name in sorted(M.keys()):
        table.Record(domain_name,
                     M[domain_name]['ip'],
                     M[domain_name]['user'],
                     M[domain_name]['conns'],
                     M[domain_name]['conn_max'],
                     DELETE.BUTTON('/asa/conf/domain/%s' % domain_name, V('Delete'), tail=True, CLASS='btn-xs'))
    
    if alert != None: V.Page.html(alert)
    V.Page.html(table)