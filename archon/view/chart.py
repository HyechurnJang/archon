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

from core import *

class Chart(VIEW):
       
    def __init__(self, _type, *labels, **options):
        VIEW.__init__(self, 'DIV', **{'id' : VIEW.getUUID(), 'lib' : 'dimple'})
        if 'xkey' not in options: options['xkey'] = 'X'
        if 'ykey' not in options: options['ykey'] = 'Y'
        if 'xaxis' not in options: options['xaxis'] = True
        if 'yaxis' not in options: options['yaxis'] = True
        if 'width' not in options: options['width'] = 0
        if 'height' not in options: options['height'] = 0
        if 'min' not in options: options['min'] = None
        if 'max' not in options: options['max'] = None
        if 'health' not in options: options['health'] = False
        if 'legend' not in options: options['legend'] = False
        self.series = []
        self.labels = labels
        self.label_len = len(labels)
        self.xkey = options['xkey']
        self.ykey = options['ykey']
        self.options = options
        self['chart'] = {
            'type' : _type,
            'series' : self.series,
            'options' : options
        }
  
class Line(Chart):
      
    def __init__(self, *labels, **options):
        Chart.__init__(self, 'line', *labels, **options)
         
    def Data(self, series, *vals):
        datasets = []
        series = {'series' : series, 'datasets' : datasets}
        for i in range(0, self.label_len):
            datasets.append({self.xkey : self.labels[i], self.ykey : vals[i]})
        self.series.append(series)
        return self
    
class Bar(Chart):
     
    def __init__(self, *labels, **options):
        Chart.__init__(self, 'bar', *labels, **options)
         
    def Data(self, series, *vals):
        for i in range(0, self.label_len):
            self.series.append({self.xkey : self.labels[i], 'series' : series, self.ykey : vals[i]})
        return self

class Pie(Chart):
    
    def __init__(self, *labels, **options):
        Chart.__init__(self, 'pie', *labels, **options)
         
    def Data(self, series, *vals):
        datasets = []
        series = {'series' : series, 'datasets' : datasets}
        for i in range(0, self.label_len):
            datasets.append({self.xkey : self.labels[i], self.ykey : vals[i]})
        self.series.append(series)
        return self

class Donut(Chart):
    def __init__(self, *labels, **options):
        if 'size' not in options: options['size'] = 10
        Chart.__init__(self, 'donut', *labels, **options)
         
    def Data(self, series, *vals):
        datasets = []
        series = {'series' : series, 'datasets' : datasets}
        for i in range(0, self.label_len):
            datasets.append({self.xkey : self.labels[i], self.ykey : vals[i]})
        self.series.append(series)
        return self

class HealthLine(Line):
      
    def __init__(self, *labels, **options):
        options['health'] = True
        options['min'] = 0
        options['max'] = 100
        Line.__init__(self, *labels, **options)
        self['chart']['options']['health_min_r'] = "0"
        self['chart']['options']['health_min_g'] = "0"
        self['chart']['options']['health_max_r'] = "0"
        self['chart']['options']['health_max_g'] = "0"
        self.health_min = 100
        self.health_max = 0
         
    def Data(self, series, *vals):
        datasets = []
        series = {'series' : series, 'datasets' : datasets}
        for i in range(0, self.label_len):
            val = vals[i]
            if val == None: val = 0
            if val < self.health_min: self.health_min = val
            if val > self.health_max: self.health_max = val
            datasets.append({self.xkey : self.labels[i], self.ykey : val})
        self.series.append(series)
        min_r = str(255 - int( ( 0.01 * self.health_min ) * 255 ))
        min_g = str(int( ( 0.01 * self.health_min ) * 255 ))
        max_r = str(255 - int( ( 0.01 * self.health_max ) * 255 ))
        max_g = str(int( ( 0.01 * self.health_max ) * 255 ))
        self['chart']['options']['health_min_r'] = min_r
        self['chart']['options']['health_min_g'] = min_g
        self['chart']['options']['health_max_r'] = max_r
        self['chart']['options']['health_max_g'] = max_g
        return self

class HealthBar(Bar):
     
    def __init__(self, *labels, **options):
        options['health'] = True
        options['min'] = 0
        options['max'] = 100
        Bar.__init__(self, *labels, **options)
        self['chart']['options']['health_min_r'] = "0"
        self['chart']['options']['health_min_g'] = "0"
        self['chart']['options']['health_max_r'] = "0"
        self['chart']['options']['health_max_g'] = "0"
        self.health_min = 100
        self.health_max = 0
         
    def Data(self, series, *vals):
        for i in range(0, self.label_len):
            val = vals[i]
            if val == None: val = 0
            if val < self.health_min: self.health_min = val
            if val > self.health_max: self.health_max = val
            self.series.append({self.xkey : self.labels[i], 'series' : series, self.ykey : vals[i]})
        min_r = str(255 - int( ( 0.01 * self.health_min ) * 255 ))
        min_g = str(int( ( 0.01 * self.health_min ) * 255 ))
        max_r = str(255 - int( ( 0.01 * self.health_max ) * 255 ))
        max_g = str(int( ( 0.01 * self.health_max ) * 255 ))
        self['chart']['options']['health_min_r'] = min_r
        self['chart']['options']['health_min_g'] = min_g
        self['chart']['options']['health_max_r'] = max_r
        self['chart']['options']['health_max_g'] = max_g
        return self

class Topo(VIEW):
    
    def __init__(self, **options):
        if 'width' not in options: options['width'] = 0
        if 'height' not in options: options['height'] = 400
        VIEW.__init__(self, 'CANVAS', **{'id' : VIEW.getUUID(), 'lib' : 'arbor', 'class' : 'arborwrapper'})
        self.nodes = {}
        self.edges = {}
        self['topo'] = {
            'datasets' : {'nodes' : self.nodes, 'edges' : self.edges},
            'options' : options
        }
    
    def Node(self, name, label=None, color='grey', dot=False):
        if label == None: label = name
        if dot: self.nodes[name] = {'label' : label, 'color' : color, 'shape' : 'dot'}
        else: self.nodes[name] = {'label' : label, 'color' : color}
        return self

    def Edge(self, src, dst, color='grey'):
        if src not in self.edges: self.edges[src] = {}
        self.edges[src][dst] = {}
        return self
    
    def __len__(self, *args, **kwargs):
        return self.nodes.__len__()
    
    def isNode(self, name):
        if name in self.nodes: return True
        return False

class Gauge(VIEW):
    
    def __init__(self, title, value, min=0, max=100, **attrs):
        VIEW.__init__(self, 'DIV', **ATTR.merge(attrs, {'id' : VIEW.getUUID(), 'lib' : 'justgage'}))
        self['chart'] = {'title' : title, 'value' : value, 'min' : min, 'max' : max}
