# -*- coding: utf-8 -*-

import json
import re

from archon import pageview
from archon.view import *
from manager import ACIManager

# Create your views here.

@pageview(ACIManager)
def device(manager, request, method, path, query, data, menu):
    
    layout = DIV()
    
    if len(path) > 3:
        domain_name = path[3]
        dn = '/'.join(path[4:])
        
        node_data = manager[domain_name](dn, detail=True)
        children = node_data.children(detail=True)
        
        layout.html(HEADER(1).html(node_data['name']))
        
        lo_detail = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
        for key in node_data: lo_detail.html(KeyVal(key, node_data[key]))
        
        if hasattr(node_data, 'System'):
            lo_system = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
            for key in node_data.System: lo_system.html(KeyVal(key, node_data.System[key]))
            layout.html(Col(6).html(HEADER(3).html('Details')).html(lo_detail))
            layout.html(Col(6).html(HEADER(3).html('System')).html(lo_system))
        else:
            layout.html(Col(12).html(HEADER(3).html('Details')).html(lo_detail))
        
        lo_child = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
        layout.html(Col(12).html(HEADER(3).html('Child Objects')).html(lo_child))
        for child in children:
            key = child.keys(); val = []; hkey = []
            for k in key: val.append(child[k])
            for k in key: hkey.append('+' + k)
            lo_child.html(FooTable('Class Name', *hkey).record(child.class_name, *val))
            
        return layout
    
    node_data = manager.Node.list(detail=True)
    node_health = manager.Node.health()
    cfrm_data = manager.Class('firmwareCtrlrRunning').list(detail=True)
    sfrm_data = manager.Class('firmwareRunning').list(detail=True)
    tsys_data = manager.System.list(detail=True)
     
    for domain_name in manager:
        table = DataTable('Type', 'ID', 'Name', 'Model', 'Serial', 'Version', 'INB Mgmt IP', 'OOB Mgmt IP', 'State', 'Uptime')
         
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
                        table.record('Controller',
                                     id,
                                     Get(node['name'], '/aci/show/device/' + domain_name + '/' + node['dn']),
                                     node['model'],
                                     node['serial'],
                                     firm['version'],
                                     inb,
                                     oob,
                                     'Service' if state == 'in-service' else 'Enormal',
                                     uptime[:-5])
                        break
            elif node['role'] == 'spine':
                cnt_spne += 1
                for firm in sfrm_data[domain_name]:
                    if node['dn'] + '/' in firm['dn']:
                        table.record('Spine',
                                     id,
                                     Get(node['name'], '/aci/show/device/' + domain_name + '/' + node['dn']),
                                     node['model'],
                                     node['serial'],
                                     firm['version'],
                                     inb,
                                     oob,
                                     'Service' if state == 'in-service' else 'Enormal',
                                     uptime[:-4])
                        break
            elif node['role'] == 'leaf':
                cnt_leaf += 1
                for firm in sfrm_data[domain_name]:
                    if node['dn'] + '/' in firm['dn']:
                        table.record('Leaf',
                                     id,
                                     Get(node['name'], '/aci/show/device/' + domain_name + '/' + node['dn']),
                                     node['model'],
                                     node['serial'],
                                     firm['version'],
                                     inb,
                                     oob,
                                     'Service' if state == 'in-service' else 'Enormal',
                                     uptime[:-4])
                        break
        layout.html(HEADER(1).html(domain_name + u' 도메인'))
        layout.html(table)
     
    if layout.isEmpty(): layout.html(Alert(u'알림', u'APIC 연결이 없습니다', **{'class' : 'alert-info'}))
     
    return layout

