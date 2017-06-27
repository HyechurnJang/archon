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

import re
import ipaddress
from archon import *

def get_host_type(V, t):
    if t == 'phys': return V('Physical Device')
    elif t == 'virt': return V('Virtual Machine')
    elif t == 'hv': return V('Hypervisor')
    else: return V('Unknown')
    
def get_power_stat(V, pw):
    pw_low = pw.lower()
    if 'power' in pw_low:
        if 'on' in pw_low: return V('Power ON'), '/resources/images/tool/play.png'
        elif 'off' in pw_low: return V('Power OFF'), '/resources/images/tool/stop.png'
    return V('Unknown'), '/resources/images/vendor/color/question.png'

def get_host_os(V, os, cfgdos=None):
    
    def get_host_name_img(os_name):
        os_low = os_name.lower()
        if 'centos' in os_low: return os_name, '/resources/images/vendor/color/centos.png'
        elif 'ubuntu' in os_low: return os_name, '/resources/images/vendor/color/ubuntu.png'
        elif 'hat' in os_low: return os_name, '/resources/images/vendor/color/redhat.png'
        elif 'windows' in os_low: return os_name, '/resources/images/vendor/color/windows.png'
        elif 'suse' in os_low: return os_name, '/resources/images/vendor/color/suse.png'
        elif 'debian' in os_low: return os_name, '/resources/images/vendor/color/debian.png'
        elif 'fedora' in os_low: return os_name, '/resources/images/vendor/color/fedora.png'
        elif 'linux' in os_low: return os_name, '/resources/images/vendor/color/linux.png'
        elif 'vmware' in os_low: return 'VMWare', '/resources/images/vendor/color/vmware.png'
        elif 'openstack' in os_low: return 'OpenStack', '/resources/images/vendor/color/openstack.png'
        else: return V('Unknown'), '/resources/images/vendor/color/question.png'
    
    if os: return get_host_name_img(os)
    if cfgdos: return get_host_name_img(cfgdos)
    return V('Unknown'), '/resources/images/vendor/color/question.png'

def get_rn(dn):
    ret = re.match('(?P<path>.*)/(?P<key>\w+)-(?P<rn>\[?[\W\w]+\]?)$', dn)
    if ret: return ret.group('path'), ret.group('key'), ret.group('rn')
    ret = re.match('^(?P<rn>\w+)$', dn)
    if ret: return None, None, ret.group('rn')
    return None, None, None

def set_topo(topo, dn, color='grey', path_color='grey', dot=False):
    
    prev_dn = None
    while True:
        if topo.isNode(dn): break
            
        path, kn, rn = get_rn(dn)
        if kn != None: label = kn.upper() + ':' + rn
        else: label = rn 

        if prev_dn == None:
            topo.Node(dn, label, color=color, dot=dot)
        else:
            topo.Node(dn, label, color=path_color)
            topo.Edge(prev_dn, dn)
        if topo.isNode(path):
            topo.Edge(dn, path)
            break
        if path == None: break
        prev_dn = dn
        dn = path


def get_dn_topo(dn):
    sdn = dn.split('/')
    sdn_len = len(sdn)
    topo = TOPO()
    prev_name = None
    for i in range(0, sdn_len):
        rn = sdn[i]
        kv = re.match('^(?P<key>\w+)-(?P<val>[\W\w]+)', rn)
        if kv: name = '%s:%s' % (kv.group('key').upper(), kv.group('val'))
        else: continue
        if i == sdn_len - 1: topo.Node(name, color='red', dot=True)
        else: topo.Node(name, color='orange')
        if prev_name != None: topo.Edge(prev_name, name)
        prev_name = name
    return topo

def is_ip_name(ip):
    if Archon.INV.IP.Get(ip) != None: return True
    return False

def is_mac_name(mac):
    if Archon.INV.MAC.Get(mac) != None: return True
    return False

def get_ip_name(ip):
    name = Archon.INV.IP.Get(ip)
    if name != None: return '%s (%s)' % (ip, name)
    return ip

def get_mac_name(mac):
    name = Archon.INV.MAC.Get(mac)
    if name != None: return '%s (%s)' % (mac, name)
    return mac

def set_ip_name(ip, name):
    Archon.INV.IP[ip] = name
    
def set_mac_name(mac, name):
    Archon.INV.MAC[mac.upper()] = name

def is_ip_addr(ip):
    kv = re.match('\s*(?P<ip>\d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d?)', ip)
    if kv != None: return kv.group('ip')
    return ''

def get_ip_range(ip_stt, ip_end):
    ip_stt = is_ip_addr(ip_stt)
    ip_end = is_ip_addr(ip_end)
    if ip_stt != '':
        if ip_end == '': return [ip_stt]
        ip_stt = ipaddress.ip_address(unicode(ip_stt))
        ip_end = ipaddress.ip_address(unicode(ip_end))
        if ip_stt >= ip_end: return [str(ip_stt)]
        i = 0
        ret = []
        while True:
            _tmp = ip_stt + i
            i += 1
            if _tmp <= ip_end: ret.append(str(_tmp))
            else: break
        return ret
    return []

def get_comma_to_list(text):
    return re.sub(',\s+', ',', text).split(',')