@pageview(ACIManager)
def tenant(manager, request, method, path, query, data, menu):
    
    layout = DIV()
    
    if len(path) > 3:
        domain_name = path[3]
        dn = '/'.join(path[4:])
        
        tenant = manager[domain_name](dn, detail=True)
        
        layout.html(HEADER(1).html(tenant['name']))
        
        lo_detail = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
        layout.html(Col(12).html(HEADER(3).html('Details')).html(Col(12).html(lo_detail)))
        for key in tenant: lo_detail.html(KeyVal(key, tenant[key]))
        
        approf = tenant.AppProfile.list(detail=True)
        lo_ap = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
        lo_detail.html(DIV().html(HEADER(4).html('Application Profile')).html(lo_ap))
        for ap in approf:
            key = ap.keys(); val = []; hkey = []
            for k in key: val.append(ap[k])
            for k in key: hkey.append('+' + k if k != 'name' else k)
            lo_ap.html(FooTable(*hkey).record(*val))
            
            epgs = ap.EPG.list(detail=True)
            lo_epg = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
            lo_ap.html(DIV().html(HEADER(4).html('EPGs')).html(lo_epg))
            for epg in epgs:
                key = epg.keys(); val = []; hkey = []
                for k in key: val.append(epg[k])
                for k in key: hkey.append('+' + k if k != 'name' else k)
                lo_epg.html(FooTable(*hkey).record(*val))
        
        
#         lo_bd = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
#         layout.html(DIV().html(HEADER(3).html('EPGs')).html(lo_bd))
#         
#         lo_ctx = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
#         layout.html(DIV().html(HEADER(3).html('EPGs')).html(lo_ctx))
#         
#         lo_ctr = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
#         layout.html(DIV().html(HEADER(3).html('EPGs')).html(lo_ctr))
#         
#         lo_flt = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
#         layout.html(DIV().html(HEADER(3).html('EPGs')).html(lo_flt))
#          
#         lo_child = DIV(**{'style' : 'padding:0px 0px 0px 40px;'})
#         layout.html(DIV().html(HEADER(3).html('Child Objects')).html(lo_child))
        
        return layout
        
    tns = manager.Tenant.list()
    epgs = manager.EPG.list()
    bds = manager.BridgeDomain.list()
    ctxs = manager.Context.list()
    ctrs = manager.Contract.list()
    flts = manager.Filter.list()
    
    table = DataTable('Domain', 'Name', 'EPG', 'Bridge Domain', 'Context', 'Contract', 'Filter')
    
    tn_cnt = 0
    
    for domain_name in manager:
        
        for tn in tns[domain_name]:
            tn_cnt += 1
            name = tn['name']
            epg_data = '<ul style="list-style:none;padding-left:10px;margin:0px;">'
            bd_data = '<ul style="list-style:none;padding-left:10px;margin:0px;">'
            ctx_data = '<ul style="list-style:none;padding-left:10px;margin:0px;">'
            ctr_data = '<ul style="list-style:none;padding-left:10px;margin:0px;">'
            flt_data = '<ul style="list-style:none;padding-left:10px;margin:0px;">'
            
            for epg in epgs[domain_name]:
                if tn['dn'] in epg['dn']: epg_data += '<li><small>' + re.sub('(ap-|epg-)', '', '/'.join(epg['dn'].split('/')[2:])) + '</small></li>'
            
            for bd in bds[domain_name]:
                if tn['dn'] in bd['dn']: bd_data += '<li><small>' + bd['name'] + '</small></li>'
            
            for ctx in ctxs[domain_name]:
                if tn['dn'] in ctx['dn']: ctx_data += '<li><small>' + ctx['name'] + '</small></li>'
                
            for ctr in ctrs[domain_name]:
                if tn['dn'] in ctr['dn']: ctr_data += '<li><small>' + ctr['name'] + '</small></li>'
                
            for flt in flts[domain_name]:
                if tn['dn'] in flt['dn']: flt_data += '<li><small>' + flt['name'] + '</small></li>'
            
            epg_data += '</ul>'    
            bd_data += '</ul>'
            ctx_data += '</ul>'
            ctr_data += '</ul>'
            flt_data += '</ul>'
            
            table.record(domain_name, Get(name, '/aci/show/tenant/' + domain_name + '/' + tn['dn']), epg_data, bd_data, ctx_data, ctr_data, flt_data)
    
    if table.isEmpty():
        layout.html(Alert(u'알림', u'APIC 연결이 없습니다', **{'class' : 'alert-info'}))
    else:
        layout.html(
            Panel(**{'class' : 'panel-default'}).Head(
                Row().html(
                    Col(3).html(
                        Icon('users', **{'class' : 'fa-5x'})
                    )
                ).html(
                    Col(9, **{'class' : 'text-right'}).html(
                        DIV(**{'class' : 'huge-font'}).html(tn_cnt)
                    ).html(
                        DIV().html('Tenants')
                    )
                )
            )
        )
        layout.html(table)
    
    return layout

@pageview(ACIManager)
def epg(manager, request, method, path, query, data, menu):
    return 'Endpoint Group'

@pageview(ACIManager)
def ep(manager, request, method, path, query, data, menu):
    return 'Endpoint'

@pageview(ACIManager)
def contract(manager, request, method, path, query, data, menu):
    return 'Contract'

@pageview(ACIManager)
def external(manager, request, method, path, query, data, menu):
    return 'External Network'

@pageview(ACIManager)
def fault(manager, request, method, path, query, data, menu):
    return 'Fault'


@pageview(ACIManager)
def intf_util(manager, request, method, path, query, data, menu):
    return 'Interface Utilization'

@pageview(ACIManager)
def epg_util(manager, request, method, path, query, data, menu):
    return 'Epg Utilization'


@pageview(ACIManager)
def eptracker(manager, request, method, path, query, data, menu):
    return 'EP Tracker'

@pageview(ACIManager)
def ofinder(manager, request, method, path, query, data, menu):
    return 'Object Finder'


@pageview(ACIManager)
def config(manager, request, method, path, query, data, menu):
    
    alert = None
    
    if method == 'POST':
        if manager.addDomain(data['domain_name'], data['ip'], data['user'], data['passwd']):
            alert = Alert(u'연결 성공', data['ip'] + u'와 연결이 ' + data['domain_name'] + u' 으로 설정되었습니다', **{'class' : 'alert-success'})
        else:
            alert = Alert(u'연결 실패', data['domain_name'] + u'와 연결이 실패하였습니다', **{'class' : 'alert-danger'})
        
    elif method == 'DELETE':
        if manager.delDomain(path[2]):
            alert = Alert(u'제거 성공', path[2] + u'와 연결이  제거되었습니다', **{'class' : 'alert-success'})
        else:
            alert = Alert(u'제거 실패', path[2] + u'의 연결이 제거되지 않았습니다', **{'class' : 'alert-danger'})
        
    menu.html(
        Modal(BUTTON, u'APIC 연결', 'Register APIC Domain', **{'class' : 'btn-primary', 'style' : 'float:right;'}).html(
            Post('/aci/conf', 'Register', **{'class' : 'btn-primary', 'style' : 'float:right;'}
            ).Text('domain_name', Post.TopLabel('Domain Name')
            ).Text('ip', Post.TopLabel('APIC Address'), placeholder='XXX.XXX.XXX.XXX'
            ).Text('user', Post.InLabel('User Name')
            ).Password()
        )
    )
    
    table = FooTable('Domain Name', '+APIC IP', u'+관리자 ID', u'+시작 커넥션 개수', u'+최대 커넥션 개수', '')
    for domain_name in manager:
        table.record(domain_name, 
                     manager[domain_name]['ip'], 
                     manager[domain_name]['user'],
                     manager[domain_name]['conns'],
                     manager[domain_name]['conn_max'],
                     DelButton('/aci/conf/' + domain_name, u'삭제', tail=True))
    
    ret = DIV()
    if alert != None: ret.html(alert)
    return ret.html(table)





